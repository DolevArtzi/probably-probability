class Player:
    def __init__(self,name):
        self.name = name

    def setName(self,name):
        self.name = name

    def setHand(self,hand):
        self.hand = hand

    def getHand(self):
        return self.hand

    def __str__(self):
        return str(self.name)

