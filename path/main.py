import random
from node import *
import maze as mz

maze_path = "data/maze2.csv"
total_nodes = 20


def main():

    maze = mz.Maze( maze_path )

    #find the distances between deandends
    distances = maze.get_distances()
    print( distances )
    
    #找出經過各deadend的順序
    #path = maze.find_path( distances )
    path = [ 1, 10, 12, 17 ] 

    #找出完整路徑
    full_path = maze.find_full_path( path )

    #生成並寫入指令
    cmd = open('../bluetooth/cmd.txt', 'w+')
    maze.generate_cmd( cmd, full_path )

if __name__=='__main__':
    main()

