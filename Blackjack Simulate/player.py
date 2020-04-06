from strategy import Strategy
import time
class Player:
    def __init__(self):
        self.hand = [[]]
        self.bet = 10
        self.money = 0
        self.bets = [self.bet]
        self.currMultiplier = 0
        self.multiplierWin = [0,0,0,0,0]
        self.multiplierLoss = [0,0,0,0,0]
        self.countCount = [0,0,0,0,0]
        self.minMoney = 0
        self.maxMoney = 0
        self.minCount = 0
        self.count = 0
        self.Strategy = Strategy()
    def getFaceUp(self):
        return self.hand[0][0]
    def changeBet(self, amount):
        self.bet = amount
    def resetMoney(self, amount):
        self.money = amount
    def updateMoney(self, amount):
        self.money += amount
        if self.money < self.minMoney:
            self.minCount = self.count
            self.minMoney = self.money
        self.maxMoney = max(self.maxMoney, self.money)
    def adjustMultiplier(self, trueCount):
        self.count += 1
        if trueCount < 2:
            self.bet = 10
            self.currMultiplier = 0
        elif trueCount == 2:
            self.bet = 70
            self.currMultiplier = 1
        elif trueCount == 3:
            self.bet = 120
            self.currMultiplier = 2
        elif trueCount == 4:
            self.bet = 160
            self.currMultiplier = 3
        else:
            self.bet = 200
            self.currMultiplier = 4 
    def addMultiplierWinner(self, amount=1):
        self.multiplierWin[self.currMultiplier] += amount
        self.countCount[self.currMultiplier] += 1
    def addMultiplierLoss(self, amount=1):
        self.multiplierLoss[self.currMultiplier] += amount
        self.countCount[self.currMultiplier] += 1
    def getTotal(self, hand = []):
        total = 0
        hasAce = False
        for card in hand:
            if card == 1:
                hasAce = True
            total += min(card, 10)
        if hasAce:
            if total + 10 > 21:
                return [total]
            else:  
                return [total, total + 10]
        return [total]
    def hit(self, card, handNum = 0):
        self.hand[handNum].append(card)
    def clear(self):
        self.hand = [[]]
        self.bets = [self.bet]
    def __str__(self):
        return str(self.hand)
    def hasBlackjack(self, handNum = 0):
        hand = self.hand[handNum]
        if self.maxTotal(handNum) == 21 and len(hand) == 2:
            return True
        else:
            return False
    def canSplit(self, hand):
        return len(hand) == 2 and hand[0] == hand[1]
    def isBusted(self, hand):
        return self.maxTotal(hand) > 21
    def maxTotal(self, handNum = 0):
        total = self.getTotal(self.hand[handNum])
        return total[len(total) - 1]
    def play(self, faceUp, deck):
        currHand = self.hand[0]
        currIndex = 0
        while True:
            if len(self.hand) == currIndex:
                break
            else:
                currHand = self.hand[currIndex]
            strategy = self.Strategy.basicStrategy(currHand, faceUp)
            illustrious18 = self.Strategy.illustrious18(currHand, faceUp, deck.getTrueCount())
            if illustrious18:
                strategy = illustrious18
            if strategy == 'Split':
                newHand = [currHand.pop()]
                currHand.append(deck.deal())
                newHand.append(deck.deal())
                self.hand.append(newHand)
                self.bets.append(self.bet)
                if currHand[0] == 1:
                    break
            elif strategy == 'Hit':
                currHand.append(deck.deal())
            elif strategy == 'Double':
                currHand.append(deck.deal())
                self.bets[currIndex] *= 2
                currIndex += 1
            elif strategy == 'Stand':
                currIndex += 1
            else:
                break
    def dealerPlay(self, deck):
        currHand = self.hand[0]
        while True:
            strategy = self.Strategy.dealerStrategy(currHand)
            if strategy == 'Hit':
                currHand.append(deck.deal())
            elif strategy == 'Stand':
                return           