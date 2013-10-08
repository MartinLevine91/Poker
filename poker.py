"""
5 point plan:
* Outs calculator

Two options: it could "think" like a person: figure out what hand it
has and proceed from there. it could brute force it. I prefer the former,
though it may need lots and lots of work.

Presume the former.
- needs a class or something for describing the hand
- will probably have to think about things seperately.
> ofAKinds
> straights
> flushes



* auto-watch full tilt and give odds/outs to one side
* Super impose over full tilt (always on top)
* track opponent profits
* become smarter (heuristics? AI course style learning?)
"""
import random

def findOuts(hand):
    """
    Not designed for runner-runner or more.
    """
    outsTo = Outs()
    # count flush cards
    
    # look for straight draws

    # nOfAKind analysis
    nOfAKind = [[],[],[],[]]
    lastCard = None
    current_nOfAKind = []

    for card in hand:
        if lastCard == None:
            current_nOfAKind.append(card)
        elif card%13 == lastCard%13:
            current_nOfAKind.append(card)
        else:
            n = len(current_nOfAKind)
            nOfAKind[n-1].append(current_nOfAKind)
            current_nOfAKind = [card]

        lastCard = card

    n = len(current_nOfAKind)
    nOfAKind[n-1].append(current_nOfAKind)

    while True:
        pass
    
    
    """
Output:
class rather than dict?
information stored in list, but accessable for both read and
write through methods.



    """
    


class Outs():
    # designed for single draw, would need to be redesigned
    # to consider runnner-runner options.
    def __init__(self):
        self.Pair = None
        self.TwoPair = None
        self.ThreeOfAKind = None
        self.Straight = None
        self.Flush = None
        self.FullHouse = None
        self.FourOfAKind = None
        self.StraightFlush = None

class Deck():
    def __init__(self,shuffled=True,CardList= None):
        if CardList == None:
            self.CardList = range(0,52)
            if shuffled == True:
                random.shuffle(self.CardList)
        else:
            self.CardList =CardList
                
    def deal(self,card = None):
        if card == None:
            return self.CardList.pop()
        else:
            CardList.remove(card)
            return card
        

def string(card,length = "Short"):
    if length == "Short": 
        value = card%13 + 2
        valDict = {2:"2",
                   3:"3",
                   4:"4",
                   5:"5",
                   6:"6",
                   7:"7",
                   8:"8",
                   9:"9",
                   10:"T",
                   11:"J",
                   12:"Q",
                   13:"K",
                   14:"A"}
        suit = ["C","D","H","S"][card/13]
        return valDict[value] + suit
    elif length == "Long":
        value = card%13 + 2
        valDict = {2:"Two",
                   3:"Three",
                   4:"Four",
                   5:"Five",
                   6:"Six",
                   7:"Seven",
                   8:"Eight",
                   9:"Nine",
                   10:"Ten",
                   11:"Jack",
                   12:"Queen",
                   13:"King",
                   14:"Ace"}
        suit = ["Clubs","Diamonds","Hearts","Spades"][card/13]
        return '%s of %s' % (valDict[value],suit)
        
    
def evaluateHand(hand):
    handDict = {
        "Straight Flush":   None,
        "Four of a kind":   None,
        "Full House":       None,
        "Flush":            None,
        "Straight":         None,
        "Three of a kind":  None,
        "Two of a kind":    None,
        "High card":        None
        }

# Straight Flush
    # Sort hand by suit then High to low
    hand.sort()
    hand.reverse()
    straightFlush = []
    lastCard = -1
    for card in hand:
        #If a card is in the same suit and has a value one lower
        if card/13 == lastCard/13 and card == lastCard - 1:
            #Add it to the current straight flush
            straightFlush.append(card)
        else:
            #If you've just changed suit, and have a SF run ending in a 2:
            #check to see if you have an Ace in that suit
            if len(straightFlush) == 4 and lastCard%13 == 0 and (lastCard + 12) in hand:
                    #If you do, add that Straight Flush to the dict, but
                    #only if there isn't already one there (as this is 5 high)
                    straightFlush.append(lastCard + 12)
                    if handDict["Straight Flush"] == None:
                        handDict["Straight Flush"] = straightFlush
                        
            #if a card doesn't add to your streak, try again from the zero:
            straightFlush = [card]
        #if you have a straight flush:
        if len(straightFlush) == 5:
            # if there isn't a straight flush already stored, add this one to
            #hand dict
            if handDict["Straight Flush"] == None:
                handDict["Straight Flush"] = straightFlush            
            else:
                #Store the SF with the largest minimum value, found 5 highs
                #are stored elsewhere, so this assumes 2 lows are 6 high and
                #gives priority to found hands.
                minStored = (min(handDict["Straight Flush"]))%13
                minFound = (min(straightFlush))%13
                if minFound >= minStored:
                    handDict["Straight Flush"] = straightFlush
            straightFlush = []
        lastCard = card
    #If you've just changed finished the deck, and have a SF run ending in a 2:
    #check to see if you have an Ace in that suit
    if len(straightFlush) == 4 and lastCard%13 == 0 and (lastCard + 12) in hand:
            #If you do, add that Straight Flush to the dict, but
            #only if there isn't already one there (as this is 5 high)
            straightFlush.append(lastCard + 12)
            if handDict["Straight Flush"] == None:
                handDict["Straight Flush"] = straightFlush

#Flush
    flush = []
    lastCard = -1
    for card in hand:
        #If a card is in the same suit
        if card/13 == lastCard/13:
            #Add it to the current flush
            flush.append(card)
        else:
            #if a card doesn't add to your streak, try again from the zero:
            flush = [card]
        #if you have a flush:
        if len(flush) == 5:
            # if there isn't a flush already stored, add this one to
            #hand dict
            if handDict["Flush"] == None:
                handDict["Flush"] = flush
            else:
                #Compare the flushes and store the better one.
                storedFlush = handDict["Flush"]
                print storedFlush
                print flush
                scoreStored = 0
                scoreFound = 0
                for i in range(5):
                    scoreStored += storedFlush[-(i+1)]%13 * 13**i
                    scoreFound += flush[-(i+1)]%13 * 13**i
                    
                if scoreFound >= scoreStored:
                    handDict["Flush"] = flush
            flush = []
        lastCard = card


# Straight
    hand.sort(key =(lambda x: x%13))
    hand.reverse()

    straight = [hand[0]]
    lastCard = hand[0]
    for card in hand:
        #If a card continues the current run
        if card%13 == lastCard%13 - 1:
            #Add it to the straight
            straight.append(card)
        #If a card has the same value as the card before
        elif card%13 == lastCard%13:
            #ignore it
            pass
        #If the card has more than a gap of one from the previous card, start
        #from zero.
        else:
            straight = [card]
            
        if len(straight) == 4 and straight[0]%13 == 3:
            for ace in [12,25,38,51]:
                if ace in hand:
                    straight.append(ace)
                    #If you do, add that Straight to the dict, but only
                    #if there isn't already one there (as this is just 5 high)                    if handDict["Straight"] == None:
                    handDict["Straight"] = straight
                    straight = []
                    break
        #if you have a straight:
        elif len(straight) == 5:
            # if there isn't a straight already stored, add this one to
            #hand dict
            if handDict["Straight"] == None:
                handDict["Straight"] = straight
                
            else:
                #Store the straight with the largest minimum value, found 5 highs
                #are stored elsewhere, so this assumes 2 lows are 6 high and
                #gives priority to found hands.
                minStored = (min(handDict["Straight"]))%13
                minFound = (min(straightFlush))%13
                if minFound >= minStored:
                    handDict["Straight"] = straight
            straight = []
        lastCard = card           

    nOfAKind = [[],[],[],[]]
    lastCard = None
    current_nOfAKind = []

    for card in hand:
        if lastCard == None:
            current_nOfAKind.append(card)
        elif card%13 == lastCard%13:
            current_nOfAKind.append(card)
        else:
            n = len(current_nOfAKind)
            nOfAKind[n-1].append(current_nOfAKind)
            current_nOfAKind = [card]

        lastCard = card

    n = len(current_nOfAKind)
    nOfAKind[n-1].append(current_nOfAKind)
    current_nOfAKind = [card]

    #FourOfAKind
    handDict["Four of a kind"] = findnOfAKindHand(nOfAKind,[4,1])
    handDict["Full House"] = findnOfAKindHand(nOfAKind,[3,2])    
    handDict["Three of a kind"] = findnOfAKindHand(nOfAKind,[3,1,1])    
    handDict["Two Pair"] = findnOfAKindHand(nOfAKind,[2,2,1])    
    handDict["Two of a kind"] = findnOfAKindHand(nOfAKind,[2,1,1,1])    
    handDict["High card"] = findnOfAKindHand(nOfAKind,[1,1,1,1,1])    

    for item in handDict:
        print item + " "*(20-len(item)),
        print handDict[item]
        
    return handDict

def findnOfAKindHand(nOfAKind,target):
#target is in the format [4,1] or [2,2,1] for four of a kind and two pair respectively
    target.sort()
    target.reverse()

    used = []
    handSoFar = []
    for n in target:
        found = findnOfAKind(n, used, nOfAKind)
        if found:
            handSoFar = handSoFar + found[:n]
            used.append(found)
        else:
            return None
    return handSoFar
            
    
        
def findnOfAKind(nMin,used,nOfAKind):
    best = None
    for n in range(nMin, 4):
        for current_nOfAKind in nOfAKind[n-1]:
            if current_nOfAKind not in used:
                if best == None:
                    best = current_nOfAKind
                elif (best[0])%13 < (current_nOfAKind[0])%13:
                    best = current_nOfAKind
    return best
           

