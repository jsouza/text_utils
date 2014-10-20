#!/usr/bin/env python

import sys
import codecs
from nltk import FreqDist

def main():
	args = sys.argv
	input_file = codecs.open(args[1], 'r', 'utf-8')
	fd = FreqDist()
	for line in input_file:
		tokens = line.split(" ")
		for token in tokens:
			fd[token.lower()] += 1

	print "Number of unique occurrences = ", fd.B()

if __name__ == "__main__":
	main()