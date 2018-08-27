import json
def csvConvert(fileName, saveFile):
	f = open(fileName,"r")
	dict = json.loads(f.read())
	contents = ""
	for pair in dict:
		combo = pair.split('&')
		contents += combo[0] + ',' + combo[1]
		contents += ',' + str(dict[pair]["0"])
		contents += ',' + str(dict[pair]["-1"])
		contents += ',' + str(dict[pair]["1"])
		contents += '\n'
	saveFile = open(saveFile, "w+")
	saveFile.write(contents)
	saveFile.close()
	
csvConvert("blackjackHit.txt", "hitCSV.csv")
