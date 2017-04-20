import argparse
from collections import defaultdict
from Queue import Queue
from State import State

class ThreeDigits():

    # Used to remove mutators based upon last state
    DIGIT_ONE = 1
    DIGIT_TWO = 3
    DIGIT_THREE = 5

    def __init__(self, search_algorithm, start_state, end_state, forbidden_states):
        # Initalise the search algorithm to use
        self.search_algorithm = search_algorithm
        # Initalise the start, end and forbidden states
        self.start_state = start_state
        self.end_state = end_state
        self.forbidden_states = forbidden_states
        # obtain search path states
        self.search_path = []
        # keep track of visited states
        self.visited = []


    # Function to get all the valid children of a state
    def get_children_states(self, state, parent_state):
        # Create a list of mutator helpers
        mutators = [-100,100,-10,10,-1,1]
        if parent_state:
            # remove last updated digit mutators
            del mutators[self.last_update(state, parent_state) - 1]
            del mutators[self.last_update(state, parent_state) - 1]
        # store children in list to be returned
        children = []
        # loop through the leftover mutators and mutate the state, adding it to
        # the list of children if it is a valid new state
        for mutator in mutators:
            new_state = state + mutator
            if new_state not in self.forbidden_states and (new_state, state) not in self.visited:
                # convert state into string to add extra 0's to check validity
                state_str = str(state)
                if len(state_str) == 2:
                    state_str = '0' + state_str
                elif len(state_str) == 1:
                    state_str = '00' + state_str

                if mutator < 0:
                    # check if digit being mutated is not 0
                    if int(state_str[abs(len(str(abs(mutator))) - 3) % 3]) != 0:
                        children.append(new_state)
                else:
                    # check if digit being mutated is not 9
                    if int(state_str[abs(len(str(abs(mutator))) - 3) % 3]) != 9:
                        children.append(new_state)
        return children


    # Function to call the requested search algorithm
    def solve(self):
        # run requested search algorithm populating the visited and expanded lists
        if (self.search_algorithm == 'B'):
            self.BFS()
            self.path(self.end_state)
        elif (self.search_algorithm == 'D'):
            self.DFS()
        elif (self.search_algorithm == 'I'):
            self.IDS()
        elif (self.search_algorithm == 'G'):
            self.greedy()
        elif (self.search_algorithm == 'A'):
            self.aStar()
        elif (self.search_algorithm == 'H'):
            self.hillClimbing()
        else:
            raise TypeError('The letter entered doesn\'t represent any search algorithm.')
        # return visited and expanded states
        return self.toString()


    def last_update(self, state, parent_state):
        if abs(state - parent_state) == 100:
            return self.DIGIT_ONE
        elif abs(state - parent_state) == 10:
            return self.DIGIT_TWO
        else:
            return self.DIGIT_THREE


    # recursively find search path
    def path(self, end_state):
        if end_state == None:
            return
        for state in self.visited:
            if state[0] == end_state:
                self.search_path.insert(0, state[0])
                self.path(state[1])
                return


    # Implementation of the breadth first search algorithm
    def BFS(self):
        # keep a queue for BFS
        queue = Queue()

        # enqueue the start state to the queue as a tuple (state, parent_state)
        queue.enqueue(State(self.start_state))

        # keep looping whilst there's still states in the queue
        while queue.is_empty() != True:
            # dequeue next state and add it to visited
            current_state = queue.front().get_state()
            parent_state = queue.dequeue().get_parent()
            children_states = self.get_children_states(current_state, parent_state)
            self.visited.append((current_state, parent_state))

            # add current states children states to the queue
            for child_state in children_states:
                queue.enqueue(State(child_state, current_state))

            # check if end state is found
            if current_state == self.end_state:
                # end state found
                return


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


    # convert visited and expanded lists to string to be returned
    def toString(self):
        # visited -- convert integers to strings and add 0's to non 3-digit numbers
        # then append values together with commas
        visited = ["0" + state if len(state) == 2 else state for state in list(map(str, [state_tuple[0] for state_tuple in  self.visited]))]
        visited = ["00" + state if len(state) == 1 else state for state in visited]
        visited = ','.join(visited)
        # path -- convert integers to strings and add 0's to non 3-digit numbers
        # then append values together with commas
        if len(self.search_path) == 0:
            path = "No solution found."
        else:
            path = ["0" + state if len(state) == 2 else state for state in list(map(str, self.search_path))]
            path = ["00" + state if len(state) == 1 else state for state in path]
            path = ','.join(path)
        # return search path + visited lists as a string
        return path + '\n' + visited


def main():
    # Parse in the command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('search_algorithm', help='A single letter representing the algorithm to search with, out of B for BFS, D for DFS, I for IDS, G for Greedy, A for A*, H for Hill Climbing.')
    parser.add_argument('input_file', help='A filename of a file to open for the search details.')
    args = parser.parse_args()

    # Parse in the input file
    with open(args.input_file) as input_file:
        content = [line.strip() for line in input_file.readlines()]
    start_state = int(content[0])
    end_state = int(content[1])
    if len(content) == 3:
        # there are forbidden states, insert them in a list
        forbidden_states = list(map(int, content[2].split(',')))
    else:
        forbidden_states = []

    # Create a ThreeDigits object
    threeDigitsSolver = ThreeDigits(args.search_algorithm, start_state, end_state, forbidden_states)
    # Call solve to get a string with the visited and expanded states
    output = threeDigitsSolver.solve()

    # Write the solution to the output file
    # with open('output.txt', mode='wt') as output_file:
    #     output_file.write(output)
    print(output)


if __name__ == '__main__':
    main()
