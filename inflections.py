


class Inflector(object):
	pronouns = ['I', 'you', 'he', 'she', 'it', 'we', 'you', 'they', 'somebody', 'someone',
				'something', 'whoever', 'ye', 'anyone', 'anything', 'everybody', 'everyone',
				'everything', 'nobody', 'none', 'nothing', 'one', 'plenty']
	possessive_pronouns = ['my', 'your', 'his', 'her', 'its', 'our', 'your', 'their']

	@staticmethod
	def inflect(technical_sentence):
		print
		print technical_sentence