import os, random, string
import xml.etree.ElementTree as xml


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
            if arg != '':
                kwargs.update({arg: None})
        if kwargs:
            return random.choice(self.search(**kwargs))
        else:
            return random.choice(self.words)

class Sentence(object):
    def __init__(self, lexicon, inflector):
        self.base_sentence = []
        self.pos_sentence = []
        self.technical_sentence = []
        self.final_sentence = ""
        self.grammar = self.parse_grammar()
        self.lexicon = lexicon
        self.inflector = inflector

    def parse_grammar(self):
        """
        Parses the grammar file into an internal dictionary.
        """
        # possible_types = (
        #     'indicative',
        # )
        # self.base_sentence_type = random.choice(possible_types)

        data = open('data/grammar.txt', 'r').read().split('\n')

        # delete comments and blank lines from grammar data
        for i in range(len(data)-1, -1, -1):
               if not data[i] or data[i][0] == '#':
                   del data[i]

        for i in range(0, len(data)):
            data[i] = data[i].split(' -> ')

        grammar = {}
        for element in data:
            if element[0] not in grammar:
                grammar[element[0]] = []
            for item in element[1].split(' | '):
                grammar[element[0]].append(item.split(' '))

        return grammar

    def process(self, level):
        """
        Recursively constructs a sentence diagram.
        """
        def go(level):
            if level in self.grammar:
                next = random.choice(self.grammar[level])
                for element in next:
                    go(element)
            else:
                if level != '_':
                    result.append(level)

        result = []
        go(level)
        return result

    def get_sentence(self, level='S'):
        """
        Returns a randomly generated sentence. This is the most top-level user-accessed
        method so far. Everything else is automatic.
        """
        self.pos_sentence = []
        self.technical_sentence = []
        self.base_sentence = []
        self.final_sentence = ""

        self.pos_sentence = self.process(level)
        for pos in self.pos_sentence:
            if 'verb' == pos[:4]:
                new_word = self.lexicon.random(pos[5:], category='verb')
            elif 'adverb' == pos[:6]:
                new_word = self.lexicon.random(pos[7:], category='adverb')
            else:
                new_word = self.lexicon.random(category=pos)
            self.technical_sentence.append(new_word)
            self.base_sentence.append(new_word['base'])

        self.inflector.inflect(self.base_sentence, self.pos_sentence, self.technical_sentence)

        if 'i' in self.base_sentence:
            self.base_sentence[self.base_sentence.index('i')] = 'I'

        self.final_sentence = string.capwords(self.base_sentence[0])+" "+" ".join(self.base_sentence[1:])
        if 'whose' in self.base_sentence or 'whom' in self.base_sentence:
            self.final_sentence += "?"
        else:
            self.final_sentence += "."

        #... add complements
