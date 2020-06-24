import math
import random
import time
class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
    def __str__(self):
        currStr = ""
        if self.value == 1:
            currStr += "A"
        elif self.value == 11:
            currStr += "J"
        elif self.value == 12:
            currStr += "Q"
        elif self.value == 13:
            currStr += "K"
        else:
            currStr += str(self.value)
        if self.suit == 0:
            currStr += " Diamonds"
        elif self.suit == 1:
            currStr += " Clubs"
        elif self.suit == 2:
            currStr += " Hearts"
        else: 
            currStr += " Spades"
        return currStr
class Deck:
    def __init__(self, numDecks = 2):
        self.deck = []
        self.index = 0
        self.numDecks = numDecks
        self.length = numDecks * 52
        self.setCut()
        self.count = 0
        self.sideBetCount = 0
        for k in range(numDecks):
            for i in range(1, 14):
                for j in range(4):
                    self.deck.append(Card(i, j))
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
        self.sideBetCount = 0
    def setCut(self):
        multiplier = 0.9
        if self.numDecks == 6:
            multiplier = 1.5
        elif self.numDecks == 2:
            multiplier = 0.8
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
        self.kingsBounty(card)
        #self.zenCount(card)
        #self.KOCount(card)
        #self.omegaII(card)
    def hiLo(self, card):
        value = card.value
        if value >= 2 and value <= 6:
            self.count = self.count + 1
        elif value >= 10 or value == 1:
            self.count = self.count - 1
    def zenCount(self, card):
        value = card.value
        if value == 2 or value == 3 or value == 7:
            self.count += 1
        elif value == 4 or value == 5 or value == 6:
            self.count += 2
        elif value >= 10:
            self.count -= 2
        elif value == 1:
            self.count -= 1
    def KOCount(self, card):
        value = card.value
        if value <= 7 and value >= 2:
            self.count += 1
        elif value >= 10 or value == 1:
            self.count -= 1
    def omegaII(self, card):
        value = card.value
        if value == 7 or value == 2 or value == 3:
            self.count += 1
        elif value >= 10:
            self.count -= 2
        elif value == 4 or value == 5 or value == 6:
            self.count += 2
        elif value == 9:
            self.count -= 1
    def kingsBounty(self, card):
        value = card.value
        suit = card.suit
        if value == 13:
            if suit == 3:
                self.sideBetCount -= 6
            else:
                self.sideBetCount -= 2
        elif value >= 10:
            self.sideBetCount -= 2
        else:
            self.sideBetCount += 1
        #print('count card: ' + str(card) + ' ' + str(self.sideBetCount))
    def getTrueCount(self):
        #return self.trueCountTable[self.count + 30][self.index]
        trueCount = math.floor(self.count * 52 / (self.length - self.index))
        return trueCount
    def getSideBetTrueCount(self):
        trueCount = math.floor(self.sideBetCount * 52 / (self.length - self.index))
        return trueCount