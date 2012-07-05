     _____           _ _____
    | __  |___ ___ _| |   __|___ ___ ___ ___
    |    -| .'|   | . |__   | -_|   |_ -| -_|
    |__|__|__,|_|_|___|_____|___|_|_|___|___|


RandSense v 0.5
===================

RandSense is a random sentence generator. It uses a context-free grammar to construct grammatically correct yet often silly and nonsensical sentences.

RandSense is built using the [SimpleNLG](http://code.google.com/p/simplenlg/) default lexicon, with some of my own modifications.

Usage
===================

    Usage: randsense.py [options]

    Options:
      -h, --help            show this help message and exit
      -n NUMBER, --number=NUMBER
                        define how many sentences to generate
      -g, --grammar         print grammar object before sentences
      -p, --pos             print 'part of speech' sentence with each sentence
      -t, --tech            print 'technical sentence' with each sentence
      -v, --verbose         prints all optional output; same as -gpt

Many thanks
===================

- [Antonio Zamora](http://www.scientificpsychic.com/az.html)
- [Adam Parrish](http://www.decontextualize.com/teaching/dwwp/topics-ii-recursion-and-context-free-grammars/)
- [SimpleNLG](http://code.google.com/p/simplenlg/)

To do list
===================

- Make weighted paths
- Add proper nouns
- Add negations
- Add commas, semicolons, colons
- Add more tenses
- Adjectives: comparative, superlative
- Make "Warriors engage" type constructions possible (right now the logic is in place only for "a warrior" or "the warriors")
- Determiners can have <singularorplural/> tag, so check for this and do a choice on the noun if so

Known bugs
===================

- Some questions are being "rendered" as statements
- 'else' is ending sentences sometimes
