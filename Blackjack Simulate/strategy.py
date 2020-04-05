class Strategy:
    def __init__(self):
        return
    def getTotal(self, hand):
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
    def canSplit(self, hand):
        return len(hand) == 2 and hand[0] == hand[1]
    def dealerStrategy(self, hand):
        total = self.getTotal(hand)
        maxTotal = total[len(total) - 1]
        if maxTotal < 17 or (len(total) == 2 and maxTotal == 17):
            return 'Hit'
        else:
            return 'Stand'
    def basicStrategy(self, hand, faceUp):
        total = self.getTotal(hand)
        if self.canSplit(hand) and hand[0] != 5:
            if hand[0] == 2 or \
               hand[0] == 3:
                if faceUp <= 7 and faceUp != 1:
                    return 'Split'
                else:
                    return 'Hit'
            elif hand[0] == 7:
                if faceUp <= 8 and faceUp != 1:
                    return 'Split'
                else:
                    if faceUp >= 2 and faceUp <= 6:
                        return 'Stand'
                    else:
                        return 'Hit'
            elif hand[0] == 4:
                if faceUp == 5 or faceUp == 6:
                    return 'Split'
                else:
                    return 'Hit'
            elif hand[0] == 6:
                if faceUp >= 2 and faceUp <= 6:
                    return 'Split'
                else:
                    if faceUp >= 4 and faceUp <= 6:
                        return 'Stand'
                    else:
                        return 'Hit'
            elif hand[0] == 8 or hand[0] == 1:
                return 'Split'
            elif hand[0] == 9:
                if faceUp == 7 or faceUp == 10 or faceUp == 1:
                    return 'Stand'
                else:
                    return 'Split'
            else: #10
                return 'Stand'
        elif len(total) == 2: #has an ace and soft
            canDouble = len(hand) == 2
            if total[1] >= 19:
                if faceUp == 6:  
                    return 'Double'
                else:
                    return 'Stand'
            elif total[1] == 18:
                if faceUp == 7 or faceUp == 8:
                    return 'Stand'
                elif faceUp >= 2 and faceUp <= 6:
                    return 'Double' if canDouble else 'Stand'
                else:
                    return 'Hit'
            elif total[1] == 17 or total[1] == 16:
                if faceUp >= 3 and faceUp <= 6:
                    return 'Double' if canDouble else 'Hit'
                else:
                    return 'Hit'
            elif total[1] == 15 or total[1] == 14:
                if faceUp >= 4 and faceUp <= 6:
                    return 'Double' if canDouble else 'Hit'
                else:
                    return 'Hit'
            elif total[1] == 13:
                if faceUp >= 5 and faceUp <= 6:
                    return 'Double' if canDouble else 'Hit'
                else:
                    return 'Hit'
            else:
                return 'Stand'
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
                if faceUp >= 4 and faceUp <= 6:
                    return 'Stand'
                else:
                    return 'Hit'
            elif maxTotal == 11:
                return 'Double' if canDouble else 'Hit'
            elif maxTotal == 10:
                if faceUp >= 2 and faceUp <= 9:
                    return 'Double' if canDouble else 'Hit'
                else:
                    return 'Hit'
            elif maxTotal == 9:
                if faceUp >= 2 and faceUp <= 6:
                    return 'Double' if canDouble else 'Hit'
                else:
                    return 'Hit'
            else:
                return 'Hit'
    def illustrious18(self, hand, faceUp, count):
        #insurance w/ count 3
        #split 10s vs 6 w/ count 4
        #split 10s vs 5 w/ count 5
        #stay on 12 vs 3 w/  count 2
        #stay on 12 vs 2 w/ count 3
        #double on 9 vs 2 w/ count 1
        #double on 9 vs 7 w/ count 3
        #double on 10 vs 10 w/ count 4
        #double on 10 vs A w/ count 4
        #double on 11 vs A w/ count 1
        #stay on 16 vs 10 w/ count > 0
        #stay on 15 vs 10 w/ count 4
        #stay on 16 vs 9 w/ count 5
        #hit on 13 vs 2 w/ count -1
        #hit on 13 vs 3 w/ count -2
        #hit on 12 vs 4 w/ count < 0
        #hit on 12 vs 5 w/ count -2
        #hit on 12 vs 6 w/ count -1
        total = self.getTotal(hand)
        maxTotal = total[len(total) - 1]
        hasAce = len(total) == 2
        canDouble = len(hand) == 2
        if hasAce:
            return False
        elif maxTotal == 12:
            if faceUp == 2 and count >= 3:
                return 'Stand'
            elif faceUp == 3 and count >= 2:
                return 'Stand'
            elif faceUp == 4 and count < 0:
                return 'Hit'
            elif faceUp == 5 and count <= -2:
                return 'Hit'
            elif faceUp == 6 and count <= -1:
                return 'Hit'
            else:
                return False
        elif maxTotal == 13:
            if faceUp == 2 and count <= -1:
                return 'Hit'
            elif faceUp == 3 and count <= -2:
                return 'Hit'
            else:
                return False
        elif maxTotal == 16:
            if faceUp >= 10 and count > 0:
                return 'Stand'
            elif faceUp == 9 and count >= 5:
                return 'Stand'
            else:
                return False
        elif maxTotal == 15:
            if faceUp >= 10 and count >= 4:
                return 'Stand'
            else:
                return False
        elif canDouble:
            if maxTotal == 10 and faceUp >= 10 and count >= 4:
                return 'Double'
            elif maxTotal == 10 and faceUp == 1 and count >= 4:
                return 'Double'
            elif maxTotal == 9 and faceUp == 7 and count >= 3:
                return 'Double'
            elif maxTotal == 9 and faceUp == 2 and count >= 1:
                return 'Double'
            else:
                return False
        else:
            return False
        