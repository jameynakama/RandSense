import os, random, string
import wordnik

API_KEY = "1081e3eed25591267a10307da5c01c675d1d199db0e2d7c3f"

class ObjectList(object):
    def __init__(self):
        self.list = []
        self.words = set()
        self.parts_of_speech = set()
        self.uniques = set()

    def __repr__(self):
        result = "["
        for item in self.list:
            if self.list.index(item) < 15:
                result += item.__repr__()+", "
        if len(self.list) > 15:
            result += "..."
        return result + "]"

    def __getitem__(self, key):
        return self.list[key]

    def __len__(self):
        return len(self.list)

    def all(self):
        result = ObjectList()
        for word in self.list:
            result.save(word)
        return result

    def count(self):
        return len(self.list)

    def filter(self, init=False, **kwargs):
        # return a new ObjectList so it can continue being filtered/checked/etc.
        if init: result = []
        else: result = ObjectList()
        for word in self.list:
            if all(item in word.__dict__.items() for item in kwargs.items()):
                if init: result.append(word)
                else: result.save(word)
        return result

    def save(self, word):
        self.list.append(word)
        self.words.add(word.word)
        self.parts_of_speech.add(word.part_of_speech)
        self.uniques.add((word.word, word.part_of_speech))

    def random(self, part_of_speech=''):
        if part_of_speech:
            return random.choice(self.filter(part_of_speech=part_of_speech))
        else:
            return random.choice(self.list)

class DictionaryParser(object):
    def __init__(self):
        pass

    def parse(self):

        words = ''
        for text_file in os.listdir('data/dictionary/'):
            words += open('data/dictionary/'+text_file, 'r').read()

        words = words.split("******")[1:]
        for i in range(len(words)):
            w = Word()
            words[i] = words[i].strip().split('\n')
            w.word = words[i][0].split(': ', 1)[-1]
            w.part_of_speech = words[i][1].split(': ', 1)[-1]
            w.definitions = words[i][2:]
            w.save()

class Word(object):
    objects = ObjectList()

    def __init__(self):
        self.word = ''
        self.part_of_speech = ''
        self.definitions = []

    def __repr__(self):
        return "<" + self.word + " - " + self.part_of_speech + ">"

    # "PUBLIC"

    def save(self):
        # validate here
        Word.objects.save(self)
        
class Sentence(object):
    VOWELS = ['a', 'e', 'i', 'o', 'u']

    def __init__(self):
        self.pos_sentence = []
        self.sentence = ''
        self.grammar = self.parse_grammar()

    def parse_grammar(self):
        # possible_types = (
        #     'declarative',
        #     )
        # self.sentence_type = random.choice(possible_types)

        data = open('data/grammar.txt', 'r').read().split('\n')

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
        self.sentence = []
        self.process('SENTENCE')
        for part_of_speech in self.pos_sentence:
            self.sentence.append(Word.objects.random(part_of_speech).word)

        # Here's where we'll do replacements, like conjugations
        while 'ART-INDEF' in self.pos_sentence:
            index = self.pos_sentence.index('ART-INDEF')
            if self.sentence[index+1][0] in Sentence.VOWELS:
                self.sentence[index] = 'an'
            else:
                self.sentence[index] = 'a'
            self.pos_sentence[index] = 'ART-INDEF-REPLACED'

        # TEMPORARY LOCATORS (right now this only works with one word each - find better way)
        if 'VT' in self.pos_sentence:
            index = self.pos_sentence.index('VT')
            self.sentence[index] = "<"+self.sentence[index]+">"
        if 'VI' in self.pos_sentence:
            index = self.pos_sentence.index('VI')
            self.sentence[index] = "<"+self.sentence[index]+">"


        self.sentence[0] = string.capwords(self.sentence[0])
        self.sentence = ' '.join(self.sentence) + "."
        return self.sentence


def cycle_definitions():
    for word in Word.objects.all():
        print word
        for definition in word.definitions:
            print "{index}: {definition}".format(
                index=word.definitions.index(definition)+1,
                definition=definition,
                )
        raw_input()

def get_word(part_of_speech):
    return w.words_get_random_word(includePartOfSpeech=part_of_speech)['word']

def make_sentence(parts_of_speech):
    """
    Pass in a sentence filled with parts of speech to construct a real sentence.
    E.g., 'noun verb-transitive adjective noun'
    """

    result = []
    for word in parts_of_speech.split(' '):
        result.append(get_word(word))
    return ' '.join(result).capitalize() + '.'

def foo(s):
    while True:
        print s.get_sentence()
        if 'poop' in s.sentence:
            break



w = wordnik.Wordnik(API_KEY)
dp = DictionaryParser()
dp.parse()

s = Sentence()