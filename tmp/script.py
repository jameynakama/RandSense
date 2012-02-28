# for parsing a words file


with open("words.txt") as f:
    words = f.read()

words = words.split("******")
words[0] = words[0].strip('\n')     # identifier, such as NOUN
for i in range(1, len(words)):
    words[i] = words[i].strip('\n').split('\n')
    for j in range(len(words[i])):
        words[i][j] = dict(words[i][j].split(': '))
        w = Word(words[i][j]).save()
