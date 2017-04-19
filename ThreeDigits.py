import argparse
from collections import defaultdict
from Queue import Queue

class ThreeDigits():

    # Member variables
    search_algorithm
    search_tree
    start_state
    end_state
    forbidden_states
    last_update

    # Constants
    VALID_RANGE = range(0,999)

    def __init__(self, search_algorithm, start_state, end_state, forbidden_states):
        # Initalise the search algorithm to use
        self.search_algorithm = search_algorithm
        # Initalise the start, end and forbidden states
        self.start_state = start_state
        self.end_state = end_state
        self.forbidden_states = forbidden_states
        # Initalise the search tree
        self.search_tree = defaultdict(list)
        self.search_tree[]
        # Store the index of the last updated digit e.g. 1, 2 or 3 representing
        # the first, second and third digits
        self.last_update = None


    # Function to add a state to search tree
    def add_state(self, state):
        self.search_tree[state].append(1)


    # Function to get all the valid children of a state
    def get_children(self, state):
        # Create a list of helpers to mutate the state for the previously updated
        mutators = [-100,100,-10,10,-1,1]
        if last_update:
            del mutators[last_update - 1]
            del mutators[last_update]
        children = []
        # loop through the leftover mutators and mutate the state, adding it to
        # the list of children if it is a valid new state
        for mutator in mutators:
            new_state = state + h
            if new_state not in self.search_tree and new_state in self.VALID_RANGE:
                children.append(new_state)
        return children


    # Function to call the requested search algorithm
    def solve(self):
        if (self.search_algorithm == 'B'):
            return BFS()
        elif (self.search_algorithm == 'D'):
            return DFS()
        elif (self.search_algorithm == 'I'):
            return IDS()
        elif (self.search_algorithm == 'G'):
            return greedy()
        elif (self.search_algorithm == 'A'):
            return aStar()
        elif (self.search_algorithm == 'H'):
            return hillClimbing()
        else:
            raise TypeError('The letter entered doesn\'t represent any search algorithm.')


    # Implementation of the breadth first search algorithm
    def BFS(self):
        # keep track of states added to search path
        visited = []

        # keep track of expanded states
        expanded = [start_state]

        # keep a queue for BFS
        queue = Queue()

        # enqueue the start state to the queue
        queue.enqueue(start_state)

        # keep looping whilst there's still states in the queue
        while queue:
            # dequeue next state and add it to visited
            current_state = queue.dequeue()
            visited.append(current_state)

            # get current states children states and add them to expanded
            for child in get_children(current_state):
                queue.enqueue(child)
                expanded.append(child)

            # check if end state is found
            if current_state == self.end_state:
                # end state found
                return [visited, expanded]


    # Implementation of the depth first search algorithm
    def DFS(self):
        pass


    # Implementation of the iterative deepening search algorithm
    def IDS(self):
        pass


    # Implementation of the greedy search algorithm
    def greedy(self):
        pass


    # Implementation of the A* search algorithm
    def aStar(self):
        pass


    # Implementation of the hill climbing search algorithm
    def hillClimbing(self):
        pass


def main():
    # Parse in the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('algo', help='A single letter representing the algorithm to search with, out of B for BFS, D for DFS, I for IDS, G for Greedy, A for A*, H for Hill Climbing.')
    parser.add_argument('file', help='A filename of a file to open for the search details.')
    args = parser.parse_args()

    # Parse in the input file
    with open(args.file) as input_file:
        content = [line.strip() for line in input_file.readlines()]
    start_state = int(content[0])
    end_state = int(content[1])
    if len(content) == 3:
        # there are forbidden states
        forbidden_states = list(map(int, content[2].split(',')))
    else:
        forbidden_states = None

    # Create a ThreeDigits object
    threeDigitsSolver = ThreeDigits(args.algo, start_state, end_state, forbidden_states)
    # Call solve which will return a list with two values, firstly a list of the
    # solution path and secondly a list of the expanded nodes
    output = threeDigitsSolver.solve()

    # Write the results to the output file -- needs work
    with open('output.txt', mode='wt') as output_file:
        output_file.write(','.join(output[0]))
        output_file.write(','.join(output[1]))


if __name__ == '__main__':
    main()
