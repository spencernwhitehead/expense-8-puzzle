# expense-8-puzzle
Assignment 1 for CSE4360 Artificial Intelligence

ORIGINAL ASSIGNMENT DESCRIPTION:

Your task is to build an agent to solve a modifed version of the 8 puzzle problem (called the Expense 8 puzzle problem). The task is still to take a 3X3 grid on which 8 tiles have been placed, where you can only move one tile at a time to an adjacent location (as long as it is blank) and figure out the order in which to move the tiles to get it to a desired configuration. However now the number on the tile now also represents the cot of moving that tile (moving the tile marked 6 costs 6).

Your program should be called expense_8_puzzle and the command line invocation should follow the following format:

expense_8_puzzle.py <start-file> <goal-file> <method> <dump-flag>

    <start-file> and <goal-file> are required.
     <method> can be
         bfs - Breadth First Search
        ucs - Uniform Cost Search
        dfs - Depth First Search
        dls - Depth Limited Search (Note: Depth Limit will be obtained as a Console Input) [Note: This part is EC for CSE 4308 students]
        ids - Iterative Deepening Search [Note: This part is EC for CSE 4308 students]
        greedy - Greedy Seach
        a* - A* Search (Note: if no <method> is given, this should be the default option)
    If <dump-flag>  is given as true, search trace is dumped for analysis in trace-<date>-<time>.txt (Note: if <dump-flag> is not given, assume it is false)
        search trace contains: fringe and closed set contents per loop of search(and per iteration for IDS), counts of nodes expanded and nodes

ORIGINAL README:

Spencer Whitehead
Python 3.11.1

structure:
	the program starts with setting up various global variables and reads the files and assigns them to arrays
	node class is defined
	function gridswap is defined to be able to manipulate the grid
	function heuristic is defined, takes manhattan distance for each tile and multiplies by value of tile
	graphSearch function implements search functionality, takes node from fringe, checks if in closed,
		expands otherwise, takes children and adds them to fringe
		the way the children are added depends on chosen algorithm, and every algorithm can be chosen
		including the extra credit ones
	the expand function finds every direction a tile can be moved with the current grid, and creates new child
		nodes based on those valid directions and returns them in a list
	the last part of the program is the main function, which calls the graphsearch function and prints the
		information for the output when the goal node is found
	

you can run the program with the following command:
py <path to file>/expense_8_puzzle.py <start-file> <goal-file> <method> <dump-flag : "true" | "false>
