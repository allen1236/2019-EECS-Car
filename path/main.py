import random
from node import *
import maze as mz

maze_path = "data/maze2.csv"
total_nodes = 20


def main():

    maze = mz.Maze( maze_path )
    deadends = [ int(key) for key in maze.nd_dict if ( maze.nd_dict[key].isEnd() ) ]
    previous_start_point, start_point = 1, 2

    #find the distances between deandends
    distances = maze.get_distances( start_point, deadends )
    
    #找出經過各deadend的順序
    path = maze.find_path( distances, start_point, deadends )

    #找出完整路徑
    full_path = [previous_start_point] + maze.find_full_path( path )
    print( full_path )

    #生成並寫入指令
    cmd = open('../bluetooth/cmd.txt', 'w+')
    maze.generate_cmd( cmd, full_path, deadends )

if __name__=='__main__':
    main()

