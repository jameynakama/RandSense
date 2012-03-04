import os
import xml.etree.ElementTree as xml

def main():
	data = xml.parse(os.path.join('data/dictionary/default-lexicon.xml'))
	root = data.getroot()

	dictionary = {}
	for word in root:
		word_dict = {}
		for line in word:
			word_dict[line.tag] = line.text
		dictionary.update({word[0].text: word_dict})

	return dictionary

if __name__ == '__main__':
	main()