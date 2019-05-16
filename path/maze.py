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
        direction = {1:1, 2:3, 3:4, 4:2}
        # process raw_data
        for dt in self.raw_data:
            nd = node.Node(dt[0])
            for i in range(1,5):
                if not math.isnan(dt[i]):
                    nd.setSuccessor( int(dt[i]), direction[i], int(dt[i+4]) )
            self.nd_dict[dt[0]] = nd
    
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

        ans = [ nd_to ] 
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
        _nds_to = list( nds_to )
        unexplored = [nd_from] 
        counter = {nd_from: copy.copy( self.nd_dict[nd_from].getDistances() )} 

        while len(_nds_to) > 0:
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
                            if neighbor in _nds_to:
                                _nds_to.remove( neighbor )
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

    def get_distances( self, start_point, _deadends ):
        
        path_len = dict()
        deadends = [ start_point ] + _deadends
        for i in deadends:
            path_list = self.shortestPath_list( i, deadends )
            for j in path_list:
                path_len[(i,j)] = path_list[ j ] 
        return path_len

    def find_path( self, distances, start_point, deadends ):
        path = [ start_point ]
        total_len = 0
        for dead_end_add in deadends:
            insert_pos = 0
            smallest = -1
            for i in range(len(path)):
                compare = total_len + distances[(path[i], dead_end_add)]
                if i != len(path) - 1:
                    compare -= distances[(path[i], path[i+1])]
                    compare += distances[(dead_end_add, path[i+1])]
                if smallest == -1 or compare < smallest:
                    insert_pos = i
                    smallest = compare
            path.insert( insert_pos+1, dead_end_add )
            total_len += smallest
        return path

    def find_full_path( self, path ):
        full_path = [ path[0] ]
        for nd_from, nd_to in zip( path[:-1], path[1:] ):
            full_path += self.shortestPath( nd_from, nd_to )[1:]
        return full_path

    def generate_cmd( self, cmd, full_path, deadends ):
        cmds=[]
        for i in range(len(full_path)-2):
            A=int(self.nd_dict[full_path[i]].getDirection(full_path[i+1]))-int(self.nd_dict[full_path[i+1]].getDirection(full_path[i+2]))
            if A==-3 or A==1:
                cmds.append('nl')
            if A==-1 or A==3:
                cmds.append('nr')
            if A==0:
                cmds.append('nf')
            if A==2 or A==-2:
                cmds.append('ng')
        print(cmds)
        for c in cmds:
            cmd.write( c + '\n' )
        cmd.write( 'stop' )

