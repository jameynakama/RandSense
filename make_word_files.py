import os
import wordnik

# make repeats not happen

API_KEY = "1081e3eed25591267a10307da5c01c675d1d199db0e2d7c3f"

infile = "word_list.txt"
outdir = "data/words/"

w = wordnik.Wordnik(API_KEY)

no_definitions_list = []
try:
    current_part_of_speech = ''
    for line in open(infile, 'r'):
        if line[0] == '#' or line == '\n':
            continue
        if line[0] == '>':
            current_part_of_speech = line.strip('> ').strip().lower()
            continue

        # here is where we check for existing words with the same part of speech
        # if they exist, then we don't make an API call 
        data = ''
        if current_part_of_speech == 'article':
            potential_files = ['definite-article.txt', 'indefinite-article.txt']
            for filename in potential_files:
                if os.path.exists(outdir+filename):
                    data += open(outdir+filename, 'r').read()
        elif current_part_of_speech == 'verb':
            potential_files = ['verb-transitive.txt', 'verb-intransitive.txt', 'phrasal-verb.txt']
        else:
            potential_files = [current_part_of_speech+'.txt']

        for filename in potential_files:
            if os.path.exists(outdir+filename):
                data += open(outdir+filename, 'r').read()

        if "word: "+line.strip() in data:
            print "Not searching for "+line.strip()+"."
            continue

        # when making the dictionary files, make a definitions: ['def1', 'def2', 'def3',] type structure
        # and then match this in the DictionaryParser

        definitions = w.word_get_definitions(line.strip())
        if not definitions:
            no_definitions_list.append(line.strip())
            continue

        if not os.path.exists(outdir+definitions['partOfSpeech']+".txt"):
            print "\nCreating {0} file...\n".format(definition['partOfSpeech'].upper())
            open(outdir+definition['partOfSpeech']+".txt", 'w')

        # NOW, right here we check for file and make it if needed, and we write the 
        # word and part of speech and set up the definitions. then, in the loop, we add
        # each definition to the new list
        for definition in definitions:
            if current_part_of_speech not in definition['partOfSpeech']:
                continue
            # if not os.path.exists(outdir+definition['partOfSpeech']+".txt"):
            #     print "\nCreating {0} file...\n".format(definition['partOfSpeech'].upper())
            #     open(outdir+definition['partOfSpeech']+".txt", 'w')
            # if 'word: {0}\npart_of_speech: {1}\ndefinition: {2}'.format(
            #     definition['word'].encode('utf-8'),
            #     definition['partOfSpeech'].encode('utf-8'),
            #     definition['text'].encode('utf-8'),
            #     ) in open(outdir+definition['partOfSpeech']+".txt").read():
            #     print "Skipping '{0} - {1}'...".format(definition['word'], definition['partOfSpeech'])
            #     continue
            with open(outdir+definition['partOfSpeech']+".txt", 'a') as f:
                f.write("******\n")
                f.write("word: " + definition['word'].encode('utf-8') + '\n')
                f.write("part_of_speech: "+definition['partOfSpeech'].encode('utf-8') + '\n')
                f.write("definition: "+definition['text'].encode('utf-8') + '\n')
                # if 'verb' in definition['partOfSpeech']:
                #     f.write("i: \n")
                #     f.write("you: \n")
                #     f.write("it: \n")
                #     f.write("we: \n")
                #     f.write("they: \n")
                print "Added '{0}' to '{1}.txt'.".format(
                    definition['word'].encode('utf-8'),
                    definition['partOfSpeech'].upper(),
                    )
except IOError, e:
    print e

if no_definitions_list:
    print "\nNo definitions found for the following words:"
    for word in no_definitions_list: print word
