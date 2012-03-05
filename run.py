from sentences import Lexicon, Sentence
from inflections import Inflector


l = Lexicon()
s = Sentence(l)

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

#############
# BEGIN
#############
def main():
    for i in range(10):
        print "\n{0}: {1}".format(i+1, s.get_sentence())

if __name__ == '__main__':
    main()