import os, random, string
import xml.etree.ElementTree as xml

from inflections import Inflector


class Lexicon(object):
	def __init__(self):
		self.xml_tree = xml.parse(os.path.join('data/lexicon.xml'))
		self.root = self.xml_tree.getroot()

		self.words = []
		for word in self.root:
			word_dict = {}
			for line in word:
				word_dict.update({line.tag: line.text})
			self.words.append(word_dict)

	def search(self, *args, **kwargs):
		"""
		Returns a list of word dictionaries matching all the given traits
		and tag values.

		Examples:
		lexicon.search('transitive', ditranstive')
		lexicon.search(base='jump', category='verb')
		lexicon.search('intrasitive', base='jump')
		"""
		for arg in args:
			kwargs.update({arg: None})
		result = []
		for entry in self.words:
			if all(item in entry.items() for item in kwargs.items()):
				result.append(entry)
		return result

	def random(self, *args, **kwargs):
		"""
		Similar to search() in usage, this will return a random word based
		on the given arguments.

		Examples:
		lexicon.random()
		lexicon.random('transitive')
		lexicon.random(category='noun')
		"""
		for arg in args:
			kwargs.update({arg: None})
		if kwargs:
			return random.choice(self.search(**kwargs))
		else:
			return random.choice(self.words)

class Sentence(object):
    VOWELS = ['a', 'e', 'i', 'o', 'u']

    def __init__(self, lexicon):
        self.pos_sentence = []
        self.sentence = ''
        self.grammar = self.parse_grammar()
        self.lexicon = lexicon

    def parse_grammar(self):
        # possible_types = (
        #     'indicative',
        #     )
        # self.sentence_type = random.choice(possible_types)

        data = open('data/grammar.txt', 'r').read().split('\n')

        # delete comments and blank lines from grammar data
        for i in range(len(data)-1, -1, -1):
       		if not data[i] or data[i][0] == '#':
       			data.pop(i)

        for i in range(0, len(data)):
            data[i] = data[i].split(' -> ')

        grammar = {}
        for element in data:
            grammar[element[0]] = []
            for item in element[1].split(' | '):
                grammar[element[0]].append(item.split(' '))

        return grammar

    def process(self, level):
        if level in self.grammar:
            next = random.choice(self.grammar[level])
            for element in next:
                self.process(element)
        else:
            self.pos_sentence.append(level)

    def get_sentence(self):
        self.pos_sentence = []
        self.technical_sentence = []
        self.sentence = []
        self.process('SENTENCE')
        for part_of_speech in self.pos_sentence:
        	self.technical_sentence.append(self.lexicon.random(category=part_of_speech))
        for word in self.technical_sentence:
        	self.sentence.append(word['base'])

        # # Here's where we'll do replacements, like inflections (for now)
        # while 'ART-INDEF' in self.pos_sentence:
        #     index = self.pos_sentence.index('ART-INDEF')
        #     if self.sentence[index+1][0] in Sentence.VOWELS:
        #         self.sentence[index] = 'an'
        #     else:
        #         self.sentence[index] = 'a'
        #     self.pos_sentence[index] = 'ART-INDEF-REPLACED'

        # # TEMPORARY LOCATORS (right now this only works with one word each - find better way)
        # if 'VT' in self.pos_sentence:
        #     index = self.pos_sentence.index('VT')
        #     self.sentence[index] = "<"+self.sentence[index]+">"
        # if 'VI' in self.pos_sentence:
        #     index = self.pos_sentence.index('VI')
        #     self.sentence[index] = "<"+self.sentence[index]+">"

        Inflector.inflect(self.technical_sentence)

        self.sentence[0] = string.capwords(self.sentence[0])
        self.sentence = ' '.join(self.sentence) + "."
        return self.sentence