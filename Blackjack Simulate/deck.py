import math
import random
import time
class Deck:
    def __init__(self, numDecks = 2):
        self.deck = []
        self.index = 0
        self.numDecks = numDecks
        self.length = numDecks * 52
        self.setCut()
        self.count = 0
        for k in range(numDecks):
            for i in range(1, 14):
                for j in range(4):
                    card = i
                    if i >= 10:
                        card = 10 
                    self.deck.append(card)
        #self.generateTrueCountTable()
    def generateTrueCountTable(self):
        trueCountTable = []
        for i in range(60):
            count = i - 30
            countRow = []
            for j in range(self.length):
                countRow.append(math.floor(count * 52 / (self.length - j)))
            trueCountTable.append(countRow)
        self.trueCountTable = trueCountTable
    def shuffle(self):
        random.shuffle(self.deck)
        self.index = 0
        self.count = 0
    def setCut(self):
        multiplier = 0.9
        if self.numDecks == 6:
            multiplier = 1.5
        elif self.numDecks == 2:
            multiplier = 0.9
        elif self.numDecks == 1:
            multiplier = 0.5
        self.cut = math.floor((self.numDecks - multiplier) * 52)
    def __str__(self):
        currStr = []
        for card in self.deck:
            currStr.append(str(card))
        return str(currStr)
    def deal(self):
        card = self.deck[self.index]
        self.cardCount(card)
        self.index += 1
        return card
    def cardCount(self, card):
        self.hiLo(card)
        #self.zenCount(card)
        #self.KOCount(card)
        #self.omegaII(card)
    def hiLo(self, card):
        value = card
        if value >= 2 and value <= 6:
            self.count = self.count + 1
        elif value >= 10 or value == 1:
            self.count = self.count - 1
    def zenCount(self, card):
        value = card
        if value == 2 or value == 3 or value == 7:
            self.count += 1
        elif value == 4 or value == 5 or value == 6:
            self.count += 2
        elif value >= 10:
            self.count -= 2
        elif value == 1:
            self.count -= 1
    def KOCount(self, card):
        value = card
        if value <= 7 and value >= 2:
            self.count += 1
        elif value >= 10 or value == 1:
            self.count -= 1
    def omegaII(self, card):
        value = card
        if value == 7 or value == 2 or value == 3:
            self.count += 1
        elif value >= 10:
            self.count -= 2
        elif value == 4 or value == 5 or value == 6:
            self.count += 2
        elif value == 9:
            self.count -= 1 
    def getTrueCount(self):
        #return self.trueCountTable[self.count + 30][self.index]
        trueCount = math.floor(self.count * 52 / (self.length - self.index))
        return trueCount