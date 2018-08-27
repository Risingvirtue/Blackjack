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
		self.players.append(Player()) #dealer
		for i in range(players):
			self.players.append(Player())
	def play(self):
		for player in self.players:
			player.hit(self.deck.deal())
		for player in self.players:
			player.hit(self.deck.deal())
	def shuffle(self):
		self.deck.shuffle()
		for player in self.players:
			player.clear()
	def playerMove(self):
		for i in range(1,len(self.players)):
			player = self.players[i]
			player.prevTotal = player.maxTotal()
			player.hit(self.deck.deal())
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
	def lastPlayerValue(self, player):
		if player + 1 >= len(self.players):
			return None
		else:
			return self.players[player + 1].prevTotal
	def dealerFaceUp(self):
		dealer = self.players[0]
		return min(dealer.hand[1].value, 10)
		
def saveInfo(fileName, winner, lastValue, dealerFaceUp):
	f=open(fileName, "r")
	dict = json.loads(f.read())
	key = str(lastValue) + "&" + str(dealerFaceUp)
	if (key not in dict):
		dict[key] = {"0": 0, "-1": 0, "1": 0}
	dict[key][str(winner)] += 1
	
	f = open(fileName,"w+")
	f.write(json.dumps(dict))
	f.close()
"""
f = open("blackjackHit.txt","w+")
f.write(json.dumps({}))
f.close()

f = open("blackjackStand.txt","w+")
f.write(json.dumps({}))
f.close()
"""
blackjack = Blackjack(1)
blackjack.shuffle()
"""
for i in range(100000):
	if i % 1000 == 0:
		print(i)
	blackjack.play()
	blackjack.playerMove()
	blackjack.dealerMove()
	winner = blackjack.winner()[0]
	standWinner = blackjack.standWinner()[0]
	lastValue = blackjack.lastPlayerValue(0)
	dealerFaceUp = blackjack.dealerFaceUp()
	
	
	saveInfo("blackjackHit.txt", winner, lastValue, dealerFaceUp)
	saveInfo("blackjackStand.txt", standWinner, lastValue, dealerFaceUp)
	blackjack.shuffle()

"""
blackjack = Blackjack(1)
blackjack.shuffle()

blackjack.play()
print("Dealer's face up is: ")
print(blackjack.players[0].hand[1])
while blackjack.players[1].maxTotal() < 21:
	yourTotal = blackjack.players[1].maxTotal()
	print("Your hand:")
	print(blackjack.players[1])
	print("Total: " + str(yourTotal))
	choice = input("Hit? Y or N:")
	if choice == "Y":
		blackjack.playerHit()
	else:
		break
if blackjack.players[1].maxTotal() > 21:
	print("Your hand:")
	print(blackjack.players[1])
	print("Busted, you lose")
else:
	blackjack.dealerMove()
	yourTotal = blackjack.players[1].maxTotal()
	dealerTotal = blackjack.players[0].maxTotal()
	print("Your hand: ")
	print(blackjack.players[1])
	print("Total: " + str(yourTotal))
	print("Dealer's hand: ")
	print(blackjack.players[0])
	print("Total: " + str(dealerTotal))
	if dealerTotal > 21:
		print("You Win!")
	elif yourTotal < dealerTotal:
		print("You lose!")
	elif yourTotal == dealerTotal:
		print("Push")
	else: 
		print("You Win!")
		
		
		
		
	




