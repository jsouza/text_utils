'''
Created on Nov 11, 2013

Kind of grep to match sentences present in one file in a second file.

@author: desouza
'''
import sys
import codecs


def main():
    args = sys.argv
    usage = "%s <sentences_file> <input_file>\n" % args[0]
    if len(args) < 3:
        sys.stderr.write(usage)
        sys.exit(1)

    lines_dict = {}
    for no, line in enumerate(codecs.open(args[2], 'r', 'utf-8'), 1):
        lines_dict[line.strip()] = no

    for sent in codecs.open(args[1], 'r', 'utf-8'):
        ssent = sent.strip()
        if lines_dict.get(ssent, False):
            sys.stdout.write("%i\t%s\n" % (lines_dict.get(ssent), ssent.encode('utf-8')))


if __name__ == '__main__':
    main()
