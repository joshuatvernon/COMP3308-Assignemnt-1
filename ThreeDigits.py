import argparse
from collections import defaultdict
from Queue import Queue
from State import State

class ThreeDigits():

    def __init__(self, search_algorithm, start_state, goal_state, forbidden_states):
        # Initalise the search algorithm to use
        self.search_algorithm = search_algorithm
        # Initalise the start, end and forbidden states
        self.start_state = State(start_state, State(None))
        self.goal_state = State(goal_state)
        self.forbidden_states = forbidden_states
        # obtain search path states
        self.search_path = []
        # keep track of visited states
        self.visited = []
        # keep track of expanded states
        self.expanded = []


    # Function to call the requested search algorithm
    def solve(self):
        # run requested search algorithm populating the visited and expanded lists
        if (self.search_algorithm == 'B'):
            self.BFS()
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
        # return search path and visited states
        return self.toString()


    # Function to get all the valid children of a state
    def get_children_states(self, state, parent_state):
        # Create a list of mutator helpers
        mutators = [-100,100,-10,10,-1,1]
        if parent_state.get_state() != None:
            # remove last updated digit mutators
            del mutators[self.last_update(state, parent_state)]
            del mutators[self.last_update(state, parent_state)]
        # store children in list to be returned
        children = []
        # loop through the leftover mutators and mutate the state, adding it to
        # the list of children if it is a valid new state
        for mutator in mutators:
            new_state = State(state.get_state() + mutator, state)
            if new_state.get_state() not in self.forbidden_states and (new_state.get_state(), self.last_update(new_state, state)) not in self.expanded:
                # convert state into string to add extra 0's to check validity
                state_str = str(state.get_state())
                if len(state_str) == 2:
                    state_str = '0' + state_str
                elif len(state_str) == 1:
                    state_str = '00' + state_str
                # check for 0's and 9's
                if mutator < 0:
                    # check if digit being mutated is not 0
                    if int(state_str[abs(len(str(abs(mutator))) - 3) % 3]) != 0:
                        children.append(new_state)
                else:
                    # check if digit being mutated is not 9
                    if int(state_str[abs(len(str(abs(mutator))) - 3) % 3]) != 9:
                        children.append(new_state)
        return children


    # Return an index used to remove mutators based upon last state
    def last_update(self, state, parent_state):
        if abs(state.get_state() - parent_state.get_state()) == 100:
            return 0
        elif abs(state.get_state() - parent_state.get_state()) == 10:
            return 2
        else:
            return 4


    # The Manhattan heuristic for a move between two numbers A and B is the sum of the absolute
    # differences of the corresponding digits of these numbers
    def manhattan_heuristic(self, A, B):
        a, b = [0,0,0], [0,0,0]

        # get A's digits
        if len(str(A.get_state())) == 3:
            a[0] = int(str(A.get_state())[0])
            a[1] = int(str(A.get_state())[1])
            a[2] = int(str(A.get_state())[2])
        elif len(str(A.get_state())) == 2:
            a[1] = int(str(A.get_state())[0])
            a[2] = int(str(A.get_state())[1])
        else:
            a[2] = A.get_state()

        # get B's digits
        if len(str(B.get_state())) == 3:
            b[0] = int(str(B.get_state())[0])
            b[1] = int(str(B.get_state())[1])
            b[2] = int(str(B.get_state())[2])
        elif len(str(B.get_state())) == 2:
            b[1] = int(str(B.get_state())[0])
            b[2] = int(str(B.get_state())[1])
        else:
            b[2] = B.get_state()

        return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])


    # update the search path
    def path(self, end_state):
        while end_state.get_state() != None:
            self.search_path.insert(0, end_state.get_state())
            end_state = end_state.get_parent()


    # Implementation of the breadth first search algorithm
    def BFS(self):
        # keep a queue for BFS
        queue = Queue()

        # enqueue the start state to the queue as a tuple (state, parent_state)
        self.start_state.set_parent(State(None))
        queue.enqueue(self.start_state)
        self.expanded.append((self.start_state.get_state(), None))

        # keep looping whilst there's still states in the queue
        while queue.is_empty() != True and len(self.visited) <= 1000:
            # dequeue next state and add it to visited
            current_state = queue.front()
            parent_state = queue.dequeue().get_parent()
            children_states = self.get_children_states(current_state, parent_state)
            self.visited.append(current_state.get_state())

            # add current states children states to the queue
            for child_state in children_states:
                queue.enqueue(child_state)
                self.expanded.append((child_state.get_state(), self.last_update(child_state, current_state)))

            # check if end state is found
            if current_state.get_state() == self.goal_state.get_state():
                # end state found
                self.path(current_state)
                break


    # Implementation of the depth first search algorithm
    def DFS_recurse(self, current_state, parent_state):
        if len(self.visited) == 1000:
            return State(-1, State(None))
        # get children states and add current state to visited
        children_states = self.get_children_states(current_state, parent_state)
        self.visited.append(current_state.get_state())

        # check if end state is found
        if current_state.get_state() == self.goal_state.get_state():
            # end state found
            return current_state

        # loop through children states and perform DFS on them
        for child_state in children_states:
            self.expanded.append((child_state.get_state(), self.last_update(child_state, current_state)))
            result = self.DFS_recurse(child_state, current_state)
            if result.get_state() == self.goal_state.get_state():
                return result

        return State(-1, State(None))


    # Implementation of the depth first search algorithm
    def DFS(self):
        self.expanded.append((self.start_state.get_state(), None))
        end_state = self.DFS_recurse(self.start_state, self.start_state.get_parent())
        self.path(end_state)


    # Implementation of the greedy search algorithm
    def greedy(self):
        # add start state to expanded and initalise fringe
        self.start_state.set_parent(State(None))
        self.expanded.append((self.start_state.get_state(), None))
        fringe = []

        # Initalise current state and parent state
        current_state = self.start_state
        parent_state = self.start_state.get_parent()

        # keep looping whilst there's still states in the fringe and visited is less than 1000
        while True:
            children_states = self.get_children_states(current_state, parent_state)
            self.visited.append(current_state.get_state())

            # add current states children states to expanded and the fringe
            for child_state in children_states:
                fringe.append(child_state)
                self.expanded.append((child_state.get_state(), self.last_update(child_state, current_state)))

            # check if goal state is found
            if current_state.get_state() == self.goal_state.get_state():
                # goal state found
                self.path(current_state)
                break

            if len(fringe) > 0:
                # Initalise best new state, best heuristic and index with values of first state in fringe
                best_new_state = fringe[0]
                best_heuristic = self.manhattan_heuristic(fringe[0], self.goal_state)
                best_new_state_idx = 0
                idx = 0
                for new_state in fringe:
                    if self.manhattan_heuristic(new_state, self.goal_state) <= best_heuristic:
                        # update best heuristic found, best new state found and the index of it, so we
                        # can delete it from the fringe
                        best_heuristic = self.manhattan_heuristic(new_state, self.goal_state)
                        best_new_state = new_state
                        best_new_state_idx = idx
                    idx += 1
                # delete the chosen new state from the fringe, update current state and parent state
                current_state = fringe.pop(best_new_state_idx)
                parent_state = current_state.get_parent()

            if len(fringe) <= 0 and len(self.visited) >= 1000:
                break


    # Implementation of the iterative deepening search algorithm
    def IDS_recurse(self, current_state, parent_state, depth):
        if len(self.visited) == 1000:
            return State(-1, State(None))
        # get children states and add current state to visited
        children_states = self.get_children_states(current_state, parent_state)
        self.visited.append(current_state.get_state())

        # check if end state is found
        if current_state.get_state() == self.goal_state.get_state():
            # end state found
            return current_state

        # If reached the maximum depth, stop recursing
        if depth <= 0:
            return State(-1, State(None))

        # loop through children states and perform DFS on them
        for child_state in children_states:
            self.expanded.append((child_state.get_state(), self.last_update(child_state, current_state)))
            result = self.IDS_recurse(child_state, current_state, depth - 1)
            if result.get_state() == self.goal_state.get_state():
                return result

        return State(-1, State(None))


    # Implementation of the iterative deepening search algorithm
    def IDS(self):
        depth = 0
        while True:
            self.expanded.append((self.start_state.get_state(), None))
            end_state = self.IDS_recurse(self.start_state, self.start_state.get_parent(), depth)
            if end_state.get_state() == self.goal_state.get_state():
                self.path(end_state)
                break
            depth += 1
            self.visited = []

    # Implementation of the A* search algorithm
    def aStar(self):
        # add start state to expanded and initalise fringe
        self.start_state.set_parent(State(None))
        self.expanded.append((self.start_state.get_state(), None))
        fringe = []

        # Initalise current state and parent state
        current_state = self.start_state
        parent_state = self.start_state.get_parent()

        # keep looping whilst there's still states in the fringe and visited is less than 1000
        while True:
            children_states = self.get_children_states(current_state, parent_state)
            self.visited.append(current_state.get_state())

            # add current states children states to expanded and the fringe
            for child_state in children_states:
                fringe.append(child_state)
                self.expanded.append((child_state.get_state(), self.last_update(child_state, current_state)))

            # check if goal state is found
            if current_state.get_state() == self.goal_state.get_state():
                # goal state found
                self.path(current_state)
                break

            if len(fringe) > 0:
                # Initalise best new state, best heuristic and index with values of first state in fringe
                best_new_state = fringe[0]
                best_heuristic = self.manhattan_heuristic(fringe[0], self.goal_state) + fringe[0].get_depth()
                best_new_state_idx = 0
                idx = 0
                for new_state in fringe:
                    if self.manhattan_heuristic(new_state, self.goal_state) + new_state.get_depth() <= best_heuristic:
                        # update best heuristic found, best new state found and the index of it, so we
                        # can delete it from the fringe
                        best_heuristic = self.manhattan_heuristic(new_state, self.goal_state) + new_state.get_depth()
                        best_new_state = new_state
                        best_new_state_idx = idx
                    idx += 1
                # delete the chosen new state from the fringe, update current state and parent state
                current_state = fringe.pop(best_new_state_idx)
                parent_state = current_state.get_parent()

            if len(fringe) <= 0 and len(self.visited) >= 1000:
                break


    # Implementation of the hill climbing search algorithm
    def hillClimbing(self):
        pass


    # convert visited and expanded lists to string to be returned
    def toString(self):
        # path -- convert integers to strings and add 0's to non 3-digit numbers
        # then append values together with commas
        if len(self.search_path) == 0 or self.search_path == [-1]:
            path = "No solution found."
        else:
            path = ["0" + state if len(state) == 2 else state for state in list(map(str, self.search_path))]
            path = ["00" + state if len(state) == 1 else state for state in path]
            path = ','.join(path)

        # visited -- convert integers to strings and add 0's to non 3-digit numbers
        # then append values together with commas
        visited = ["0" + state if len(state) == 2 else state for state in list(map(str, self.visited))]
        visited = ["00" + state if len(state) == 1 else state for state in visited]
        visited = ','.join(visited)

        # concatenate search path + visited lists as a string
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
    # Call solve to get a string with the search path and visited states, then print to stdout
    print(threeDigitsSolver.solve())


if __name__ == '__main__':
    main()
