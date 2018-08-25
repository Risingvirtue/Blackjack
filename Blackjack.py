import math
import random
class Suit:
	Diamond = 0
	Clover = 1
	Heart = 2
	Spade = 3
class Card:
	def __init__(self, value, suit):
		self.value = value;
		self.suit = suit;
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
		currStr += str(self.suit)
		return currStr
		
class Deck:
	def __init__(self):
		self.deck = []
		self.currCard = 0
		for i in range(1, 14):
			for j in range(4):
				self.deck.append(Card(i,j))
	def riffle(self):
		l = 0
		m = math.floor(len(self.deck) / 2)
		r = m
		newDeck = []
		while l < m or r < len(self.deck):
			if l >= m:
				newDeck.append(self.deck[r])
				r = r + 1
			elif r >= len(self.deck):
				newDeck.append(self.deck[l])
				l = l + 1
			else:
				if random.random() < 0.5:
					newDeck.append(self.deck[l])
					l += 1
				else:
					newDeck.append(self.deck[r])
					r += 1
		self.deck = newDeck
	def shuffle(self):
		for i in range(9):
			self.riffle()
	def __str__(self):
		currStr = []
		for card in self.deck:
			currStr.append(str(card))
		return str(currStr)

deck = Deck()
deck.shuffle()
print(deck)

