#!/usr/local/bin/python2.7
# encoding: utf-8
'''
analysis.remove_lines -- Removes a list of lines (specified by their numbers) from
an input file.

analysis.remove_lines is script that removes lines from a text file. The lines are
specified by their number in an input file. The results are written to the standard
output.

It defines classes_and_methods

@author:     José Guilherme
        
@copyright:  2013 José Guilherme. All rights reserved.
        
@license:    Apache License

@contact:    jose.camargo.souza@gmail.com
@deffield    updated: Updated
'''

from argparse import ArgumentParser, RawDescriptionHelpFormatter
import argparse
import codecs
import os
import sys


__all__ = []
__version__ = 0.1
__date__ = '2013-04-23'
__updated__ = '2013-04-23'


def main(argv=None):  # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version, program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by user_name on %s.
  Copyright 2013 organization_name. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license,
                                formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("delete_lines", action="store",
                            help="File containing the line numbers to remove.")
        parser.add_argument("input_file", action="store",
                            help="Text file to be processed.")
        parser.add_argument('-V', '--version', action='version',
                            version=program_version_message)

        # Process arguments
        args = parser.parse_args()

        try:
            lines_file = codecs.open(args.delete_lines, 'r')
            input_file = codecs.open(args.input_file, 'r')
        except IOError, e:
            sys.stderr.write("error: could not open input file " + e)

        lines_list = lines_file.readlines()
        lines_list = [int(t) for t in lines_list]

        for i, l in enumerate(input_file):
            if i not in lines_list:
                sys.stdout.write(l.strip() + "\n")

    except Exception, e:
        return 2

if __name__ == "__main__":
    sys.exit(main())
