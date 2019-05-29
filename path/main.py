import random
from node import *
import maze as mz

maze_path = "data/maze3.csv"
cmd_path = "../bluetooth/cmd_g_backup.txt"
total_nodes = 38 


def main():

    maze = mz.Maze( maze_path )

    maze.draw_map( total_nodes )

    deadends = [ int(key) for key in maze.nd_dict if ( maze.nd_dict[key].isEnd() ) ]
    previous_start_point, start_point = 1, 5
    deadends.remove( 15 )
    deadends.append( 15 )
    print( deadends )

    #find the distances between deandends
    distances = maze.get_distances( start_point, deadends )
    print( "get_distances" )
    
    #找出經過各deadend的順序
    path = maze.find_path( distances, start_point, deadends )
    print( path )
    #path = [ 5, 11, 18, 25, 35, 38 ]

    #找出完整路徑
    full_path = [previous_start_point] + maze.find_full_path( path )
    print( full_path )

    #生成並寫入指令
    #cmd = open('../bluetooth/cmd.txt', 'w+')
    cmd = open( cmd_path, 'w+')
    maze.generate_cmd( cmd, full_path, deadends )

if __name__=='__main__':
    main()

