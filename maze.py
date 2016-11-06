#!/usr/bin/env python3

'''
CPSC 481
Assignment 1
Maze

Python 3.5

Modified 7/23/16


'''


import sys
import ast
from grid import Cell   # from filename import className
from grid import AStar
from grid import Agent


# For Debug
#Prints all cells from graph
def printCell(self):
    for x in range(len(self.graph)):
        for y in range(len(self.graph)):    
            print('Label: ', self.graph[x][y].label)
            print('x,y: ({},{})'.format(self.graph[x][y].x, self.graph[x][y].y))
            print('{} = {} + {} '.format(self.graph[x][y].f,self.graph[x][y].g,self.graph[x][y].h))
            print()
    print('len(graph): ', len(self.graph))
    print()
    
    
def printAgentInfo(self):
    print('### Agent Info ###')
    print('Current Location: {}'.format(self.currentLocation))
    print('Steps Taken: {}'.format(self.stepsTaken))
    print('Total Cost: {}'.format(self.totalCost))
    print()


def main ():
    
    finalPath = []
    
    ### This gives us:
    ### start and end as tuples --> (x,y) 
    ### quicksandLocation and netLocation as lists --> [(x,y), (x,y)]
    ### toll as dictionary --> {value:(x,y), value:(x,y)}
    
    with open(sys.argv[-1], 'r') as f:
        startLocation = f.readline()
        startLocation = ast.literal_eval(startLocation)
        
        
        endLocation = f.readline()
        endLocation = ast.literal_eval(endLocation)
        
        
        quicksandLocation = f.readline()
        quicksandLocation = quicksandLocation.split()
        for i in range(len(quicksandLocation)):
            quicksandLocation[i] = ast.literal_eval(quicksandLocation[i])
            
            
        netLocation = f.readline()
        netLocation = netLocation.split()
        for i in range(len(netLocation)):
            netLocation[i] = ast.literal_eval(netLocation[i])
        # Implemented extended net locations in the init_grid() function.
        
        
        tollLocation = f.readline().strip().split()
        tollLocation = ','.join(tollLocation)
        tollLocation = '{' + tollLocation + '}'
        tollLocation = ast.literal_eval(tollLocation)
        

    ### The above code reads from file and creates tuples, 
    ### lists, and dictionary similar to below.
    ### startLocation = (2,3)
    ### endLocation = (19,10)
    ### quicksandLocation = [(0,0), (5,5), (15,15)]
    ### netLocation = [(10,10), (17,8)]
        # Spiderweb has expanded web values are implemented in init_grid() function
    ### tollLocation = {2:(1,3), 10:(3,3), 7:(10,15), 200:(19,9)}
    

    # Create AStar object with start and end locations
    agentObj = Agent(startLocation, endLocation, startLocation)
    mazeObj = AStar()
    #printAgentInfo(agentObj)
    
    # Initialize the grid with all trap locations. Start and end locations are not designated on grid, only to object.
    mazeObj.init_grid(startLocation, endLocation, quicksandLocation, netLocation, tollLocation)
    
    #printCell(mazeObj)
    ##Just messing around with converting the Neighbor list to a list of Objects
    #temp = mazeObj.get_neighbor_cells(startLocationObj)
    
    # Hope for the best...
    finalPath = mazeObj.move(agentObj)
    #printAgentInfo(agentObj)

    print('###################################################')
    print('Total cost: ${}'.format(agentObj.totalCost))
    print('Total number of steps taken: {}'.format(agentObj.stepsTaken))
    print('Traveled route: {}'.format(finalPath))
    print('###################################################')
    
    with open("output.txt", "wt") as out_file:
        out_file.write('Total cost: ${}\n'.format(agentObj.totalCost))
    #print('Total cost: ${}'.format(mazeObj.cost))
        out_file.write('Total number of steps taken: {}\n'.format(agentObj.stepsTaken))
    #print('Total number of steps taken: {}'.format(mazeObj.steps))
        out_file.write('Traveled route: {}\n'.format(finalPath))
    #print('Traveled route: {}'.format(finalPath))
    
    #out_file.close()


if __name__ == '__main__':
    main( )

'''
Total cost: $25
Total number of steps taken: 25
Traveled route: 
    [[2, 3], [3, 3], [3, 4], [3, 5], [3, 6], 
    [3, 7], [3, 8], [4, 8], [5, 8], [6, 8],
    [7, 8], [8, 8], [9, 8], [10, 8], [11, 8], 
    [12, 8], [13, 8], [14, 8], [15, 8], [16, 8],
    [16, 9], [16, 8], [17, 9], [18, 9], [18, 8], [19, 8]]


Total cost: $26
Total number of steps taken: 26
Traveled route: 
    [(2, 3), (3, 3), (3, 4), (3, 5), (3, 6), 
     (3, 7), (3, 8), (4, 8), (5, 8), (6, 8), 
     (7, 8), (8, 8), (9, 8), (10, 8), (11, 8), 
     (12, 8), (13, 8), (14, 8), (15, 8), (15, 7), 
     (16, 7), (16, 6), (17, 6), (18, 6), (18, 7), 
     (19, 7), (19, 8)]
     
     
     
Total cost: $50
Total number of steps taken: 36
Traveled route: 
    [(2, 3), (1, 3), (0, 3), (0, 4), (0, 5),
     (0, 6), (0, 7), (0, 8), (0, 9), (0, 10),
     (0, 11), (0, 12), (0, 13), (0, 14), (0, 15),
     (0, 16), (0, 17), (0, 18), (1, 18), (2, 18),
     (3, 18), (4, 18), (5, 18), (6, 18), (7, 18), 
     (8, 18), (9, 18), (10, 18), (11, 18), (12, 18), 
     (13, 18), (14, 18), (15, 18), (16, 18), (17, 18), 
     (18, 18), (19, 18)]
'''