import Blackjack as b
blackjack = b.Blackjack(1)
blackjack.shuffle()

blackjack.play()
print("Dealer's face up is: ")
print(blackjack.players[0].hand[1])
while blackjack.players[1].maxTotal() < 21:
	yourTotal = blackjack.players[1].maxTotal()
	print("Your hand:")
	print(blackjack.players[1])
	print("Total: " + str(yourTotal))
	choice = input("Hit? Y or N:")
	if choice == "Y":
		blackjack.playerHit()
	else:
		break
if blackjack.players[1].maxTotal() > 21:
	print("Your hand:")
	print(blackjack.players[1])
	print("Busted, you lose")
else:
	blackjack.dealerMove()
	yourTotal = blackjack.players[1].maxTotal()
	dealerTotal = blackjack.players[0].maxTotal()
	print("Your hand: ")
	print(blackjack.players[1])
	print("Total: " + str(yourTotal))
	print("Dealer's hand: ")
	print(blackjack.players[0])
	print("Total: " + str(dealerTotal))
	if dealerTotal > 21:
		print("You Win!")
	elif yourTotal < dealerTotal:
		print("You lose!")
	elif yourTotal == dealerTotal:
		print("Push")
	else: 
		print("You Win!")