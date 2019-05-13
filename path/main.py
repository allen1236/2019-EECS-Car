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
    print( maze.dead_end )
    path = maze.find_path( distances )

    #找出完整路徑
    full_path = maze.find_full_path( path )

    #生成並寫入指令
    cmd = open('cmd.txt')
    maze.generate_cmd( cmd )

if __name__=='__main__':
    main()

