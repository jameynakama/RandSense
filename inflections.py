'''

Adjectives: comparative, superlative


Determiners can have <singularorplural/> tag, so check for this and do a choice on the noun if so


'''



class Inflector(object):

	VOWELS = ['a', 'e', 'i', 'o', 'u',]

	# pronouns = ['I', 'you', 'he', 'she', 'it', 'we', 'you', 'they', 'somebody', 'someone',
	# 			'something', 'whoever', 'ye', 'anyone', 'anything', 'everybody', 'everyone',
	# 			'everything', 'nobody', 'none', 'nothing', 'one', 'plenty']
	# possessive_pronouns = ['my', 'your', 'his', 'her', 'its', 'our', 'your', 'their']

	@staticmethod
	def inflect_noun(determiner, noun):
		# right now just try to make plurals
		if 'plural' in determiner:
			if 'plural' in noun:
				noun = noun['plural']
			else:
				noun = noun['base']
				if noun[-2:] in ['ey',]:
					noun = noun+'s'
				if noun[-1] in ['y',]:
					noun = noun[:-1]+'ies'
				elif noun[-2:] in ['ss', 'ch',]:
					noun = noun+'es'
				elif noun[-1] in ['s',]:
					noun = noun+'ses'
				else:
					noun = noun+'s'
		else:
			noun = noun['base']

		determiner = determiner['base']

		if determiner in ['a', 'an',]:
			if noun[0] in Inflector.VOWELS:
				determiner = 'an'
			else:
				determiner = 'a'

		return determiner, noun

	@staticmethod
	def inflect_verb(verb):
		pass