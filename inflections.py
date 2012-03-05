'''

Adjectives: comparative, superlative


Determiners can have <singularorplural/> tag, so check for this and do a choice on the noun if so


'''



class Inflector(object):

	pronouns = ['I', 'you', 'he', 'she', 'it', 'we', 'you', 'they', 'somebody', 'someone',
				'something', 'whoever', 'ye', 'anyone', 'anything', 'everybody', 'everyone',
				'everything', 'nobody', 'none', 'nothing', 'one', 'plenty']
	possessive_pronouns = ['my', 'your', 'his', 'her', 'its', 'our', 'your', 'their']

	@staticmethod
	def inflect_noun(noun):
		# right now just try to make plurals
		if 'plural' in noun:
			result = noun['plural']+" <-- irregular form found"
		else:
			noun = noun['base']
			if noun[-2:] in ['ey',]:
				result = noun+'s'
			if noun[-1] in ['y',]:
				result = noun[:-1]+'ies'
			elif noun[-2:] in ['ss', 'ch',]:
				result = noun+'es'
			elif noun[-1] in ['s',]:
				result = noun+'ses'
			else:
				result = noun+'s'

		return result

	@staticmethod
	def inflect_verb(verb):
		pass