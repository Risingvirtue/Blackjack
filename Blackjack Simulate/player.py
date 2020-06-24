from strategy import Strategy
import time
class Player:
    def __init__(self):
        self.sideBet = 25
        self.actuallySideBet = 0
        self.sideBetMoney = 0
        self.initSideBets()
        
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
    def initSideBets(self):
        self.sideBetWin = []
        self.sideBetLoss = []
        self.sideBetCount = []
        for i in range(20):
            self.sideBetWin.append(0)
            self.sideBetLoss.append(0)
            self.sideBetCount.append(0)
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
        if trueCount < 1:
            self.bet = 10
            self.currMultiplier = 0
        elif trueCount == 1:
            self.bet = 50
            self.currMultiplier = 1
        elif trueCount == 2:
            self.bet = 75
            self.currMultiplier = 2
        elif trueCount == 3:
            self.bet = 100
            self.currMultiplier = 3
        elif trueCount == 4:
            self.bet = 150
            self.currMultiplier = 4
        else:
            self.bet = 200
            self.currMultiplier = 4
    def adjustSideBet(self, trueCount):
        if trueCount <= 0:
            self.currSideCount = 0
        elif trueCount >= 20:
            self.currSideCount = 19
        else:
            self.currSideCount = trueCount
        if trueCount < 9:
            self.sideBet = 0
        else: 
            self.sideBet = 25
            self.actuallySideBet += 1
    def paySideBet(self, dealerHasBlackjack):
        self.sideBetCount[self.currSideCount] += 1
        if self.maxTotal() != 20:
            self.sideBetMoney -= self.sideBet
            self.sideBetLoss[self.currSideCount] += self.sideBet
        else:
            card1 = self.hand[0][0]
            card2 = self.hand[0][1]
            profit = 0
            if card1.value == 13 and card2.value == 13:
                if card1.suit == 3 and card2.suit == 3:
                    if dealerHasBlackjack:
                        profit = 1000 * self.sideBet
                    else:
                        profit = 100 * self.sideBet
                elif card1.suit == card2.suit:
                    profit = 50 * self.sideBet
                else:
                    profit = 8 * self.sideBet
            elif card1.value == card2.value:
                if card1.suit == card2.suit:
                    profit = 20 * self.sideBet
                else:
                    profit = 4 * self.sideBet
            else:
                if card1.suit == card2.suit:
                    profit = 10 * self.sideBet
                else:
                    profit = 4 * self.sideBet    
            self.sideBetMoney += profit
            self.sideBetWin[self.currSideCount] += profit
            
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
            if card.value == 1:
                hasAce = True
            total += min(card.value, 10)
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
        handCopy = []
        for i in range(len(self.hand)):
            handCopy.append([])
            for j in range(len(self.hand[i])):
                handCopy[i].append(str(self.hand[i][j]))
        return str(handCopy)
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