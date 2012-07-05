import pdb
import random


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
        },
    }

    VERB_TYPES = ['verb-intransitive', 'verb-transitive', 'verb-ditransitive',]

    def inflect(self, base_sentence, pos_sentence, technical_sentence):
        """
        Here we check for all the conditions which require an inflection (and route the required
        actions). This includes pluralizing nouns for plural-only determiners, conjugating verbs
        according to subject and tense, and performing similar actions.
        """

        #1. inflect nouns by examining their determiners
        self.route_nouns(base_sentence, pos_sentence, technical_sentence)

        #2. conjugate verbs by finding their subjects (and determiners)
        self.route_verbs(base_sentence, pos_sentence, technical_sentence)

        #3. make indefinite articles agree
        while 'indefinite-article' in pos_sentence:
            new_determiner = self.make_article_agree(base_sentence[pos_sentence.index('indefinite-article')+1])
            base_sentence[pos_sentence.index('indefinite-article')] = new_determiner
            pos_sentence[pos_sentence.index('indefinite-article')] = 'determiner'

    def route_nouns(self, base_sentence, pos_sentence, technical_sentence):
        while 'determiner' in pos_sentence:
            # find all determiners and their following nouns
            determiner_index = pos_sentence.index('determiner')
            if 'plural' in technical_sentence[determiner_index]:
                for i in range(determiner_index, len(pos_sentence)):
                    if pos_sentence[i] == 'noun':
                        noun_index = i
                        break
                base_sentence[noun_index] = self.pluralize_noun(technical_sentence[noun_index])
                pos_sentence[noun_index] = 'noun-inflected'
                pos_sentence[determiner_index] = 'determiner-done'
            else:
                # maybe do random plurals here later
                pos_sentence[determiner_index] = 'determiner-done'

        for i in range(len(pos_sentence)):
            if '-done' in pos_sentence[i]:
                pos_sentence[i] = pos_sentence[i][:-5]
            elif '-inflected' in pos_sentence[i]:
                pos_sentence[i] = pos_sentence[i][:-10]

    def route_verbs(self, base_sentence, pos_sentence, technical_sentence):
        for i in range(len(pos_sentence)):
            if pos_sentence[i][:4] == 'verb':
                pos_sentence[i] = 'verb'
        while 'verb' in pos_sentence:
            # find all verbs and their preceding subjects and determiners
            verb_index = pos_sentence.index('verb')
            for i in range(verb_index, -1, -1):
                if pos_sentence[i] in ['determiner', 'indefinite-article', 'nominative-pronoun', 'possessive-pronoun']:
                    determiner_index = i
                    break
            for i in range(verb_index, -1, -1):
                if pos_sentence[i] in ['noun', 'nominative-pronoun']:
                    subject_index = i
                    break
            base_sentence[verb_index] = self.do_verb(
                                                technical_sentence[subject_index],
                                                technical_sentence[verb_index],
                                                'plural' in technical_sentence[determiner_index],
                                                )
            pos_sentence[verb_index] = 'verb-conjugated'

    def make_article_agree(self, word):
        #
        # FIX things like "an" uniform, unicycle, etc.
        #
        if word[0] in ['a', 'e', 'i', 'o', 'u']:
            if word[:3] not in ['uni',]:
                return 'an'
            else:
                return 'a'
        else:
            return 'a'

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
                    elif verb['base'][-2:] == ['sh', 'ch',]:
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
            elif verb['base'][-2:] in ['ey', 'ay',]:
                return verb['base'] + 'ed'
            elif verb['base'][-1] == 'y':
                return verb['base'][:-1] + 'ied'
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

        return new_verb