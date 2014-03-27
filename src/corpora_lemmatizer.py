#!/usr/bin/python
#-*- coding: utf-8 -*-

'''
Takes a collection of texts and lemmatizes it. The current options for 
lemmatization are restricted to the TreeTagger POS tagger.

The current implementation allows input only from a MongoDB database. Likewise,
the only output format implemented is to write the lemmatized texts to a 
directory in the filesystem.

The objective of this program is to parallelize the execution of a lemmatizer 
in several threads. Further parallelization may be achieved by dividing
the corpus into two or more parts. The number of threads is configurable.

TODO: implement an option to allow input from collections of texts in the 
filesystem.
TODO: implement an option to save the processed files in MongoDB.
TODO: add new options of lemmatizers (such as Morfette).
 

Created on Jul 16, 2012

@author: desouza
'''

from multiprocessing.process import Process
#from pymongo import Connection
import argparse
import codecs
import glob
import os.path
import sys
import time
import treetaggerwrapper

# globals
DEFAULT_TT_PATH = os.path.expanduser("~") + '/Tools/tree-tagger'
DEFAULT_THREADS_NUM = 8
SPACE = " "
NL = "\n"
BUFFER_SIZE = 1000

def set_cmdline_handler():
    desc = '''Takes a collection of texts and lemmatizes it. The current options for 
lemmatization are restricted to the TreeTagger POS tagger.

The current implementation allows input from a MongoDB database or from
files in the filesystem. The only output format implemented is to write the 
lemmatized texts to a directory in the filesystem.

The objective of this program is to parallelize the execution of a lemmatizer 
in several threads. Further parallelization may be achieved by dividing
the corpus into two or more parts. The number of threads is configurable.
'''  
    
    parser = argparse.ArgumentParser(description=desc)
    
    # positional arguments
#    db_group = parser.add_argument_group('db_input')
#    db_group.add_argument('address', metavar='address', type=str, 
#                        help='the address name/ip of the database')
#    db_group.add_argument('db_name', metavar='db_name', type=str, 
#                        help='the name of the corpora database')
#    db_group.add_argument('collection', metavar="collection_name", type=str, 
#                        help='the name of the collection that contains the corpus.')
    
    files_group = parser.add_argument_group('input_dir')
    files_group.add_argument('input_directory', metavar='input_path', type=str,
                             help='the directory where the input files are.')
    files_group.add_argument('-e', '--extension', metavar='ext', type=str,
                             help='the extension of the input files.',
                             default='')
    
    # required infos
    parser.add_argument('language', metavar='lang', type=str,
                        help='specifies the language of the corpus to process.')
    parser.add_argument('output_path', metavar="directory_path", type=str,
                        help='specifies the path of the directory to which the annotated data will be saved.')
        
    # options
#    parser.add_argument("-p", "--port", metavar='port', type=int, 
#                        help='sets the MongoDB port (otherwise the default port is used.)')
    parser.add_argument("--treetagger_path", metavar="path", type=str,
                        default=DEFAULT_TT_PATH,
                        help='specifies the path of TreeTagger. Default is $HOME/tools/tree-tagger/bin')
    parser.add_argument("-t", "--threads", metavar="threads_number", type=int,
                        default=DEFAULT_THREADS_NUM,
                        help="the number of threads to use. Default is 8.")
    
    args = parser.parse_args()
    
    return args


def lemmatize_slice(collec, base, offset, args, output_path):
    for doc in collec.find(skip=base, limit=offset):
        parallelism = doc["parallel"]
        
        file = doc["files"]
                
        # gets text file name
        name_attrib = "id_file_" + args.language
        file_name = file[name_attrib]
        
        print "Processing", file_name
        
        # gets text in the specified language
        text = file[args.language]
    
        # sets the tagger instance    
        tagger = treetaggerwrapper.TreeTagger(TAGLANG=args.language, 
                                              TAGDIR=args.treetagger_path)
               
        if parallelism == "doc":
            # passes the whole content to the lemmatizer
            s = text[0]["content"]
            tags = tagger.TagText(s, tagonly=True, encoding="utf-8")
            
        else:
            # accumulates the sentences/paragraphs to pass to the lemmatizer
            s = ''
            for t in text:
                s += t['content']

        
        tags = tagger.TagText(s)
        try:
            out_name = output_path + os.sep + file_name + ".lemma"
            out_file = codecs.open(out_name, "w", "utf-8")
            for elem in tags:
                out_file.write(elem + "\n")
            
            out_file.close()
        except IOError as e:
            sys.exit(e)
        


def process_mongo(args, output_path):
    # connects to the MongoDB server
    if args.port:
        connection = Connection(args.address, args.port)
    else:
        connection = Connection(args.address)
    
    # gets the DB
    db = connection[args.db_name]
    
    # gets the collection
    collec = db[args.collection]
    
    # sets the number of documents to be processed by each thread
    docs_num = collec.count()
    slice_size = docs_num / args.threads
    print "Threads:", args.threads
    print "Documents number:", docs_num
    print "Documents per thread:", slice_size

    # initiates a thread for each slice of documents
    # the slices are controlled using the base and offset variables
    base = 0
    offset = slice_size
    jobs = []
    for thread_num in range(args.threads):
        print "Initializing process", thread_num
        p = Process(target=lemmatize_slice, args=(collec, base, offset, args, output_path))
        jobs.append(p)
        p.start()
        base += offset
    
    for p in jobs:
        p.join()
    
    if (docs_num % 2) == 1:
        lemmatize_slice(collec, base, offset, args, output_path)

def lemmatize_files(files, output_path, args):
    # sets the tagger instance    
    tagger = treetaggerwrapper.TreeTagger(TAGLANG=args.language, 
                                          TAGDIR=args.treetagger_path)

    for file_name in files:
        try:
            out_name = output_path + os.sep + os.path.basename(file_name) + ".lemma"
            out_file = codecs.open(out_name, "w", "utf-8")

            in_file = codecs.open(file_name, 'r', 'utf-8')
            line_counter = 1
            for line in in_file:
                tokens = line.replace(SPACE, NL)
                tags = tagger.TagText(tokens, tagonly=True, encoding="utf-8")

                for elem in tags:
                    out_file.write(elem + "\n")
                
                out_file.write(NL)
                
                if (line_counter % BUFFER_SIZE) == 0:
                    out_file.flush()
                
                line_counter += 1
                
            out_file.close()

        except IOError as e:
            sys.stderr.write("error reading line: " + line_counter)
            sys.stderr.write(line)
            sys.exit(e)
              

def process_input_dir(args, input_path, output_path):
    patt = input_path + os.sep + "*" + args.extension
    files = glob.glob(patt)
    docs_num = len(files)
    if docs_num > args.threads:
        slice_size = docs_num / args.threads
    else:
        slice_size = 1
    print "Threads:", args.threads
    print "Documents number:", docs_num
    print "Documents per thread:", slice_size

    start = 0
    jobs = []
    for job_num in range(args.threads):
        print "Initializing process", job_num
        end = start + slice_size
        p = Process(target=lemmatize_files, args=(files[start:end], output_path, args))
        print files[start:end]
        jobs.append(p)
        p.start()
    	start += slice_size

    for p in jobs:
        p.join()
    
    if (docs_num % 2) == 1:
        lemmatize_files(files, output_path, args)
    
    

def main():
    args = set_cmdline_handler()
    
    input_path = os.path.expanduser(args.input_directory)
    if not os.path.exists(input_path):
        print "error: the input path does not exist."
        sys.exit(1)
    
    output_path = os.path.expanduser(args.output_path)
    if not os.path.exists(output_path):
        print "error: the output path does not exist."
        sys.exit(1)

#    if args.address and input_path:
#        print "error: conflicting input data: either the data comes from the database or from the filesystem."
#        sys.exit(1)

    
#    if args.address:
#        t1 = time.time()
#        process_mongo(args, output_path)
        
    if input_path:
        t1 = time.time()
        process_input_dir(args, input_path, output_path)
        
    t2 = time.time()
    total_time = (t2 - t1) / 60
    print "Processing time:", total_time, "minutes."
         
if __name__ == '__main__':
    main()
