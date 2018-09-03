import math
import random
import json
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
	def __init__(self, numDecks):
		self.deck = []
		self.index = 0
		self.length = numDecks * 52
		for k in range(numDecks):
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
		random.shuffle(self.deck)
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
	def isBusted(self):
		return maxTotal > 21
class Blackjack:
	def __init__(self, players):
		self.deck = Deck(6)
		self.count = 0
		self.players = []
		self.players.append(Player()) #dealer
		for i in range(players):
			self.players.append(Player())
	def cardCount(self, card):
		value = card.value
		if value <= 6 and value >= 2:
			self.count = self.count + 1
		elif value >= 10 or value == 1:
			self.count = self.count - 1
	def deal(self):
		self.clearHands()
		if self.deck.index > len(self.deck.deck) / 2:
			self.shuffle()
		for i in range(len(self.players)):
			player = self.players[i]
			card = self.deck.deal()
			player.hit(card)
			if i != 0:
				self.cardCount(card)
		for player in self.players:
			card = self.deck.deal()
			player.hit(card)
			self.cardCount(card)
	def shuffle(self):
		self.deck.shuffle()
		self.count = 0
	def clearHands(self):
		for player in self.players:
			player.clear()
	def playerMove(self):
		for i in range(1,len(self.players)):
			player = self.players[i]
			player.prevTotal = player.maxTotal()
			card = self.deck.deal()
			player.hit(card)
	def playerHit(self):
		player = self.players[1]
		player.hit(self.deck.deal())
	def dealerMove(self):
		dealer = self.players[0]
		while dealer.maxTotal() < 17:
			dealer.hit(self.deck.deal())
	def winner(self):
		dealerValue = self.players[0].maxTotal()
		winners = []
		for i in range(1, len(self.players)):
			player = self.players[i]
			playerValue = player.maxTotal()
			if (playerValue > 21):
				winners.append(-1)
			elif (dealerValue > 21):
				winners.append(1)
			elif playerValue < dealerValue:
				winners.append(-1)
			elif playerValue == dealerValue:
				winners.append(0)
			else:
				winners.append(1)
		return winners
	def standWinner(self):
		dealerValue = self.players[0].maxTotal()
		winners = []
		for i in range(1, len(self.players)):
			player = self.players[i]
			playerValue = player.prevTotal
			if dealerValue > 21:
				winners.append(1)
			if playerValue < dealerValue:
				winners.append(-1)
			elif playerValue == dealerValue:
				winners.append(0)
			else:
				winners.append(1)
		return winners
	def countDealer(self):
		dealer = self.players[0]
		self.cardCount(dealer.hand[0])
		player = self.players[1]
		for i in range(2, len(player.hand)):
			self.cardCount(player.hand[i])
	def lastPlayerValue(self, player):
		if player + 1 >= len(self.players):
			return None
		else:
			return self.players[player + 1].prevTotal
	def dealerFaceUp(self):
		dealer = self.players[0]
		return min(dealer.hand[1].value, 10)
	def dealerFaceDown(self):
		dealer = self.players[0]
		return min(dealer.hand[0].value, 10)
	def play(self):
		self.deal()
		self.playerMove()
		if not self.players[1].isBusted:	
			blackjack.dealerMove()
	def result(self):
		cardCount = round(self.count * 52 / (self.deck.length - self.deck.index))
		self.countDealer();
		return {"winner": self.winner()[0], 
				"standWinner": self.standWinner()[0], 
				"lastValue": self.lastPlayerValue(0), 
				"dealerFaceUp": self.dealerFaceUp(),
				"cardCount": cardCount}
	def __str__(self):
		print("Dealer: ")
		print(self.players[0])
		print(self.players[0].maxTotal())
		print("Player: ")
		print(self.players[1])
		print(self.players[1].maxTotal())
		return ""
		
def saveInfo(fileName, arr):
	f=open(fileName, "r")
	dict = json.loads(f.read())
	for result in arr:
		key = ""
		if "count" in result:
			key = str(result["lastValue"]) + "&" + str(result["dealerFaceUp"]) + "&" + str(result["count"])
		else:
			key = str(result["lastValue"]) + "&" + str(result["dealerFaceUp"])
		if (key not in dict):
			dict[key] = {"0": 0, "-1": 0, "1": 0}
		dict[key][str(result["winner"])] += 1
	f = open(fileName,"w+")
	f.write(json.dumps(dict))
	f.close()
def wipeSaves():
	f = open("blackjackHitCount.txt","w+")
	f.write(json.dumps({}))
	f.close()

	f = open("blackjackStandCount.txt","w+")
	f.write(json.dumps({}))
	f.close()

def runPlays(times):
	blackjack = Blackjack(1)
	blackjack.shuffle()
	standArr = []
	hitArr = []
	for i in range(times):
		if i % 100000 == 0:
			print(i)
			saveInfo("blackjackHit.txt", hitArr)
			saveInfo("blackjackStand.txt", standArr)
			standArr = []
			hitArr = []
		blackjack.deal()
		blackjack.playerMove()
		blackjack.dealerMove()
		winner = blackjack.winner()[0]
		standWinner = blackjack.standWinner()[0]
		lastValue = blackjack.lastPlayerValue(0)
		dealerFaceUp = blackjack.dealerFaceUp()
		standArr.append({"winner": standWinner, "lastValue": lastValue, "dealerFaceUp": dealerFaceUp})
		hitArr.append({"winner": winner, "lastValue": lastValue, "dealerFaceUp": dealerFaceUp})
		blackjack.shuffle()
	saveInfo("blackjackHit.txt", hitArr)
	saveInfo("blackjackStand.txt", standArr)
def runCount(times):
	blackjack = Blackjack(1)
	blackjack.shuffle()
	standArr = []
	hitArr = []
	maxCount = 0
	for i in range(times):
		if i % 100000 == 0:
			print(i)
			saveInfo("blackjackHitCount.txt", hitArr)
			saveInfo("blackjackStandCount.txt", standArr)
			standArr = []
			hitArr = []
		blackjack.play()
		result = blackjack.result()
		standArr.append({"winner": result["standWinner"], 
						"lastValue": result["lastValue"], 
						"dealerFaceUp": result["dealerFaceUp"],
						"count": result["cardCount"]})
		hitArr.append({"winner": result["winner"], 
						"lastValue": result["lastValue"], 
						"dealerFaceUp": result["dealerFaceUp"],
						"count": result["cardCount"]})
	saveInfo("blackjackHitCount.txt", hitArr)
	saveInfo("blackjackStandCount.txt", standArr)
	

	
	


		
		
		
	




