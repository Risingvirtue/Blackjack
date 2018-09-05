import Blackjack as b

#b.runPlays(100000);

#b.runCount(2000000)
#b.wipeSaves()
blackjack = b.Blackjack(1)
b.winRate(blackjack, blackjack.countPlay, 10000)