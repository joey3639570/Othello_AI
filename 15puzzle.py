from math import inf
from collections import deque
import random
import datetime

def move_prediction(inputs):
   # Move generator, takes in a state and the different possible next moves
   storage  =  []
   inputs = str(inputs)
   move = eval(inputs)
   '''
    xxx
    xxx    ->  [xxxxxxxxx]
    xxx
   '''

   i = 0
   while 0 not in move[i]: i += 1
   j = move[i].index(0);  # find zero

   # Sets boundary for the topmost cells.
   if i > 0:
       move[i][j], move[i - 1][j] = move[i - 1][j], move[i][j]
       storage.append(str(move))
       move[i][j], move[i - 1][j] = move[i - 1][j], move[i][j]

   # Sets boundary for the bottommost cells.
   if i < 3:
       move[i][j], move[i + 1][j] = move[i + 1][j], move[i][j]
       storage.append(str(move))
       move[i][j], move[i + 1][j] = move[i + 1][j], move[i][j]

   # Sets boundary for the rightmost cells.
   if j > 0:
       move[i][j], move[i][j - 1] = move[i][j - 1], move[i][j]
       storage.append(str(move))
       move[i][j], move[i][j - 1] = move[i][j - 1], move[i][j]

   # Sets boundary for the leftmost cells.
   if j < 3:
       move[i][j], move[i][j + 1] = move[i][j + 1], move[i][j]
       storage.append(str(move))
       move[i][j], move[i][j + 1] = move[i][j + 1], move[i][j]

   return storage

# Do random times move to the start matrix
def initialize(start,random_times):
    matrix = start
    for i in range(random_times):
        move = move_prediction(matrix)
        matrix = random.choice(move)
    print("Start by....")
    print(matrix)
    return matrix

# The main program, using the heuristic of the start case as the boundary for depth.
def idastar(start,finish,heuristic,cost):
    def search(path, g, bound, evaluated):
        evaluated += 1
        node = path[0]
        #print(node)
        f = g + heuristic(node,finish)
        if(f > bound):
            return f, evaluated
        if(node == str(finish)):
            return True, evaluated
        ret = inf
        moves = move_prediction(node)
        for m in moves:
            if m not in path:
                path.appendleft(m)
                t, evaluated = search(path, g + cost, bound, evaluated)
                if t is True:
                    return True, evaluated
                if t < ret:
                    ret = t
                path.popleft()
        return ret, evaluated
    bound = heuristic(start,finish)
    print("Bound first :: ",bound)
    path = deque([start])
    evaluated = 0
    while path:
        t, evaluated = search(path, 0, bound, evaluated)
        if t is True:
            path.reverse()
            return (True, path, {'space':len(path), 'time':evaluated})
        elif t is inf:
            return (False, [], {'space':len(path), 'time':evaluated})
        else:
            bound = t

# Used to flatten the matrix.
def flatten(matrix):
    matrix = str(matrix)
    matrix = eval(matrix)
    move = []
    for mat in matrix:
        move = move + mat
    return move

# Tiles out of place.
def hamming(candidate, solved, size=4): 
    res = 0
    move = flatten(candidate)
    finished = flatten(solved)
    for i in range(size*size):
        if move[i] != 0 and move[i] != finished[i]:
            res += 1
    return res

# Manhattan distance counter.
def manhattan(candidate, solved, size=4):
    res = 0
    move = flatten(candidate)
    finished = flatten(solved)
    for i in range(size*size):
        if move[i] != 0 and move[i] != finished[i]:
            ci = finished.index(move[i])
            y = (i // size) - (ci // size)
            x = (i % size) - (ci % size)
            res += abs(y) + abs(x)
    return res


def main():
    starttime = datetime.datetime.now()
    FINAL_STATE = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]] # Final matrix should look like this.
    test_state = [[2,5,3,4],[1,0,7,8],[9,6,11,12],[13,10,14,15]] # A case for testing.
    debug = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,0,15]] # Used to debug.
    trying = [[12,1,3,4],[2,13,14,5],[11,10,8,6],[9,15,7,0]] # A test case online, used for comparing the result.
    challenge = initialize(FINAL_STATE,200)
    #The number can be altered, the higher the number, the more random moves will be done to the original state.
    cost = 1
    success, steps, complexity = idastar(challenge,FINAL_STATE,manhattan,cost) # main function.
    print('space complexity:: ', complexity['space'], 'nodes in memory')
    print('time complexity:: ', complexity['time'], 'evaluated nodes')
    print('length of solution:: ', max(len(steps) - 1, 0))
    print('initial state and solution steps :: ')
    for s in steps:
        print(s)
    #c = manhattan(debug,FINAL_STATE)
    endtime = datetime.datetime.now()
    print('The search cost about .... ', (endtime - starttime).seconds, 'seconds.')
    print("Finished.")

if __name__ == '__main__':
    main()
