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
        self.dead_end = []
        
        for dt in self.raw_data:
            nd = node.Node(dt[0])
            for i in range(1,5):
                if not math.isnan(dt[i]):
                    nd.setSuccessor(int(dt[i]))
                self.nd_dict[dt[0]] = nd
    
        for dt in self.raw_data:
            count = 0
            nd = node.Node(dt[0])
            for i in range (1,5):
                if math.isnan(dt[i]):
                    count += 1
                    
            if count == 3:
                self.dead_end.append(int(dt[0]))
               
        
        
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
        path = dict()
        unexplored = [nd_from] 
        while nd_to not in path:
            if len(unexplored) == 0:
                return []
            unexplored_copy = list(unexplored)
            for nd in unexplored_copy:
                for neighbor in self.nd_dict[nd].getSuccessors():
                    if neighbor not in path:
                        unexplored.append(neighbor)
                        path[neighbor] = nd
                unexplored.remove(nd)
        pos = nd_to
        ans = [ nd_to ]
        while pos is not nd_from:
            ans = [ path[pos] ] + ans
            pos = path[pos]
        return ans
