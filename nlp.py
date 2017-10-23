
import re

file = open('mc.txt','r')
output = open('part2.txt','w')
line = file.readline()
while line:
	line = line.decode('utf-8')
	if (len(line) > 5):
		while (line.find(':') != -1):
			pos = line.find(':')
			line = line[pos + 1:]
		
		data = re.split('\s',line)
		r = []
		for i in range(0, len(data)):
			r.append(i)
		r.reverse()
		for i in r:
			if (re.search('^[A-Za-z,.\s\']+$', data[i]) != None or len(data[i]) == 0 or re.search('.com', data[i]) != None):
				del data[i]
		if len(data) > 0:
			data = '\n'.join(data) + '\n'
			output.write(data.encode('utf-8'))
	line = file.readline()