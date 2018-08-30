import Blackjack as b

#b.runPlays(100000);

blackjack = b.Blackjack(1)
blackjack.shuffle()
blackjack.deal()
blackjack.playerMove()
blackjack.dealerMove()
print(blackjack.count)