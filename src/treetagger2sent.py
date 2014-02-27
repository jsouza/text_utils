'''
Created on Nov 18, 2013

@author: desouza
'''
import codecs
import glob
import sys


def main():
    args = sys.argv
    if len(args) != 3:
        sys.stderr.write("Usage: %s <annotated_files_path> <sentence_file_path>\n" % args[0])
        sys.exit(1)

    annotated_files = glob.glob(args[1] + "/*.lemma")
    output_file = codecs.open(args[2], 'w', 'utf-8')
    for file_path in annotated_files:
        input_file = codecs.open(file_path, 'r', 'utf-8')
        out_line = ""
        for line in input_file:
            sline = line.strip()
            if sline == "":
                out_line += "\n"
                output_file.write(out_line)
                out_line = ""
                continue
            else:
                out_line += " "

            tok_line = sline.split()
            pos_tag = tok_line[1]
            out_line += pos_tag

        input_file.close()

    output_file.close()

if __name__ == '__main__':
    main()
