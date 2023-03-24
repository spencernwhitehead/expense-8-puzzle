import sys
from datetime import datetime

algo = 'a*'
if len(sys.argv) > 3:
    algo = sys.argv[3]

depthlim = 0

dump = False
outfile = None
if (len(sys.argv) > 4 and sys.argv[4] == 'true') or (len(sys.argv) > 3 and sys.argv[3] == 'true'):
    dump = True
    outfile = open(datetime.now().strftime('trace-%Y_%m_%d-%H_%M_%S')+'.txt', 'x')

nodesPopped = 0
nodesExpanded = 0
nodesGenerated = 1
maxFringe = 0

#initialize working grid and goal
currentGrid = [[0,0,0],[0,0,0],[0,0,0]]
goalGrid = [[0,0,0],[0,0,0],[0,0,0]]

#open files and apply info to grids
start = open(sys.argv[1])
goal = open(sys.argv[2])

startstr = start.read().replace('\n', '').replace(' ', '')
goalstr = goal.read().replace('\n', '').replace(' ', '')

for i in range(3):
    for j in range(3):
        currentGrid[i][j] = int(startstr[0])
        startstr = startstr[1:]
        goalGrid[i][j] = int(goalstr[0])
        goalstr = goalstr[1:]

#create node class for search
#includes grid state, depth, cost, parent, and children, which starts unexpanded
class node:
    state = 0
    depth = 0
    cost = 0
    parent = None
    step = ''
    h = 0
    children = []

    def __init__(self, state, depth, cost, parent, step):
        self.state = state
        self.depth = depth
        self.cost = cost
        self.parent = parent
        self.step = step
    
    def getInfo(self):
        if self.step != 'start':
            return '{state = ' + str(self.state) + ', d = ' + str(self.depth) + ', g(n) = ' + str(self.cost) + ', h(n) = ' + str(self.h) + ', step = ' + self.step + ', parent = ' + self.parent.getInfo() + '} '
        else:
            return '{state = ' + str(self.state) + ', d = ' + str(self.depth) + ', g(n) = ' + str(self.cost) + ', h(n) = ' + str(self.h) + ', step = ' + self.step + ', parent = { None } } '

#swap tiles on grid
#should only be used when one tile is zero and both are orthogonal
def gridswap(grid, a1, a2, b1, b2):
    newGrid = [[0,0,0],[0,0,0],[0,0,0]]
    for i in range(3):
        for j in range(3):
            newGrid[i][j] = grid[i][j]

    newGrid[a1][b1], newGrid[a2][b2] = newGrid[a2][b2], newGrid[a1][b1]
    return newGrid

#returns heuristic estimate cost
#takes manhattan distance and multiplies by tile value
def heuristic(grid):
    global goalGrid
    h = 0
    found = False
    for i in range(3):
        for j in range(3):
            for k in range(3):
                for l in range(3):
                    if grid[i][j] == goalGrid[k][l]:
                        h += (abs(i-k) + abs(j-l)) * grid[i][j]
                        found = True
                        break
                if found:
                    found = False
                    break
    return h         

def graphSearch(startNode):
    global nodesGenerated
    global nodesExpanded
    global nodesPopped
    global maxFringe
    global algo
    global depthlim

    #fringe starts off with only parent node
    fringe = [startNode]
    closed = []

    #loop until answer is found
    while(True):
        if len(fringe) > maxFringe:
            maxFringe = len(fringe)
        
        #get node at front of fringe and test for goal, return if success
        if len(fringe) == 0:
            return -1
        curNode = fringe.pop(0)
        nodesPopped = nodesPopped + 1

        if curNode.state in closed:
            continue
        closed.append(curNode.state)

        if curNode.state == goalGrid:
            return curNode
        
        #otherwise get children for node and add to fringe
        if dump:
            outfile.write('\ngenerating successors to ' + curNode.getInfo())

        curNode.children = expand(curNode)
        nodesExpanded = nodesExpanded + 1

        if dump:
            outfile.write('\n\t' + str(len(curNode.children)) + ' successors generated')

        for child in curNode.children:
            nodesGenerated = nodesGenerated + 1

            #FIFO
            if algo == 'bfs':
                fringe.append(child)

            #insert by cost
            elif algo == 'ucs':
                inserted = False
                for i in range(len(fringe)):
                    if child.cost < fringe[i].cost:
                        fringe.insert(i, child)
                        inserted = True
                        break
                if inserted == False:
                    fringe.append(child)

            #LIFO
            elif algo == 'dfs':
                fringe.insert(0,child)

            #conditional LIFO
            elif (algo == 'dls' or algo == 'ids'):
                if child.depth <= depthlim + 1:
                    fringe.insert(0,child)

            #insert by h(n)
            elif algo == 'greedy':
                inserted = False
                for i in range(len(fringe)):
                    if child.h < fringe[i].h:
                        fringe.insert(i, child)
                        inserted = True
                        break
                if inserted == False:
                    fringe.append(child)
            
            #default, insert by g(n) + h(n)
            else:
                inserted = False
                for i in range(len(fringe)):
                    if child.cost + child.h < fringe[i].cost + fringe[i].h:
                        fringe.insert(i, child)
                        inserted = True
                        break
                if inserted == False:
                    fringe.append(child)
        
        if dump:
            outfile.write('\n\tclosed: ' + str(closed))
            outfile.write('\n\tfringe:')
            for node in fringe:
                outfile.write('\n\t\t' + node.getInfo())

def expand(curNode):
    #get location of blank tile
    x = 0
    y = 0
    for i in range(3):
        for j in range(3):
            if curNode.state[i][j] == 0:
                x = i
                y = j

    #adds nodes to successors if blank tile can move in that direction
    #sets state to current state with blank tile swapped with whatever direction tile it's testing for
    #and sets cost to whatever tile it's swapping with
    #also I accidentally mixed up the x and y variables but it still works
    successors = []
    if x < 2:
        successors.append(node(gridswap(curNode.state, x, x+1, y, y), curNode.depth+1, curNode.state[x][y] + curNode.state[x+1][y] + curNode.cost, curNode, 'move '+str(curNode.state[x+1][y])+' up'))
    if x > 0:
        successors.append(node(gridswap(curNode.state, x, x-1, y, y), curNode.depth+1, curNode.state[x][y] + curNode.state[x-1][y] + curNode.cost, curNode, 'move '+str(curNode.state[x-1][y])+' down'))
    if y < 2:
        successors.append(node(gridswap(curNode.state, x, x, y, y+1), curNode.depth+1, curNode.state[x][y] + curNode.state[x][y+1] + curNode.cost, curNode, 'move '+str(curNode.state[x][y+1])+' left'))
    if y > 0:
        successors.append(node(gridswap(curNode.state, x, x, y, y-1), curNode.depth+1, curNode.state[x][y] + curNode.state[x][y-1] + curNode.cost, curNode, 'move '+str(curNode.state[x][y-1])+' right'))
    
    #calculates heuristic if using algorithm were it's needed
    if algo == 'a*' or algo == 'greedy':
        for i in range(len(successors)):
            successors[i].h = heuristic(successors[i].state)

    return successors

if __name__ == "__main__":
    startNode = node(currentGrid, 0, 0, None, 'start')

    if dump:
        outfile.write('cmd line args: ' + str(sys.argv))
        outfile.write('\nmethod selected: ' + algo)
        outfile.write('\nrunning ' + algo)
    
    goalNode = None

    if algo == 'dls':
        depthlim = int(input('enter depth limit: '))

    if algo == 'ids':
        while goalNode == None or goalNode == -1:
            goalNode = graphSearch(startNode)
            depthlim += 1
    else:
        goalNode = graphSearch(startNode)
        if goalNode == -1:
            print("couldn't find solution")
            quit() 

    print('nodes popped:', nodesPopped, '\nnodes expanded:', nodesExpanded, '\nnodes generated:', nodesGenerated, '\nmax fringe size:', maxFringe)
    print('solution found at depth', goalNode.depth, 'with cost of', goalNode.cost, '\nsteps:')

    steps = []
    tempNode = goalNode
    while(tempNode.step != 'start'):
        steps.insert(0, tempNode.step)
        tempNode = tempNode.parent
    for step in steps:
        print(step)