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
    def __init__(self, numDecks):
        self.deck = []
        self.index = 0
        self.numDecks = numDecks
        self.length = numDecks * 52
        self.setCut()
        self.count = 0
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
        self.cut = math.floor((self.numDecks - random.random() - 1) * 52)
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
        value = card.value
        if value <= 6 and value >= 2:
            self.count = self.count + 1
        elif value >= 10 or value == 1:
            self.count = self.count - 1
    def getTrueCount(self):
        trueCount = round(self.count * 52 / (len(self.deck) - self.index))
        return trueCount
class Player:
    def __init__(self):
        self.hand = [[]]
        self.prevTotal = 0
        self.bet = 10
        self.money = 0
        self.multiplier = 1
        self.bets = [self.bet * self.multiplier]
    def getFaceUp(self):
        return self.hand[0][0]
    def changeBet(self, amount):
        self.bet = amount
    def resetMoney(self, amount):
        self.money = amount
    def updateMoney(self, sign):
        self.money += self.multiplier * self.bet * sign
    def adjustMultiplier(self, trueCount):
        if trueCount < 2:
            self.bet = 10
        elif trueCount < 3:
            self.bet = 25
        elif trueCount < 4:
            self.bet = 50
        elif trueCount < 5:
            self.bet = 75
        else:
            self.bet = 100
            
    def getTotal(self, hand = None):
        if hand == None:
            hand = self.hand[0]
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
    def hit(self, card, handNum=0):
        self.hand[handNum].append(card)
    def clear(self):
        self.hand = [[]]
        self.bets = [self.multiplier * self.bet]
    def __str__(self):
        allHands = []
        for hand in self.hand:
            handArr = []
            for card in hand:
                handArr.append(str(card))
            allHands.append(handArr)
        return str(allHands)
    def hasAce(self, hand):
        for card in hand:
            if card.value == 1:
                return true
        return false
    def hasBlackjack(self, handNum=0):
        hand = self.hand[handNum]
        if self.maxTotal(handNum) == 21 and len(hand) == 2:
            return True
        else:
            return False
    def canSplit(self, hand):
        return len(hand) == 2 and hand[0].value == hand[1].value
    def isBusted(self, hand):
        return self.maxTotal(hand) > 21
    def maxTotal(self, handNum=0):
        total = self.getTotal(self.hand[handNum])
        return total[len(total) - 1]
    def play(self, faceUp, deck):
        currHand = self.hand[0]
        currIndex = 0
        while True:
            if len(self.hand) == currIndex:
                return True
            else:
                currHand = self.hand[currIndex]
            strategy = self.basicStrategy(currHand, faceUp.value)
            if strategy == 'Split':
                newHand = [currHand.pop()]
                currHand.append(deck.deal())
                newHand.append(deck.deal())
                self.hand.append(newHand)
                self.bets.append(self.bet * self.multiplier)
            elif strategy == 'Hit':
                currHand.append(deck.deal())
            elif strategy == 'Double':
                currHand.append(deck.deal())
                self.bets[currIndex] *= 2
                currIndex += 1
            elif strategy == 'Stand':
                currIndex += 1
            else:
                print('currHand')
                for i in range(len(currHand)):
                    print(currHand[i])
                return None
    def basicStrategy(self, hand, faceUp):
        total = self.getTotal(hand)
        if self.canSplit(hand) and hand[0].value != 5:
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
            else:
                return 'Stand'
        elif len(total) == 2: #has an ace and soft
            canDouble = len(hand) == 2
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
            elif total[1] == 14 or total[1] == 13:
                if faceUp >= 5 and faceUp <= 6:
                    return 'Double' if canDouble else 'Hit'
                else:
                    return 'Hit'
        else:
            canDouble = len(hand) == 2
            maxTotal = total[len(total) - 1]
            if maxTotal >= 17:
                return 'Stand'
            elif maxTotal >= 13 and maxTotal <= 16:
                if faceUp >= 2 and faceUp <= 6:
                    return 'Stand'
                else:
                    return 'Hit'
            elif maxTotal == 12:
                if faceUp >= 4 and faceUp <=6:
                    return 'Stand'
                else:
                    return 'Hit'
            elif maxTotal == 11:
                if faceUp == 1:
                    return 'Hit'
                else:
                    return 'Double' if canDouble else 'Hit'
            elif maxTotal == 10:
                if faceUp >= 2 and faceUp <= 9:
                    return 'Double' if canDouble else 'Hit'
                else:
                    return 'Hit'
            elif maxTotal == 9:
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
            for j in range(2): #deal two cards
                player = self.players[i]
                card = self.deck.deal()
                player.hit(card)
                if i != 0 or j == 0: #start counting all face up cards
                    self.deck.cardCount(card)
    def clearHands(self):
        for player in self.players:
            player.clear()
    def playerMove(self):
        dealer = self.players[0]
        if dealer.hasBlackjack():
            return
        for i in range(1,len(self.players)):
            player = self.players[i]
            player.play(self.players[0].getFaceUp(), self.deck)
    def dealerMove(self):
        dealer = self.players[0]
        while dealer.maxTotal() < 17:
            dealer.hit(self.deck.deal())
    def winner(self):
        dealerTotal = self.players[0].maxTotal()
        dealerHand = self.players[0].hand[0]
        for i in range(1, len(self.players)):
            player = self.players[i]
            for j in range(len(player.hand)):
                currHand = player.hand[j]
                currTotal = player.maxTotal(j)
                if currTotal > 21: #if player busted
                    player.money -= player.bets[j]
                    #print('busted remove ' + str(player.bets[j]))
                elif currTotal == 21 and len(currHand) == 2 \
                    and not (dealerTotal == 21 and len(dealerHand) == 2): #if blackjack
                    player.money += player.bets[j] * 3 / 2
                    #print('blackjack add ' + str(player.bets[j] * 3 / 2))
                elif dealerTotal > 21 or currTotal > dealerTotal: #dealer busted or greater than dealer
                    player.money += player.bets[j]
                    #print('dealer busted or greater than dealer' + str(player.bets[j]))
                elif currTotal < dealerTotal:
                    player.money -= player.bets[j]
                    #print('dealer wins ' + str(player.bets[j]))
                
    def countDealer(self):
        dealer = self.players[0]
        self.cardCount(dealer.hand[0])
        player = self.players[1]
        for i in range(2, len(player.hand)):
            self.cardCount(player.hand[i])
    def play(self):
        self.adjustMultiplier()
        self.deal()
        self.playerMove()
        self.dealerMove()
        self.winner()
    def adjustMultiplier(self):
        trueCount = self.deck.getTrueCount()
        for i in range(1, len(self.players)):
            player = self.players[i]
            player.adjustMultiplier(trueCount)
    def result(self):
        cardCount = round(self.count * 52 / (self.deck.length - self.deck.index))
        self.countDealer()
        return {"winner": self.winner()[0], 
                "standWinner": self.standWinner()[0], 
                "lastValue": self.lastPlayerValue(0), 
                "dealerFaceUp": self.dealerFaceUp(),
                "cardCount": cardCount}
    def __str__(self):
        print("Dealer: ")
        print(self.players[0])
        print(self.players[0].getTotal())
        print("Player: ")
        print(self.players[1])
        print(self.players[1].getTotal())
        print("playerMoney: " + str(self.players[1].money))
        return ""
def runPlays(times):
    blackjack = Blackjack(1)
    blackjack.shuffle()
    
    for i in range(times):
        if i % 100000 == 0:
            print(i)
        blackjack.play()
    print(blackjack)
runPlays(1000000)
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
