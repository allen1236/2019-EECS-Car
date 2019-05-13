class Node:
    def __init__(self, index=0):
        self.index = index
        # store successors' indices
        self.successors = dict()
        self.directions = dict()

    def getIndex(self):
        return self.index

    def getSuccessors(self):
        return [ succ for succ in self.successors ] 

    def setSuccessor( self, successor, direction, distance ):
        # check whether 'successor' is valid by comparing with the class member
        for succ in self.successors:
            if succ == successor:
                return
        # Update the successors in data members 
        self.successors[ successor ] = distance
        self.directions[ successor ] = direction
        return

    def isSuccessor(self, nd):
        # check whether nd is a successor
        return ( nd in self.successors ) 

    def isEnd(self):
        return len(self.successors) == 1 and self.index != 1

    def getDirection( self, nd ):
        if nd in self.successors:
            return self.directions[ nd ]
        else:
            print( "Error: path doesn't exist!" )
            return 0 

    def getDistances( self ):
        return self.successors


