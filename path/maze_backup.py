import node
import math
import csv
import pandas

class Maze:
    def __init__(self, filepath):
        """
        read file and build graph
        """
        # data read from csv
        self.raw_data = pandas.read_csv(filepath).values
        # graph if saved here
        self.nd_dict = dict()

        # process raw_data
        dead_end = []
        print(dead_end)
        for dt in self.raw_data:
            nd = node.Node(dt[0])
            for i in range(1,5):
                if not math.isnan(dt[i]):
                    nd.setSuccessor(int(dt[i]))

            self.nd_dict[dt[0]] = nd
        
        print(dead_end) 
        #print self.self.nd_dict
        #for i in range(1, len(self.nd_dict)+1):
        #print(i,self.nd_dict[i].getSuccessors())
    
    def shortestPath(self, nd_from, nd_to):
        """ 
        return a path (sequence of nodes) from the current node to the nearest unexplored deadend 
        e.g.
            1 -- 2 -- 3     
                 |    |  ->  shortestPath(1,4) returns [1,2,4]
                 4 -- 5
        """
        Q = []
        d = {}
        pi = {}
        marked = []

        #initialization
        Q.append(self.nd_dict[nd_from])
        marked.append(self.nd_dict[nd_from])
        d[self.nd_dict[nd_from]] = 0

        while len(Q) != 0:
            u = Q.pop(0)
            
            successor = u.getSuccessors()
            for v in successor:
                if self.nd_dict[v] not in marked:
                    marked.append(self.nd_dict[v])
                    Q.append(self.nd_dict[v])
                    d[self.nd_dict[v]] = d[u] + 1
                    pi[self.nd_dict[v]] = u
        path = []
        tank = self.nd_dict[nd_to]
        while True:
            path.append(tank)
            if tank.getIndex() == nd_from:
                break
            tank = pi[tank]
        
        path = path[::-1] 
        path_result = []
        
        for i in range(len(path)):
            index = path[i].getIndex()
            path_result.append(int(index))

        return path_result

     

             
             
         


