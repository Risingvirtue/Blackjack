from blackjack import Blackjack

def runPlays(times):
    blackjack = Blackjack(1, 6)
    blackjack.shuffle()
    for i in range(times):
        if i % 100000 == 0:
            print(i)
        blackjack.play()
    print(blackjack)
runPlays(1000000)