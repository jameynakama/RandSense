grammar = {}

data = open('grammar.txt', 'r').read().split('\n')

for i in range(0, len(data)):
	data[i] = data[i].split(' -> ')

for element in data:
	grammar[element[0]] = []
	for item in element[1].split(' | '):
		grammar[element[0]].append(item.split(' '))

for key, value in grammar.iteritems():
	print "{k}: {v}".format(
		k=key,
		v=value,
		)