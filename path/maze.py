import node
import math
import csv
import pandas
import copy

class Maze:
    def __init__(self, filepath):
        #read file and build graph
        # data read from csv
        self.raw_data = pandas.read_csv(filepath).values
        # graph if saved here
        self.nd_dict = dict()

        # process raw_data
        self.dead_end = [1]

        direction = {1:1, 2:3, 3:4, 4:2}
        
        for dt in self.raw_data:
            nd = node.Node(dt[0])
            for i in range(1,5):
                if not math.isnan(dt[i]):
                    nd.setSuccessor( int(dt[i]), direction[i], int(dt[i+4]) )
            self.nd_dict[dt[0]] = nd
            if nd.isEnd():
                self.dead_end.append( int(dt[0]) )
    
    def shortestPath(self, nd_from, nd_to):

        path = dict()
        unexplored = [nd_from] 
        counter = {nd_from: copy.copy( self.nd_dict[nd_from].getDistances() )} 

        while nd_to not in path:
            unexplored_copy = list(unexplored)
            for nd in unexplored_copy:
                end = True
                for neighbor in self.nd_dict[nd].getSuccessors():
                    if neighbor not in path:
                        if counter[nd][neighbor] > 0:
                            counter[nd][neighbor] -= 1;
                            end = False
                        else: 
                            unexplored.append(neighbor)
                            counter[neighbor] = copy.copy( self.nd_dict[neighbor].getDistances() )
                            path[neighbor] = nd
                if end:
                    unexplored.remove(nd)

        ans = [] 
        distances = 0 
        pos = nd_to

        while pos is not nd_from:
            ans = [ path[pos] ] + ans
            distances += self.nd_dict[ pos ].getDistances()[ path[pos] ]
            pos = path[pos]
        distances += len( ans ) - 1

        return ans

    def shortestPath_list(self, nd_from, nds_to):

        path = dict()
        unexplored = [nd_from] 
        counter = {nd_from: copy.copy( self.nd_dict[nd_from].getDistances() )} 

        while len(unexplored) > 0:
            unexplored_copy = list(unexplored)
            for nd in unexplored_copy:
                end = True
                for neighbor in self.nd_dict[nd].getSuccessors():
                    if neighbor not in path:
                        if counter[nd][neighbor] > 0:
                            counter[nd][neighbor] -= 1;
                            end = False
                        else: 
                            unexplored.append(neighbor)
                            counter[neighbor] = copy.copy( self.nd_dict[neighbor].getDistances() )
                            path[neighbor] = nd
                if end:
                    unexplored.remove(nd)

        paths = dict()
        distances = dict()
        for nd_to in nds_to:
            pos = nd_to
            ans = [ nd_to ]
            distances[ nd_to ] = 0
            while pos is not nd_from:
                ans = [ path[pos] ] + ans
                distances[ nd_to ] += self.nd_dict[ pos ].getDistances()[ path[pos] ]
                pos = path[pos]
            paths[nd_to] = ans
            distances[ nd_to ] += len( paths[ nd_to ] ) - 1
        return distances 

    def get_distances( self ):
        
        dead_end = self.dead_end
        print( dead_end )
        path_len = dict()
        for i in dead_end:
            path_list = self.shortestPath_list( i, dead_end )
            for j in path_list:
                path_len[(i,j)] = path_list[ j ] 
                print( self.shortestPath( i, j )) 
        return path_len

    def find_path( self, distances ):
        path = [ self.dead_end[0] ]
            

        
        

        
        return path

    def find_full_path( self, path ):
        full_path = []

        return full_path

    def generate_cmd( self, cmd ):
        pass
