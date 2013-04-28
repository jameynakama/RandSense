#!/usr/bin/env python

import pprint
from argparse import ArgumentParser

from sentences import Lexicon, Sentence
from inflections import Inflector


lexicon = Lexicon()
inflector = Inflector()
sentence = Sentence(lexicon, inflector)
sentence.parse_grammar()

''' helper functions
---------------------------'''

def foo(word='random'):
    """
    Print sentences until the given word is in one.
    """
    i = 0
    while True:
        i += 1
        sentence.get_sentence()
        print "\n{}: {}".format(i, sentence.final_sentence)
        if word in sentence.base_sentence:
            break

''' begin
---------------------------'''

def main():
    op = ArgumentParser(description="RandSense-python")

    op.add_argument(
        "-n", "--number",
        help="define how many sentences to generate",
        default=10,
    )
    op.add_argument(
        "-g", "--grammar",
        action="store_true",
        help="print grammar object before sentences",
        default=False,
    )
    op.add_argument(
        "-p", "--pos",
        action="store_true",
        help="print 'part of speech' sentence with each sentence",
        default=False,
    )
    op.add_argument(
        "-t", "--tech",
        action="store_true",
        help="print 'technical sentence' with each sentence",
        default=False,
    )
    op.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="prints all optional output; same as -gpt"
    )
    op.add_argument(
        "-l", "--level",
        help="begin at the given sentence level",
        default="S",
    )

    args = op.parse_args()
    if args.number < 1:
        op.error("you cannot print a negative number of sentences!")

    if args.grammar or args.verbose:
        pprint.pprint(sentence.grammar)
    for i in range(args.number):
        sentence.get_sentence(args.level)
        print "\n> {number}: {sentence}".format(number=i+1, sentence=sentence.final_sentence)
        if args.pos or args.verbose:
            print "\n'part of speech' sentence:\n\t{0}".format(' '.join(sentence.pos_sentence))
        if args.tech or args.verbose:
            print "\ntechnical sentence:"
            pprint.pprint(sentence.technical_sentence)

if __name__ == '__main__':
    main()
