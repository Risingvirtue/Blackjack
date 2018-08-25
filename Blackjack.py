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
		self.index = 0
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
		self.index = 0
	def __str__(self):
		currStr = []
		for card in self.deck:
			currStr.append(str(card))
		return str(currStr)
	def deal(self):
		if self.index >= len(self.deck):
			return None
		card = self.deck[self.index]
		self.index = self.index + 1
		return card
		
class Player:
	def __init__(self):
		self.hand = []
		self.prevTotal = 0
	def total(self):
		total = 0
		hasAce = False
		for card in self.hand:
			if card.value == 1:
				hasAce = True
			total += min(card.value, 10)
		if hasAce:
			return [total, total + 10]
		return [total]
	def hit(self, card):
		self.hand.append(card)
	def clear(self):
		self.hand = []
	def __str__(self):
		handArr = []
		for card in self.hand:
			handArr.append(str(card))
		return str(handArr)
	def hasAce(self):
		for card in self.hand:
			if card.value == 1:
				return true
		return false
	def maxTotal(self):
		total = self.total()
		
		currMax = max(total)
		if (currMax > 21):
			return min(total)
		else:
			return currMax
		
class Blackjack:
	def __init__(self, players):
		self.deck = Deck()
		self.players = []
		self.players.append(Player())
		for i in range(players):
			self.players.append(Player())
	def play(self):
		for player in self.players:
			player.hit(self.deck.deal())
		for player in self.players:
			player.hit(self.deck.deal())
	def shuffle(self):
		self.deck.shuffle()
	def playerMove(self):
		for i in range(1,len(self.players)):
			player = self.players[i]
			player.prevTotal = player.total()
			if random.random() < 0.5:
				player.hit(self.deck.deal())	
	def dealerMove(self):
		dealer = self.players[0]
		while dealer.maxTotal() < 17:
			dealer.hit(self.deck.deal())
		print(dealer.maxTotal())
		print(dealer)
	def winner(self):
		dealerValue = self.players[0].maxTotal()
		winners = []
		for i in range(1, len(self.players)):
			player = self.players[i]
			print(player)
			playerValue = player.maxTotal()
			if (playerValue > 21):
				winners.append(-1)
			elif (playerValue < dealerValue):
				winners.append(-1)
			elif (playerValue == dealerValue):
				winners.append(0)
			else:
				winners.append(1)
		return winners
	def lastValue(self, player):
		if player >= len(self.players):
			return None
		else:
			return self.players[player].prevTotal
		
blackjack = Blackjack(1)
blackjack.shuffle()

blackjack.play()
blackjack.playerMove()
blackjack.dealerMove()
blackjack.winner()







