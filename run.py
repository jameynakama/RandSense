import pprint

from sentences import Lexicon, Sentence
from inflections import Inflector


lexicon = Lexicon()
inflector = Inflector()
sentence = Sentence(lexicon, inflector)
sentence.parse_grammar()

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
        sentence.get_sentence()
        print "\n{}: {}".format(i, sentence.final_sentence)
        if word in sentence.base_sentence:
            break

#############
# BEGIN
#############
def main():
    # pprint.pprint(s.grammar)                   # print grammar object
    for i in range(10):
        sentence.get_sentence()
        print "\n{number}: {sentence}".format(number=i+1, sentence=sentence.final_sentence)
        # print "["+' '.join(s.pos_sentence)+"]" # also print pos_sentence
        # pprint.pprint(s.technical_sentence)    # also print technical_sentence

if __name__ == '__main__':
    main()


