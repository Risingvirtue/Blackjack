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
		self.hand = [[]]
		self.prevTotal = 0
		self.bet = 10
		self.money = 0
		self.multiplier = 1
        self.bets = [self.bet * self.multiplier]
	def changeBet(self, amount):
		self.bet = amount
	def resetMoney(self, amount):
		self.money = amount
	def updateMoney(self, sign):
		self.money += self.multiplier * self.bet * sign
	def getTotal(self, hand=self.hand):
		total = 0
		hasAce = False
		for card in hand:
			if card.value == 1:
				hasAce = True
			total += min(card.value, 10)
		if hasAce:
            if total + 10 > 21:
                return [total]
            else:  
                return [total, total + 10]
		return [total]
	def hit(self, card, hand=0):
        if hand != 0:
            self.hands[hand].append(card)
        else:
            self.hand.append(card)
	def clear(self):
		self.hand = [[]]
        self.bets = [self.multiplier * self.bet]
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
	def isBusted(self):
		return self.maxTotal() > 21
    def play(self, faceUp, deck):
        currHand = self.hand[0]
        currIndex = 0
        while True:
            strategy = self.basicStrategy(currHand, faceUp.value)
            if strategy == 'Split':
                newHand = [currHand.pop()]
                currHand.append(deck.deal())
                newHand.append(deck.deal())
                self.hand.append(newHand)
            elif strategy == 'Hit':
                currHand.append(deck.deal())
            elif strategy == 'Double':
                currHand.append(deck.deal())
                self.bets[currIndex] *= 2
            elif strategy == 'Stand':
                if self.hand.length() == currIndex:
                    return
                else:
                    currIndex += 1
                    currHand = self.hands[currIndex]
    def basicStrategy(self, hand, faceUp):
        total = self.getTotal()
        if self.canSplit() and hand[0].value != 5:
            if hand[0].value == 2 or \
               hand[0].value == 3 or \
               hand[0].value == 7:
                if faceUp <= 7 and faceUp != 1:
                    return 'Split'
                else:
                    return 'Hit'
                    
            elif hand[0].value == 4:
                if faceUp == 5 or faceUp == 6:
                    return 'Split'
                else:
                    return 'Hit'
            elif hand[0].value == 6:
                if faceUp <= 6 and faceUp != 1:
                    return 'Split'
                else:
                    return 'Hit'
            elif hand[0].value == 8 or hand[0].value == 1:
                return 'Split'
            elif hand[0].value == 9:
                if faceUp == 7 or faceUp >= 10 or faceUp == 1:
                    return 'Stand'
                else:
                    return 'Split'
        elif total.length() == 2: #has an ace and soft
            canDouble = hand.length() == 2
            if total[1] >= 19:
                return 'Stand'
            elif total[1] == 18:
                if faceUp == 2 or faceUp == 7 or faceUp == 8:
                    return 'Stand'
                elif faceUp >= 3 and faceUp <=6:
                    return 'Double' if canDouble else 'Stand'
                else:
                    return 'Hit'
            elif total[1] == 17:
                if faceUp >= 3 and faceUp <= 6:
                    return 'Double' if canDouble else 'Hit'
                else:
                    return 'Hit'
            elif total[1] == 16 or total[1] == 15:
                if faceUp >= 4 and faceUp <= 6:
                    return 'Double' if canDouble else 'Hit'
                else:
                    return 'Hit'
            elif total[1] == 14 or total == 13:
                if faceUp >= 5 and faceUp <= 6:
                    return 'Double' if canDouble else 'Hit'
                else:
                    return 'Hit'
        else:
            canDouble = hand.length() == 2
            if total[0] >= 17:
                return 'Stand'
            elif total[0] >= 13 and total[0] <= 16:
                if faceUp >= 2 and faceUp <= 6:
                    return 'Stand'
                else:
                    return 'Hit'
            elif total[0] == 12:
                if faceUp >= 4 and faceUp <=6:
                    return 'Stand'
                else:
                    return 'Hit'
            elif total[0] == 11:
                if faceUp == 1:
                    return 'Hit'
                else:
                    return 'Double' if canDouble else 'Hit'
            elif total[0] == 10:
                if faceUp >= 2 and faceUp <= 9:
                    return 'Double' if canDouble else 'Hit'
                else:
                    return 'Hit'
            elif total[0] == 9:
                if faceUp >= 3 and faceUp <= 6:
                    return 'Double' if canDouble else 'Hit'
                else:
                    return 'Hit'
            else:
                return 'Hit'
                
class Blackjack:
	def __init__(self, players):
		self.deck = Deck(6)
		self.players = []
		self.players.append(Player()) #dealer
		for i in range(players):
			self.players.append(Player())
    def shuffle(self):
        self.deck.shuffle()
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
def runPlays(times):
	blackjack = Blackjack(1)
	blackjack.shuffle()
	blackjack.deal()
    print(blackjack)
runPlays(1)
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
