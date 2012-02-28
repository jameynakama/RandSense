import random

class Sentence(object):
	def __init__(self):
		self.sentence = []
		self.grammar = self.parse_grammar()

	def get_sentence(self):
		self.sentence = []
		self.process('SENTENCE')
		return self.sentence[0].capitalize() + ' ' + ' '.join(self.sentence[1:]) + '.'

	def process(self, level):
		if level in self.grammar:
			next = random.choice(self.grammar[level])
			for element in next:
				self.process(element)
		else:
			self.sentence.append(level)

	def parse_grammar(self):
		data = open('grammar.txt', 'r').read().split('\n')

		for i in range(0, len(data)):
			data[i] = data[i].split(' -> ')

		grammar = {}
		for element in data:
			grammar[element[0]] = []
			for item in element[1].split(' | '):
				grammar[element[0]].append(item.split(' '))

		return grammar


# figure out the difference between required constituents and 
# choice constituents

grammar = {
	'SENTENCE': [['SUBJECT', 'PREDICATE']],
	'SUBJECT': [['NP']],
	'NP': [['ARTICLE', 'cat']],
	'ARTICLE': [['a'], ['the']],
	'PREDICATE': [['VP']],
	'VP': [['meows'], ['jumped'], ['is purring']],
}

s = Sentence()
for i in range(10):
	print s.get_sentence()