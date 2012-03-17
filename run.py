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
        print "\n{}: {}".format(i, s.get_sentence())
        if word in s.sentence:
            break

def make_plural_nouns(n=10):
    """
    Print n nouns in their plural form, as a test and to catch exceptions.
    """
    for i in range(n):
        print Inflector.inflect_noun(l.random(category='noun'))

def be():
    s.sentence = []
    s.technical_sentence = []
    s.pos_sentence = []
    s.process('SENTENCE')
    for part_of_speech in s.pos_sentence:
        if 'main-' in part_of_speech:
            part_of_speech = part_of_speech[5:]
        verb_type = ''
        if 'verb' == part_of_speech[:4]:
            verb_type = part_of_speech[5:]
            part_of_speech = part_of_speech[:4]
        s.technical_sentence.append(s.lexicon.random(verb_type, category=part_of_speech))
    s.technical_sentence[s.pos_sentence.index('main-verb-linking')] = s.lexicon.search(base='be')[0]

    for word in s.technical_sentence:
        s.sentence.append(word['base'])

    s.sentence = s.inflector.inflect(s.technical_sentence, s.pos_sentence, s.sentence)

    import string
    s.sentence[0] = string.capwords(s.sentence[0])
    s.sentence = ' '.join(s.sentence) + "."
    print s.sentence

#############
# BEGIN
#############
def main():
    pprint.pprint(s.grammar)
    for i in range(10):
        print "\n{0}: {1}\n".format(i+1, s.get_sentence())
        print "["+' '.join(s.pos_sentence)+"]"

if __name__ == '__main__':
    main()