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
        self.numDecks = numDecks
		self.length = numDecks * 52
        self.setCut()
        self.count = 0
        print(str(self.cut))
		for k in range(numDecks):
			for i in range(1, 14):
				for j in range(4):
					self.deck.append(Card(i,j))
	def shuffle(self):
		random.shuffle(self.deck)
		self.index = 0
        self.count = 0
        self.setCut()
    def setCut(self):
        self.cut = floor(self.numDecks - random.random() - 1) * 52)
	def __str__(self):
		currStr = []
		for card in self.deck:
			currStr.append(str(card))
		return str(currStr)
	def deal(self):
		card = self.deck[self.index]
        self.cardCount(card)
		self.index = self.index + 1
		return card
    def cardCount(self, card):
		value = card.value
		if value <= 6 and value >= 2:
			self.count = self.count + 1
		elif value >= 10 or value == 1:
			self.count = self.count - 1
class Player:
	def __init__(self):
		self.hand = []
		self.prevTotal = 0
		self.bet = 10
		self.money = 0
		self.multiplier = 1
        self.hands = []
	def changeBet(self, amount):
		self.bet = amount
	def resetMoney(self, amount):
		self.money = amount
	def updateMoney(self, sign):
		self.money += self.multiplier * self.bet * sign
	def total(self, hand=self.hand):
		total = 0
		hasAce = False
		for card in hand:
			if card.value == 1:
				hasAce = True
			total += min(card.value, 10)
		if hasAce:
			return [total, total + 10]
		return [total]
	def hit(self, card, hand=-1):
        if hand != -1:
            self.hands[hand].append(card)
        else:
            self.hand.append(card)
	def clear(self):
		self.hand = []
        self.hands = []
	def __str__(self):
		handArr = []
		for card in self.hand:
			handArr.append(str(card))
		return str(handArr)
	def hasAce(self, hand):
		for card in hand:
			if card.value == 1:
				return true
		return false
    def canSplit(self):
        return self.hand.length == 2 and self.hand[0].value == self.hand[1].value
	def maxTotal(self):
		total = self.total()
		currMax = max(total)
		if (currMax > 21):
			return min(total)
		else:
			return currMax
	def isBusted(self):
		return self.maxTotal() > 21
    def play(self, faceUp, deck):
        currHand = self.hand
        currIndex = -1
        while True:
            strategy = self.basicStrategy(currHand, faceUp, deck)
            if strategy == 'Split':
                newHand = [currHand.pop()]
                currHand.append(deck.deal())
                newHand.append(deck.deal())
                self.hands.append(newHand)
            elif strategy == 'Hit':
                currHand.append(deck.deal())
            elif strategy == 'Stand':
                if self.hands.length() == currIndex + 1:
                    return
                else:
                    currIndex += 1
                    currHand = self.hands[currIndex]
    def basicStrategy(self, hand, faceUp, deck):
        if self.canSplit():
            if hand[0].value == 2 or \
               hand[0].value == 3 or \
               hand[0].value == 7:
                if faceUp.value <= 7:
                    return 'Split'
                else:
                    return 'Hit'
                    
            elif hand[0].value == 4:
                if faceUp.value == 5 or faceUp.value == 6:
                    return 'Split'
                else:
                    return 'Hit'
            elif hand[0].value == 6:
                if faceUp.value <= 6:
                    return 'Split'
                else:
                    return 'Hit'
            elif hand[0].value == 8 or hand[0].value == 1:
                return 'Split'
            else:
                return 'Stand'
        elif self.hasAce(hand):
            
        
class Blackjack:
	def __init__(self, players):
		self.deck = Deck(6)
		self.count = 0
		self.players = []
		self.players.append(Player()) #dealer
		for i in range(players):
			self.players.append(Player())
	def deal(self):
		self.clearHands()
		if self.deck.index > self.deck.cut:
			self.deck.shuffle()
		for i in range(len(self.players)):
            for j in range(2): '''deal two cards'''
                player = self.players[i]
                card = self.deck.deal()
                player.hit(card)
                if i != 0 or j == 0: '''start counting all face up cards'''
                    self.deck.cardCount(card)
	def clearHands(self):
		for player in self.players:
			player.clear()
	def playerMove(self):
		for i in range(1,len(self.players)):
			player = self.players[i]
			player.prevTotal = player.maxTotal()
			card = self.deck.deal()
			player.hit(card)
	def normal(self):
		for i in range(1,len(self.players)):
			player = self.players[i]
			
			if self.count > 6:
				player.multiplier = 2
			elif self.count < -3:
				player.multiplier = 0.5
			else:
				player.multiplier = 1
			
			while (not player.isBusted() and player.maxTotal() < 17):
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
				player.updateMoney(-1)
			elif (dealerValue > 21):
				winners.append(1)
				player.updateMoney(1)
			elif playerValue < dealerValue:
				winners.append(-1)
				player.updateMoney(-1)
			elif playerValue == dealerValue:
				winners.append(0)
			else:
				winners.append(1)
				player.updateMoney(1)
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
	def trueCount(self):
		cardCount = round(self.count * 52 / (self.deck.length - self.deck.index))
		return cardCount
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

def winRate(blackjack, method, times):
	blackjack.shuffle()
	wins = 0
	ties = 0
	losses = 0
	for i in range(times):
		blackjack.deal()
		method()
		blackjack.dealerMove()
		result = blackjack.result()
		if result["winner"] == 1:
			wins += 1
		elif result["winner"] == 0:
			ties += 1
		else:
			losses += 1
			
	print("win: " + str(wins * 100 /times) + "%")
	print("tie: " + str(ties * 100 /times) + "%")
	print("lose: " + str(losses * 100 /times) + "%")

def money(blackjack, method, times):
	blackjack.shuffle()
	player = blackjack.players[1]
	for i in range(times):
		blackjack.deal()
		method()
		blackjack.dealerMove()
		result = blackjack.result()
		
		if player.money <= 0:
			#print("Loss at " + str(i) + " wins.")
			return False
	#print("Player total $" + str(player.money))
	return True
			
def numberOfGames(blackjack, method):
	count = 0
	player = blackjack.players[1]
	player.resetMoney(10000)
	while (player.money > 0 and count < 100000):
		blackjack.deal()
		method()
		blackjack.dealerMove()
		blackjack.winner()
		count += 1
	print(count)
