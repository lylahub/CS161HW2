# Q1 BFS
# input: takes in tree
# output: tuple of leaf nodes in order of left-to-right breadth-first search
def BFS(TREE):
    # root only tree
    if type(TREE) != tuple:
        return (TREE, )
    # use queue for the tree structure
    tree_queue = [TREE]
    search_result = ()
    while tree_queue:
        node = tree_queue.pop(0)
        for subtree in node:
            if type(subtree) == tuple:
                tree_queue.append(subtree)
            else:
                search_result += (subtree, )
    return search_result


# Q2 DFS
# input: tree
# output: tuple of leaf nodes in the order of left-to-right depth-first search
def DFS(TREE):
    # root only tree
    if type(TREE) != tuple:
        return (TREE, )
    # use tuple to store result
    search_result = ()
    for subtree in TREE:
        # apply DFS on each subtree recursively
        search_result += DFS(subtree)
    return search_result


# Q3 DFID
# aux_DFID
# input: TREE with max_depth = depth
# output: tuple of leaf nodes from right-to-left DFS with maximum depth = depth
def aux_DFID(TREE, depth):
    if depth < 0:
        return ()
    if type(TREE) != tuple:
        return (TREE, )
    search_result = ()
    for subtree in reversed(TREE):
        search_result += aux_DFID(subtree, depth-1)
    return search_result

# DFID
def DFID(TREE, depth):
    search_result = ()
    for d in range(depth + 1):
        search_result += aux_DFID(TREE, d)
    return search_result


# Q4
# These functions implement a depth-first solver for the homer-baby-dog-poison
# problem. In this implementation, a state is represented by a single tuple
# (homer, baby, dog, poison), where each variable is True if the respective entity is
# on the west side of the river, and False if it is on the east side.
# Thus, the initial state for this problem is (False False False False) (everybody
# is on the east side) and the goal state is (True True True True).

# The main entry point for this solver is the function DFS_SOL, which is called
# with (a) the state to search from and (b) the path to this state. It returns
# the complete path from the initial state to the goal state: this path is a
# list of intermediate problem states. The first element of the path is the
# initial state and the last element is the goal state. Each intermediate state
# is the state that results from applying the appropriate operator to the
# preceding state. If there is no solution, DFS_SOL returns [].
# To call DFS_SOL to solve the original problem, one would call
# DFS_SOL((False, False, False, False), [])
# However, it should be possible to call DFS_SOL with any intermediate state (S)
# and the path from the initial state to S (PATH).

# First, we define the helper functions of DFS_SOL.

# FINAL_STATE takes a single argument S, the current state, and returns True if it
# is the goal state (True, True, True, True) and False otherwise.
def FINAL_STATE(S):
    """
    Check if the current state is the goal state
    
    Input:
        S (tuple): position of Homer, baby, dog, and poison
    
    Output:
        bool: Returns True if the current state is the goal state,
              indicating all entities are on the west side of the river
    
    """
    if S == (True, True, True, True):
        return True
    return False


# NEXT_STATE returns the state that results from applying an operator to the
# current state. It takes two arguments: the current state (S), and which entity
# to move (A, equal to "h" for homer only, "b" for homer with baby, "d" for homer
# with dog, and "p" for homer with poison).
# It returns a list containing the state that results from that move.
# If applying this operator results in an invalid state (because the dog and baby,
# or poisoin and baby are left unsupervised on one side of the river), or when the
# action is impossible (homer is not on the same side as the entity) it returns [].
# NOTE that NEXT_STATE returns a list containing the successor state (which is
# itself a tuple)# the return should look something like [(False, False, True, True)].
def NEXT_STATE(S, A):
    """
    Calculate the next state resulting from moving a specified entity across the river

    Input:
        S (tuple): The current state tuple (homer, baby, dog, poison) indicating which side
                   (True for west, False for east) each entity is on
        A (str): The action specifying which entity or entities to move, with possible values:
                 'h' for Homer alone, 'b' for Homer with the baby, 'd' for Homer with the dog,
                 and 'p' for Homer with the poison

    Output:
        list of tuple: Returns a list containing the new state tuple after the move. If the move
                       is invalid or impossible due to safety rules or because entities are not
                       on the same side, it returns an empty list ([])
    """
    homer, baby, dog, poison = S
    if A == 'h':
        # Homer moves
        if (baby == dog == (not homer)) or (baby == poison == (not homer)):
            return []
        return [(not homer, baby, dog, poison)]
    elif A == 'b':
        # Homer + baby
        if homer != baby:
            return []
        return [(not homer, not baby, dog, poison)]
    elif A == 'd':
        # Homer + dog
        if homer != dog:
            return []
        # moving the dog should not leave the baby with poison alone
        if baby == poison and baby != homer:
            return []
        return [(not homer, baby, not dog, poison)]
    elif A == 'p':
        # Homer + poison
        if homer != poison:
            return []
        # moving poison should not leave the baby with the dog alone
        if baby == dog and baby != homer:
            return []
        return [(not homer, baby, dog, not poison)]
    return []


# SUCC_FN returns all of the possible legal successor states to the current
# state. It takes a single argument (S), which encodes the current state, and
# returns a list of each state that can be reached by applying legal operators
# to the current state.
def SUCC_FN(S):
    """
    Generate all possible legal successor states from the current state in the 
    homer-baby-dog-poison river crossing problem

    Input:
        S (tuple): The current state tuple (homer, baby, dog, poison), where each element
                   represents the presence of the respective entity on the west side of 
                   the river (True for west, False for east)

    Output:
        list of tuples: A list of all legal states that can be reached from the current state
                        by applying one of the allowable moves. Each state is represented as 
                        a tuple (homer, baby, dog, poison)
    """
    possible_legal_successor_states = []
    for move in ('h', 'b', 'd', 'p'):
        # Get the next state for the current move, returns a list of states
        possible_state = NEXT_STATE(S, move)
        # If there are valid next states, extend the list
        if possible_state:
            possible_legal_successor_states.extend(possible_state)
    return possible_legal_successor_states


# ON_PATH checks whether the current state is on the stack of states visited by
# this depth-first search. It takes two arguments: the current state (S) and the
# stack of states visited by DFS (STATES). It returns True if S is a member of
# STATES and False otherwise.
def ON_PATH(S, STATES):
    """
    Check if the current state is already in the list of states visited during
    the depth-first search

    Input:
        S (tuple): The current state to be checked. The state is a tuple like
                   (homer, baby, dog, poison) indicating the side (True for west,
                   False for east) of the river each entity is on
        STATES (list of tuples): A stack of states that represents the path of
                   states visited so far in the depth-first search

    Output:
        bool: Returns True if the state `S` is already in the `STATES` list, indicating
              that this state has been visited in the current path of the DFS. Returns
              False if the state `S` is not found in `STATES`, indicating that it has
              not been visited in the current search path
    """
    if S in STATES:
        return True
    return False


# MULT_DFS is a helper function for DFS_SOL. It takes two arguments: a list of
# states from the initial state to the current state (PATH), and the legal
# successor states to the last, current state in the PATH (STATES). PATH is a
# first-in first-out list of states# that is, the first element is the initial
# state for the current search and the last element is the most recent state
# explored. MULT_DFS does a depth-first search on each element of STATES in
# turn. If any of those searches reaches the final state, MULT_DFS returns the
# complete path from the initial state to the goal state. Otherwise, it returns
# [].
def MULT_DFS(STATES, PATH):
    """
    Perform a multi-branch DFS from multiple starting points to find a path to the goal state

    Inputs:
        STATES (list of tuples): A list of legal successor states from the current end state of the path

        PATH (list of tuples): A stack (first-in, first-out list) of states from the initial state to the 
                               most recently explored state

    Output:
        list of tuples: If a path to the goal state is found through any of the successors, returns the 
                        complete path including the initial state and the goal state
    """
    for state in STATES:
        # curr_state = goal state
        if FINAL_STATE(state):
            return PATH + [state]
        # no cycle: recursively search from these successors
        if state not in PATH:
            successor_states = SUCC_FN(state)
            new_path = MULT_DFS(successor_states, PATH + [state])
            if new_path:
                return new_path
    # return an empty list for no path
    return []


# DFS_SOL does a depth first search from a given state to the goal state. It
# takes two arguments: a state (S) and the path from the initial state to S
# (PATH). If S is the initial state in our search, PATH is set to []. DFS_SOL
# performs a depth-first search starting at the given state. It returns the path
# from the initial state to the goal state, if any, or [] otherwise. DFS_SOL is
# responsible for checking if S is already the goal state, as well as for
# ensuring that the depth-first search does not revisit a node already on the
# search path (i.e., S is not on PATH).
def DFS_SOL(S, PATH):
    """
    Perform a depth-first search (DFS) from a specified state to the goal state

    Inputs:
        S (tuple): The current state from which to start the DFS, represented as a tuple
                   (homer, baby, dog, poison)
                   
        PATH (list of tuples): The path from the initial state to the current state `S`. 
                               used to track the route taken in the DFS to prevent cycles
                               If `S` is the initial state, PATH should be empty []

    Output:
        list of tuples: Returns the path from the initial state to the goal state if a valid
                        route is found
    """
    if FINAL_STATE(S):
        return PATH + [S]
    # no revisiting
    if ON_PATH(S, PATH):  
        return []
    # explore successor states of S
    successor_states = SUCC_FN(S)
    return MULT_DFS(successor_states, PATH + [S])
