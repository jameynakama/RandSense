import os, random, string, pprint
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

        data = open('data/grammar/bases.txt', 'r').read().split('\n')

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
        def go(level):
            if level in self.grammar:
                next = random.choice(self.grammar[level])
                for element in next:
                    go(element)
            else:
                result.append(level)

        result = []
        go(level)
        return result

    def get_sentence(self):
        """
        Returns a randomly generated sentence. This is the most top-level user-accessed
        method so far. Everything else is automatic.
        """
        self.pos_sentence = []
        self.technical_sentence = []
        self.sentence = []

        # CORE SENTENCE
        #1. get np
        np = self.get_noun_phrase()
        #2. get vp
        vp = self.get_verb_phrase()
        #3. conjugate
        self.send_to_inflector(np, vp, 'plural' in np[0])

        #... add complements

        #.... add adjectives, adverbs

        #-1. make 'a' and 'an' correct
        while 'indefinite-article' in self.pos_sentence:
            index_of_article = self.pos_sentence.index('indefinite-article')
            index_of_next_word = index_of_article + 1
            next_word = self.sentence[index_of_next_word]
            if next_word[0] in ['a', 'e', 'i' 'o', 'u']:
                # return 'an'
                self.sentence[index_of_article] = 'an'
            else:
                # return 'a'
                self.sentence[index_of_article] = 'a'
            self.pos_sentence[index_of_article] = 'determiner'

        # print self.sentence
        # print self.pos_sentence
        # pprint.pprint(self.technical_sentence)

    def get_noun_phrase(self):
        """
        Gets a basic noun phrase and returns the technical version of it.
        """
        pos_np = self.process("NP")
        tech_np = []
        for pos in pos_np:
            new_word = self.lexicon.random(category=pos)
            tech_np.append(new_word)
            self.technical_sentence.append(new_word)
            self.pos_sentence.append(new_word['category'])
            self.sentence.append(new_word['base'])

        if 'noun' in pos_np:
            if 'plural' in tech_np[0]:
                self.sentence[1] = self.inflector.pluralize_noun(tech_np[1])

        return tech_np

    def get_verb_phrase(self):
        """
        Gets a basic verb phrase and returns the technical version of it.
        """
        pos_vp = self.process("VP")
        tech_vp = []
        for pos in pos_vp:
            new_word = self.lexicon.random(pos[5:], category=pos[:4])
            tech_vp.append(new_word)
            self.technical_sentence.append(new_word)
            self.pos_sentence.append(new_word['category'])
            self.sentence.append(new_word['base'])

        return tech_vp

    def send_to_inflector(self, tech_np, tech_vp, is_plural):
        self.sentence[-1] = self.inflector.do_verb(tech_np[-1], tech_vp[0], is_plural)