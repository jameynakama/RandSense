from sentences import Lexicon, Sentence


def foo(s):
    i = 0
    while True:
        i += 1
        print "\n{}: {}".format(i, s.get_sentence())
        if 'poop' in s.sentence:
            break

l = Lexicon()
s = Sentence(l)

def main():
    for i in range(20):
        print "\n{0}: {1}".format(i+1, s.get_sentence())

if __name__ == '__main__':
    main()