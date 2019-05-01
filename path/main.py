import random
from node import *
import maze as mz

maze_path = "data/maze.csv"
total_nodes = 6

def get_path( maze ):
    
    path_len = dict()
    print( maze.nd_dict[1].getSuccessors() )

    #TODO

    return path_len

def find_path( path_len, maze ):
    pass

def main():

    maze = mz.Maze( maze_path )
    path_len = get_path( maze )
    #path = find_path( path_len, maze )

if __name__=='__main__':
    main()
 
