#!/usr/bin/python

import pprint
from optparse import OptionParser

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
    usage = "usage: %prog [options]"
    op = OptionParser(usage)

    op.set_defaults(number=10, grammar=False, pos=False, tech=False)
    op.add_option("-n", "--number", type="int", help="define how many sentences to generate")
    op.add_option("-g", "--grammar", action="store_true", help="print grammar object before sentences")
    op.add_option("-p", "--pos", action="store_true", help="print 'part of speech' sentence with each sentence")
    op.add_option("-t", "--tech", action="store_true", help="print 'technical sentence' with each sentence")
    op.add_option("-v", "--verbose", action="store_true", help="prints all optional output; same as -gpt")

    (options, args) = op.parse_args()
    if options.number < 1:
        op.error("you cannot print a negative number of sentences!")

    if options.grammar or options.verbose:
        pprint.pprint(sentence.grammar)
    for i in range(options.number):
        sentence.get_sentence()
        print "\n> {number}: {sentence}".format(number=i+1, sentence=sentence.final_sentence)
        if options.pos or options.verbose:
            print "\n'part of speech' sentence:\n\t{0}".format(' '.join(sentence.pos_sentence))
        if options.tech or options.verbose:
            print "\ntechnical sentence:"
            pprint.pprint(sentence.technical_sentence)

if __name__ == '__main__':
    main()


