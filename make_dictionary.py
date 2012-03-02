import os
import wordnik

# make repeats not happen
#
# ideas:
# - create a set of the words and parts of speech
#
#

API_KEY = "1081e3eed25591267a10307da5c01c675d1d199db0e2d7c3f"

infile = "word_list.txt"
outdir = "data/dictionary/"

translations = {
    'noun': 'N',
    'verb-transitive': 'VT',
    'verb-intransitive': 'VI',
    'definite-article': 'ART-DEF',
    'indefinite-article': 'ART-INDEF',
    'adjective': 'ADJ',
}

def translate(part_of_speech):
    global translations
    if part_of_speech in translations.keys():
        return translations[part_of_speech]
    elif part_of_speech in translations.values():
        return [key for key in translations if translations[key] == part_of_speech][0]

w = wordnik.Wordnik(API_KEY)

no_definitions_list = []

if os.path.exists('data/existing'):
    existing_words = eval(open('data/existing', 'r').read())
else:
    existing_words = set()

try:
    for line in open('data/'+infile, 'r'):
        if line[0] == '#' or line == '\n':
            continue
        if line[0] == '>':
            current_part_of_speech = line.strip('> ').strip()
            continue

        current_word = line.strip()
        word_repr = current_word+' - '+current_part_of_speech

        if word_repr not in existing_words:
            definitions = w.word_get_definitions(current_word)
            if not definitions or translate(current_part_of_speech) not in set([word['partOfSpeech'] for word in definitions]):
                no_definitions_list.append(current_word)
                continue

            if not os.path.exists(outdir+current_part_of_speech+'.txt'):
                print "\nCreating ["+current_part_of_speech+"] file....\n"
                open(outdir+current_part_of_speech+'.txt', 'w')

            definition_list = []
            for definition in [d for d in definitions if d['partOfSpeech'] == translate(current_part_of_speech)]:
                definition_list.append(definition['text'])
            with open(outdir+current_part_of_speech+'.txt', 'a') as f:
                f.write("******\n")
                f.write("word: "+definition['word']+"\n")
                f.write("part of speech: "+current_part_of_speech+"\n")
                f.write("definitions:\n")
                for d in definition_list:
                    f.write(d.encode('utf-8')+"\n")
            existing_words.add(word_repr)
            print "Wrote <"+word_repr+"> to "+current_part_of_speech+".txt."
        else:
            print "Not adding <"+word_repr+">"


except IOError, e:
    print e

open("data/existing", 'w').write(str(existing_words))

if no_definitions_list:
    print "\nNo definitions found for the following words:"
    for word in no_definitions_list: print word	