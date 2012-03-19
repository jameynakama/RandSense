import pdb
import random


'''

Adjectives: comparative, superlative

Make "Warriors engage" possible (right now the logic is in place only for "a warrior"
    or "the warriors")

Determiners can have <singularorplural/> tag, so check for this and do a choice on the noun if so

Figure out how to handle more than one noun and verb in a clause

Recognize intransitive, transitive, and ditransitive

'''

class Inflector(object):
    VOWELS = ['a', 'e', 'i', 'o', 'u',]

    BE = {
        'present': {
            'i': 'am',
            'you': 'are',
            'it': 'is',
            'plural': 'are',
        },
        'simple_past': {
            'i': 'was',
            'you': 'were',
            'it': 'was',
            'plural': 'were',
        }
    }

    # pronouns = ['I', 'you', 'he', 'she', 'it', 'we', 'you', 'they', 'somebody', 'someone',
    # 'something', 'whoever', 'ye', 'anyone', 'anything', 'everybody', 'everyone',
    # 'everything', 'nobody', 'none', 'nothing', 'one', 'plenty']
    # possessive_pronouns = ['my', 'your', 'his', 'her', 'its', 'our', 'your', 'their']


    def inflect(self, technical_sentence, pos_sentence, base_sentence):
        """
        Here we check for all the conditions which require an inflection (and route the required
        actions). This includes pluralizing nouns for plural-only determiners, conjugating verbs
        according to subject and tense, and performing similar actions.
        """

        for pos in pos_sentence:
            if pos[:9] == 'main-noun':
                index_main_noun = pos_sentence.index(pos)
            elif pos[:9] == 'main-verb':
                index_main_verb = pos_sentence.index(pos)
        # index_determiners = []

        if 'determiner' in pos_sentence:
            determiner = technical_sentence[pos_sentence.index('determiner')]
            noun = technical_sentence[index_main_noun]
            if 'plural' in determiner:
                new_noun = self.pluralize_noun(noun)
                base_sentence[index_main_noun] = new_noun
                new_verb = self.do_verb(technical_sentence[index_main_noun], technical_sentence[index_main_verb], 'plural' in determiner)
                base_sentence[index_main_verb] = new_verb

        while 'indefinite-article' in pos_sentence:
            new_determiner = self.make_article_agree(technical_sentence[pos_sentence.index('indefinite-article')+1])
            base_sentence[pos_sentence.index('indefinite-article')] = new_determiner
            pos_sentence[pos_sentence.index('indefinite-article')] = 'determiner'

        return base_sentence

    def make_article_agree(self, word):
        #
        # FIX things like "an uniform" unicycle etc.
        #
        if word['base'][0] in Inflector.VOWELS:
            determiner = 'an'
        else:
            determiner = 'a'
        return determiner

    def pluralize_noun(self, noun):
        if 'plural' in noun:
            noun = noun['plural']
        else:
            noun = noun['base']
            if noun[-2:] in ['ey', 'ay',]:
                noun = noun+'s'
            elif noun[-1] in ['y',]:
                noun = noun[:-1]+'ies'
            elif noun[-2:] in ['ss', 'ch',]:
                noun = noun+'es'
            elif noun[-1] in ['s',]:
                noun = noun+'ses'
            else:
                noun = noun+'s'
        return noun

    def do_verb(self, subject, verb, is_plural):
        tense = random.choice([
            'present',
            'simple_past',
        ])

        if verb['base'] == 'be':
            return self.conjugate_for_be(subject, tense, is_plural)

        if tense == 'present':
            return self.conjugate_for_present(subject, verb, tense, is_plural)
        elif tense == 'simple_past':
            return self.conjugate_for_simple_past(verb)

    def conjugate_for_present(self, subject, verb, tense, is_plural):
        if is_plural:
            return verb['base']
        else:
            if subject['base'] not in ['i', 'you', 'we', 'they',]:
                if 'present3s' in verb:
                    return verb['present3s']
                else:
                    if verb['base'][-1] == 'y':
                        return verb['base'][:-1] + 'ies'
                    elif verb['base'][-2:] == 'sh':
                        return verb['base'] + 'es'
                    else:
                        return verb['base'] + 's'
            else:
                return verb['base']

    def conjugate_for_simple_past(self, verb):
        if 'past' in verb:
            return verb['past']
        else:
            if verb['base'][-1] == 'e':
                return verb['base'] + 'd'
            elif verb['base'][-1] == 'y':
                return verb['base'] + 'ied'
            else:
                return verb['base'] + 'ed'

    def conjugate_for_be(self, subject, tense, is_plural):
        if is_plural:
            new_verb = Inflector.BE[tense]['plural']
        else:
            if subject['base'] not in ['i', 'you',]:
                new_verb = Inflector.BE[tense]['it']
            else:
                new_verb = Inflector.BE[tense][subject['base']]

        print "MADE IT HERE"

        return new_verb