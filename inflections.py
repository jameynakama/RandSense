'''

Adjectives: comparative, superlative


Determiners can have <singularorplural/> tag, so check for this and do a choice on the noun if so


'''



class Inflector(object):

	# pronouns = ['I', 'you', 'he', 'she', 'it', 'we', 'you', 'they', 'somebody', 'someone',
	# 			'something', 'whoever', 'ye', 'anyone', 'anything', 'everybody', 'everyone',
	# 			'everything', 'nobody', 'none', 'nothing', 'one', 'plenty']
	# possessive_pronouns = ['my', 'your', 'his', 'her', 'its', 'our', 'your', 'their']

	@staticmethod
	def inflect_noun(noun):
		# right now just try to make plurals
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

		return noun

	@staticmethod
	def inflect_verb(verb):
		pass