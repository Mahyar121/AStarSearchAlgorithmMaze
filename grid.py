import random

class Cell:
    def __init__(self, x, y, label='...', g=1, h=0):      # parent is not in the constructor, don't know if we want it to be
        self.label = label
        self.x = x  # x coordinate
        self.y = y  # y coordinate
        self.g = g  # cost to move from starting cell to this cell
        self.h = h  # estimation of the cost to move from this cell to goal cell
        self.f = g + h


class Agent:
    def __init__(self, startLocation, endLocation, currentLocation, totalCost=-1, stepsTaken=-1):
        self.startLocation = startLocation
        self.endLocation = endLocation
        self.currentLocation = currentLocation
        self.previousLocation = startLocation
        self.totalCost = totalCost
        self.stepsTaken = stepsTaken
        self.path = []


class AStar(Cell):
    def __init__(self):
        self.opened = []  # is the open list
        self.closed = []  # visited  list
        self.graph = []  # is our grid 20x20
        self.grid_height = 20
        self.grid_width = 20
        self.start = ()
        self.end = ()


    def init_grid(self, startLocation, endLocation, quicksandLocation, netLocation, tollLocation): # start --> (x,y)
        # Creates a graph as a list
        #   Ex) If 4x4 grid of just coordinates:
        #   graph = [[(0, 0), (0, 1), (0, 2), (0, 3)], [(1, 0), (1, 1), (1, 2), (1, 3)], [(2, 0), (2, 1), (2, 2), (2, 3)], [(3, 0), (3, 1), (3, 2), (3, 3)]]
        #       where list could be looked at as having rows and columns
        self.graph = [[Cell(x,y) for y in range(self.grid_width)] for x in range(self.grid_height)]
        
        # Then iterate through qicksand, spiderweb, and toll lists  
        # and updates graph cells to be populated with appropriate values
        
        self.start = startLocation
        x,y = startLocation
        self.graph[x][y] = Cell(x,y,'Start')
        
        self.end = endLocation
        x,y = endLocation
        self.graph[x][y] = Cell(x,y,'End')
        
        #populating graph with quicksand
        for i in range(len(quicksandLocation)):
            x,y = quicksandLocation[i]
            self.graph[x][y] = Cell(x,y,'Quicksand',50)   
        
        #populating graph with spiderwebs
        for i in range(len(netLocation)):
            x,y = netLocation[i]
            self.graph[x][y] = Cell(x,y,'Center Web',100) # We can make the trap values whatever we want.
            # This extends the web locations and places them on the graph
            if x-1 >= 0:
                self.graph[x-1][y] = Cell(x-1,y,'Extended Web',100)
            if y-1 >= 0:
                self.graph[x][y-1] = Cell(x,y-1,'Extended Web',100)
            if x+1 <= (self.grid_height - 1):
                self.graph[x+1][y] = Cell(x+1,y,'Extended Web',100)
            if y+1 <= (self.grid_height - 1):
                self.graph[x][y+1] = Cell(x,y+1,'Extended Web',100)

        
        #populating graph with tolls
        val = tollLocation.keys()
        for i in val:
            x,y = tollLocation[i]
            self.graph[x][y] = Cell(x,y,'Toll',i)   # since tollLocation is a dictionary, i represents the key which is
        print()
        
        
    def get_heuristic(self, neighbor): # need to worry about other values
        # this function just calculates the heuristic value H for the cell, we find the distance between cell and goal cell, then * by D value
        return 1 * (abs(neighbor[0] - self.end[0]) + abs(neighbor[1] - self.end[1]))  # need to figure out D value, maybe 1 since g is 1
    

    def get_neighbor_cells(self, cell):  # made the neighbor cells have a combined F value down in update cells and tiebreaker, so this function is all good :D
        neighborCells = []
        x,y = cell
        
        if x < (self.grid_height - 1):
            neighborCells.append((x+1, y))
        if y > 0:
            neighborCells.append((x, y-1))
        if x > 0:
            neighborCells.append((x-1, y))
        if y < (self.grid_height - 1):
            neighborCells.append((x, y+1))
        return neighborCells
    
    
    def update_cell(self, next_potential_move, agentLocation):
        x,y = next_potential_move
        self.graph[x][y].h = self.get_heuristic(next_potential_move)   
        self.graph[x][y].f = self.graph[x][y].g + self.graph[x][y].h


    def move(self, agent):
        self.opened.append((self.graph[self.start[0]][self.start[1]].f, self.start))
        agentLocation = agent.startLocation
        while self.opened: # while it is not empty and not at end
            #### pick smallest f value from self.opened and move to that location
            agent.previousLocation = agentLocation
            f,agentLocation = min(self.opened)
            x,y = agentLocation
            agent.stepsTaken = agent.stepsTaken + 1
            agent.totalCost = agent.totalCost + self.graph[x][y].g 
            agent.currentLocation = agentLocation
            agent.path.append(agentLocation)
            self.opened = []

            if agentLocation == agent.endLocation:  
                return agent.path
            
            #### find neighbors and get their f value
            neighbor_cells = self.get_neighbor_cells(agentLocation) # get neighbor agentLocations
            ## check cell's f values and go in smallest direction
            for next_potential_move in neighbor_cells:
                self.update_cell(next_potential_move, agentLocation)
                x,y = next_potential_move
                self.opened.append((self.graph[x][y].f, next_potential_move))
            
            if agent.stepsTaken > 0:
                #Remove previous location from Open List
                #Calculate new lowest F value using min(self.opened) without PREVIOUS LOCATION
                for i in range(len(self.opened)):
                    if agent.previousLocation == self.opened[i][1]:         # always going to be true
                        self.opened.remove(self.opened[i])
                        break
                
                #compare previousLocation.f and min(neighbor_cells).f
                x,y = agent.previousLocation
                f,coordinate = min(self.opened)
                
                for i in range(len(self.closed)):
                    if agent.previousLocation == self.closed[i]:        # if we have backtracked once already the previous move
                        break
                
                    if self.graph[x][y].f < f:              # if we want to backtrack
                        self.opened.append((self.graph[x][y].f, agent.previousLocation))    # put (23, (2,3)) in opened
                        self.closed.append(agent.previousLocation)                          # put (23, (2,3)) in closed
