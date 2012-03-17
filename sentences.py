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
        self.pos_sentence = []
        self.technical_sentence = []
        self.sentence = []
        self.grammar = self.parse_grammar()
        self.lexicon = lexicon
        self.inflector = inflector

    def parse_grammar(self):
        """
        Parses the grammar file into an internal dictionary.
        """
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
            if element[0] not in grammar:
                grammar[element[0]] = []
            for item in element[1].split(' | '):
                grammar[element[0]].append(item.split(' '))

        return grammar

    def process(self, level):
        """
        Recursively constructs a sentence diagram.
        """
        if level in self.grammar:
            next = random.choice(self.grammar[level])
            for element in next:
                self.process(element)
        else:
            self.pos_sentence.append(level)

    def get_sentence(self):
        """
        Returns a randomly generated sentence. This is the most top-level user-accessed
        method so far. Everything else is automatic.
        """
        self.pos_sentence = []
        self.technical_sentence = []
        self.sentence = []
        self.process('SENTENCE')
        for part_of_speech in self.pos_sentence:
            if 'main-' in part_of_speech:
                part_of_speech = part_of_speech[5:]
            verb_type = ''
            if 'verb' == part_of_speech[:4]:
                verb_type = part_of_speech[5:]
                part_of_speech = part_of_speech[:4]
            self.technical_sentence.append(self.lexicon.random(verb_type, category=part_of_speech))
        for word in self.technical_sentence:
            self.sentence.append(word['base'])

        self.sentence = self.inflector.inflect(self.technical_sentence, self.pos_sentence, self.sentence)

        self.sentence[0] = string.capwords(self.sentence[0])
        self.sentence = ' '.join(self.sentence) + "."
        return self.sentence