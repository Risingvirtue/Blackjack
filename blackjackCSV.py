import json
def csvConvert(fileName, saveFile):
	f = open(fileName,"r")
	dict = json.loads(f.read())
	contents = ""
	for pair in dict:
		combo = pair.split('&')
		contents += combo[0] + ',' + combo[1] + ',' + combo[2]
		contents += ',' + str(dict[pair]["0"])
		contents += ',' + str(dict[pair]["-1"])
		contents += ',' + str(dict[pair]["1"])
		contents += '\n'
	saveFile = open(saveFile, "w+")
	saveFile.write(contents)
	saveFile.close()
def csvCombine(file1, file2, saveFile):
	f = open(file1,"r")
	dict = json.loads(f.read())
	f2 = open(file2, "r")
	dict2 = json.loads(f2.read())
	contents = ""
	for pair in dict:
		combo = pair.split('&')
		contents += combo[0] + ',' + combo[1] + ',' + combo[2]
		contents += ',' + str(dict[pair]["0"])
		contents += ',' + str(dict[pair]["-1"])
		contents += ',' + str(dict[pair]["1"])
		contents += ',' + str(dict2[pair]["0"])
		contents += ',' + str(dict2[pair]["-1"])
		contents += ',' + str(dict2[pair]["1"]) 
		contents += '\n'
	saveFile = open(saveFile, "w+")
	saveFile.write(contents)
	saveFile.close()
#csvConvert("blackjackHitCount.txt", "hitCSVCount.csv")
#csvConvert("blackjackStandCount.txt", "standCSVCount.csv")
csvCombine("blackjackHitCount.txt", "blackjackStandCount.txt", "combineCount.csv")
