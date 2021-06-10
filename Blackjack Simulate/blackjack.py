from deck import Deck
from strategy import Strategy
from player import Player
import time

class Blackjack:
    def __init__(self, players = 1, numDecks = 2):
        self.deck = Deck(numDecks)
        self.players = []
        for i in range(players):
            self.players.append(Player())
        self.players.append(Player()) #dealer
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
    def clearHands(self):
        for player in self.players:
            player.clear()
    def playerMove(self):
        dealer = self.players[1]
        if dealer.hasBlackjack():
            return
        player = self.players[0]
        player.play(self.players[1].getFaceUp(), self.deck)
    def dealerMove(self):
        dealer = self.players[1]
        dealer.dealerPlay(self.deck)
    def winner(self):
        dealerTotal = self.players[1].maxTotal()
        dealer = self.players[1]
        player = self.players[0]
        for j in range(len(player.hand)):
            currHand = player.hand[j]
            currTotal = player.maxTotal(j)
            if dealer.hasBlackjack():
                if not player.hasBlackjack():
                    player.updateMoney(-player.bets[j])
                    player.addMultiplierLoss(player.bets[j])
            elif currTotal > 21: #if player busted
                player.updateMoney(-player.bets[j])
                player.addMultiplierLoss(player.bets[j])
                #print('busted remove ' + str(player.bets[j]))
            elif player.hasBlackjack(j) \
                and not (dealer.hasBlackjack()): #if blackjack and dealer not blackjack
                player.updateMoney(player.bets[j] * 1.2)
                player.addMultiplierWinner(player.bets[j] * 1.2)
                #print('blackjack add ' + str(player.bets[j] * 3 / 2))
            elif dealerTotal > 21 or currTotal > dealerTotal: #dealer busted or greater than dealer
                player.updateMoney(player.bets[j])
                player.addMultiplierWinner(player.bets[j])
                #print('dealer busted or greater than dealer' + str(player.bets[j]))
            elif currTotal < dealerTotal:
                player.updateMoney(-player.bets[j])
                player.addMultiplierLoss(player.bets[j])
                #print('dealer wins ' + str(player.bets[j]))
    def play(self):
        self.adjustMultiplier()
        self.adjustSideBet()
        self.deal()
        dealerHasBlackjack = self.players[1].maxTotal() == 21
        
        self.players[0].paySideBet(dealerHasBlackjack)
        if self.players[1].maxTotal() == 21:
            self.winner()
        else:
            self.playerMove()
            self.dealerMove()
            self.winner()
    def adjustMultiplier(self):
        player = self.players[0]
        player.adjustMultiplier(self.deck.getTrueCount())
    def adjustSideBet(self):
        player = self.players[0]
        player.adjustSideBet(self.deck.getSideBetTrueCount())
    def __str__(self):
        player = self.players[0]
        print("Dealer: ")
        print(self.players[1])
        print("Player: ")
        print(self.players[0])
        print("playerMoney: " + str(self.players[0].money))
        print('minMoney: ' + str(player.minMoney))
        print('minCount: ' + str(player.minCount))
        print('maxMoney: ' + str(player.maxMoney))
        print('count: ' + str(self.deck.count))
        print('bets: ' + str(player.bets))
        wins = player.multiplierWin
        losses = player.multiplierLoss

        percentWin = []
        percentLoss = []
        percentDiff = []
        for i in range(len(wins)):
            if wins[i] + losses[i] == 0:
                percentWin.append(0)
                percentLoss.append(0)
                percentDiff.append(0)
            else:
                percentWin.append(round(wins[i] / (wins[i] + losses[i]), 4))
                percentLoss.append(round(losses[i] / (wins[i] + losses[i]), 4))
                percentDiff.append(round((percentWin[i] - percentLoss[i]) * 100, 2));
        print('Player count: ' + str(player.countCount))
        print('Player percent win: ' + str(percentWin))
        print('Player percent loss: ' + str(percentLoss))
        print('Player percent diff: ' + str(percentDiff))
        return ''
        #for i in range(len(player.sideBetWin)):
        wins = player.sideBetWin
        losses = player.sideBetLoss
        percentSideWin = []
        percentSideLoss = []
        percentSideDiff = []
        for i in range(len(wins)):
            if player.sideBetWin[i] + player.sideBetLoss[i] == 0:
                percentSideWin.append(0)
                percentSideLoss.append(0)
                percentSideDiff.append(0)
            else:
                percentSideWin.append(round(wins[i] / (wins[i] + losses[i]), 4))
                percentSideLoss.append(round(losses[i] / (wins[i] + losses[i]), 4))
                percentSideDiff.append(round((percentSideWin[i] - percentSideLoss[i]) * 100, 2));
        print('Player sideBetWin: ' + str(percentSideWin))
        print('Player sideBetLoss: ' + str(percentSideLoss))
        print('Player side Bet Count: ' + str(percentSideDiff))
        print('sideBetMoney: ' + str(player.sideBetMoney))
        print('actually Side Bet: ' + str(player.actuallySideBet))
        
        
        return ""