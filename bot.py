import Blackjack as b

#b.runPlays(100000);

#b.runCount(2000000)
#b.wipeSaves()

#b.winRate(blackjack, blackjack.normal, 100)
def passRate(times):
	count = 0
	for i in range(times):
		blackjack = b.Blackjack(1)
		notFail = b.money(blackjack, blackjack.normal, 50)
		if notFail:
			count += 1
	print(count / times)
passRate(1000)
#b.numberOfGames(blackjack, blackjack.normal)