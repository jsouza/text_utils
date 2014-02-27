'''
Created on Jun 4, 2013

@author: desouza
'''
import argparse
import sys
import random

desc = "Ramdomly samples a portion of the file passed to the standard input and writes it to the standard output."


def main():
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("--line_id", action="store_true",
                        help="outputs only the numbers of the samples lines.")
    parser.add_argument("--portion", type=float, default=0.25,
                       help="portion of the data to sample (default is 0.25).")
    parser.add_argument("--seed", type=int, default=42,
                        help="seed to use in the random number generator.")

    args = parser.parse_args()

    random.seed(args.seed)

    lines = sys.stdin.readlines()
    number_lines = len(lines)
    sample = random.sample(xrange(number_lines),
                           int(args.portion * number_lines))

    # outputs line numbers
    if args.line_id:
        for i in sample:
            sys.stdout.write(str(i) + "\n")

    # outputs the lines
    else:
        for i in sample:
            sys.stdout.write(lines[i])


if __name__ == '__main__':
    main()
