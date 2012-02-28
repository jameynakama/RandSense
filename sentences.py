import os, random
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
        if (word.word, word.part_of_speech) in self.uniques:
            # add to definitions of word if name and part of speech exist
            self.filter(init=True, word=word.word, part_of_speech=word.part_of_speech)[0].definitions.append(word.definition)
        else:
            # add the word normally if neither name or part of speech exist
            if 'definition' in word.__dict__:
                word.definitions.append(word.definition)
                del word.definition
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

    def parse(self, working_folder):

        words = ''
        for text_file in os.listdir('data/'+working_folder):
            words += open('data/'+working_folder+"/"+text_file, 'r').read()

        words = words.split("******")[1:]
        for i in range(len(words)):
            words[i] = words[i].strip('\n').split('\n')
            for j in range(len(words[i])):
                words[i][j] = words[i][j].split(': ', 1)
            Word(dict(words[i])).save()

class Word(object):
    objects = ObjectList()

    def __init__(self, dictionary):
        # word, part_of_speech, definition, verb_type
        for key, value in dictionary.iteritems():
            setattr(self, key, value)
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
            if level != '_':
                self.pos_sentence.append(level)

    def get_sentence(self):
        self.pos_sentence = []
        self.sentence = []
        self.process('SENTENCE')
        for part_of_speech in self.pos_sentence:
            self.sentence.append(Word.objects.random(part_of_speech).word)

        # Here's where we'll do replacements, like conjugations
        while 'indefinite-article' in self.pos_sentence:
            index = self.pos_sentence.index('indefinite-article')
            # print "!INDEFINITE ARTICLE DETECTED!"
            # print "The word following the article is ["+self.sentence[index+1]+"]"
            if self.sentence[index+1][0] in Sentence.VOWELS:
                self.sentence[index] = 'an'
            else:
                self.sentence[index] = 'a'
            self.pos_sentence[index] = 'indefinite-article-REPLACED'
        
        # TEMPORARY LOCATORS (right now this only works with one word each - find better way)
        if 'verb-transitive' in self.pos_sentence:
            index = self.pos_sentence.index('verb-transitive')
            self.sentence[index] = "<"+self.sentence[index]+">"
        if 'verb-intransitive' in self.pos_sentence:
            index = self.pos_sentence.index('verb-intransitive')
            self.sentence[index] = "<"+self.sentence[index]+">"

        self.sentence = ' '.join(self.sentence).capitalize() + "."
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


w = wordnik.Wordnik(API_KEY)
dp = DictionaryParser()
dp.parse("words")
