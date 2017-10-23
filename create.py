#coding:utf-8
import re
import math
import nltk
import jieba.posseg as posseg
import xpinyin
import random
import copy

myRythem = 'ang'	# 韵脚
myLength = 20	# 歌词句数
neighbour = 10	# 相邻加入特征的个数
hitPara = 20	# 选中概率[0-40]
keyWord = "生命"	# 关键词
keyWordPercentage = 0.9 # 关键词相关比例（0-1）
keyWordRythemPercentage = 0 # 关键词相关句中，符合韵律的比例
keyWordNeighbour = 2 # 关键词相邻区间
final = []
file = open('part1.txt', 'r')
backFile = open('part2.txt', 'r')
resource = []
backResource = []
total = []
for line in file:
	resource.append(line.strip())
	total.append(line.strip())
for line in backFile:
	backResource.append(line.strip())
	total.append(line.strip())

def randExclued(l):
	index = random.randint(0, len(l) - 1)
	tmp = copy.deepcopy(l[index])
	del l[index]
	return tmp

def getAns(rList, kList):
	tmp = []
	for i in xrange(0, myLength):
		if (random.randint(0,100) < keyWordPercentage):
			tmp.append(randExclued(kList))
		else:
			tmp.append(randExclued(rList))
	return tmp

def getLastword(word):
	try:
		tmp = unicode(word[-3:], 'utf-8')
		return (tmp,word[-3:])
	except Exception, e:
		try:
			tmp = unicode(word[-5:-2], 'utf-8')
			return (tmp, word[-5:-2])
		except Exception, e:
			return ('','')

pinyinGenerator = xpinyin.Pinyin()
def getRythem(word):
	tmp, w = getLastword(word)
	if w == '':
		return ('','')
	std = pinyinGenerator.get_pinyin(tmp)
	stm = pinyinGenerator.get_pinyin(tmp, show_tone_marks=True)
	for i in xrange(len(std)):
		if std[i] != stm[i]:
			return (std[i:],w)
	if len(std) == 2:
		return (std[1:],w)
	elif len(std) == 3 or len(std) == 4:
		return (std[-2:],w)
	else:
		return (std[-3:],w)

def getDist(resource):
	feq = []
	lastWord = ''
	for i in xrange(len(resource)):
		tmpRythem, lastWord = getRythem(resource[i])
		if  tmpRythem == myRythem:
			for j in xrange(neighbour):
				if i + j >= 0 and i + j < len(resource):
					feq.append(getRythem(resource[i + j])[1])
				if i - j >= 0 and i - j < len(resource):
					feq.append(getRythem(resource[i - j])[1])
	return nltk.FreqDist(feq).most_common()

def getLegalLuckone(waitList):
	luckyOne = random.choice(waitList)
	hashCount = 0
	while (hash(luckyOne) in hashList.keys()):
		hashCount += 1
		luckyOne = random.choice(waitList)
		if (hashCount > 5):
			raise Exception('需要重做')
	hashList[hash(luckyOne)] = True
	return luckyOne

freqDist = getDist(resource)
backFreqDist = getDist(backResource)
rythemOutput = []
hashList = {}
cycleTime = 0
while (cycleTime < myLength):
	cycleTime += 1
	if random.randint(0,10) <= 4:
		choosedDist = backFreqDist
		choosedResource = backResource
	else:
		choosedDist = freqDist
		choosedResource = resource
	for key, value in choosedDist:
		if (random.randint(0,100) <= hitPara):
			lastWord = key
			break
	waitList = []
	for i in xrange(len(choosedResource)):
		_, tmpWord = getLastword(choosedResource[i])
		if (tmpWord == lastWord):
			waitList.append(choosedResource[i])
	try:	
		luckyOne = getLegalLuckone(waitList)
	except Exception,e :
		cycleTime -= 1
		continue
	rythemOutput.append(luckyOne)
	# sentStruct = posseg.cut(luckyOne)
	# for k,v in sentStruct:
	# 	print '(' + k + ' , ' + v + ')' + ' ',
	# print

def st_norm(offset, sigma = 0.6):
	return (1.0/((2 * math.pi)**0.5 * sigma)) * (math.e**(-1.0 * (offset)**2/(2.0 * sigma**2)))

distribute = [st_norm(t) for t in xrange(0 - keyWordNeighbour, keyWordNeighbour + 1)]
distributeSum = sum(distribute)
def keyWordWeight(i, j):
	return int(math.ceil(distribute[j - i + keyWordNeighbour] / distributeSum * 100))

rythemKeywordList = []
keyWordFeature = []
for i in xrange(0, len(total)):
	if total[i].find(keyWord) != -1:
		for j in xrange(i - keyWordNeighbour, i + keyWordNeighbour + 1):
			try:
				for item, seg in posseg.cut(total[j]):
					if seg in ['a','n','vn']:
						keyWordFeature.append(item)
			except Exception,e :
				print 'error : ' + total[j]
				print e
			if getRythem(total[i])[0] == myRythem:
				rythemKeywordList.append(total[i])
keyWordFeature = [i[0] for i in nltk.FreqDist(keyWordFeature).most_common(5)]
keyWordList = []
for i in xrange(0, len(total)):
	 for tmpKeyWord in keyWordFeature:
		if unicode(total[i],'utf-8').find(tmpKeyWord) != -1:
			for j in xrange(i - keyWordNeighbour, i + keyWordNeighbour + 1):
				try:
					keyWordList.append([total[j], keyWordWeight(i, j)])
				except Exception,e :
					print 'error : ' + total[j]
					print e

def getRamdomByWeight(weightList):
	tmp = []
	for i in xrange(0, len(weightList)):
		for t in xrange(0, weightList[i][1]):
			tmp.append(i)
	return random.choice(tmp)

cycleTime = 0
onlyKeyWord = False
keyWordOutput = []
while (cycleTime < myLength):
	cycleTime += 1
	if (not onlyKeyWord and random.randint(0,100) <= keyWordRythemPercentage * 100):
		keyWordOutput.append(randExclued(rythemKeywordList))
		if len(rythemKeywordList) == 0:
			onlyKeyWord = True
	else:
		index = getRamdomByWeight(keyWordList)
		keyWordOutput.append(copy.deepcopy(keyWordList[index][0]))
		del keyWordList[index]

final = getAns(rythemOutput, keyWordOutput)
for i in final:
	print i
