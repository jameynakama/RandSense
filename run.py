import pprint

from sentences import Lexicon, Sentence
from inflections import Inflector


l = Lexicon()
i = Inflector()
s = Sentence(l, i)

#############
# helper functions
#############
def foo(word='random'):
    """
    Print sentences until the given word is in one.
    """
    i = 0
    while True:
        i += 1
        s.get_sentence()
        print "\n{}: {}".format(i, s.final_sentence)
        if word in s.base_sentence:
            break

#############
# BEGIN
#############
def main():
    print
    pprint.pprint(s.grammar)
    for i in range(10):
        s.get_sentence()
        print "\n{}: {}".format(i+1, s.final_sentence)
        # print "["+' '.join(s.pos_sentence)+"]"
        # pprint.pprint(s.technical_sentence)

if __name__ == '__main__':
    main()

s.parse_grammar()
