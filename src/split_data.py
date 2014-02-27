#!/usr/local/bin/python2.7
# encoding: utf-8
'''
analysis.reproduce_split -- script to reproduce the same train/test split
accross different files

analysis.reproduce_split is a script that makes it possible to reproduce
train/test split accross different files in a dataset

It defines classes_and_methods

@author:     José de Souza
        
@copyright:  2013 organization_name. All rights reserved.
        
@license:    license

@contact:    user_email
@deffield    updated: Updated
'''

from argparse import ArgumentParser, RawDescriptionHelpFormatter
import numpy as np
from sklearn.cross_validation import train_test_split
import codecs
import os
import sys


__all__ = []
__version__ = 0.1
__date__ = '2013-05-26'
__updated__ = '2013-05-26'


def main(argv=None):  # IGNORE:C0111
    '''Command line options.'''

    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_version = "v%s" % __version__
    program_build_date = str(__updated__)
    program_version_message = '%%(prog)s %s (%s)' % (program_version,
                                                     program_build_date)
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by José on %s.
  Copyright 2013 organization_name. All rights reserved.

  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0

  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc, str(__date__))

    # Setup argument parser
    parser = ArgumentParser(description=program_license,
                            formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("input_file", type=str,
                        help="file to be split into train and test.")
    parser.add_argument("portion", type=float,
                        help="portion of the file to be split for test.")
    parser.add_argument("seed", type=int,
                        help="seed for the pseudo-random-number generator.")

    parser.add_argument("-v", "--verbose", dest="verbose", action="count",
                        help="set verbosity level [default: %(default)s]")
    parser.add_argument('-V', '--version', action='version',
                        version=program_version_message)

    # Process arguments
    args = parser.parse_args()

    input_file = codecs.open(args.input_file, "r", "utf-8")
    input_lines = input_file.readlines()
    input_idxes = np.arange(len(input_lines))
    train, test = train_test_split(input_idxes, test_size=args.portion,
                                   random_state=args.seed)

    out_name = input_file.name + ".ratio" + str(args.portion) +\
    '.seed' + str(args.seed)

    train_out = codecs.open(out_name + ".train", "w", "utf-8")
    test_out = codecs.open(out_name + ".test", "w", "utf-8")

    print len(train)
    print len(test)

    for idx in train:
        train_out.write(input_lines[int(idx)])

    for idx in test:
        test_out.write(input_lines[int(idx)])

    train_out.close()
    test_out.close()

    return 0

if __name__ == "__main__":
    sys.exit(main())
