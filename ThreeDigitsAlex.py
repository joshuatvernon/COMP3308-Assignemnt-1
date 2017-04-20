#!/usr/bin/python3

import sys

class State:
	field1 = 0
	field2 = 0
	field3 = 0
	num = 0
	num_string = ""
	parent = []
	children = []
	order = 0
	digit = 0
	depth = 0
	h = 0

	def init(self,str,parent):
		self.field1 = int(str[0])
		self.field2 = int(str[1])
		self.field3 = int(str[2])
		self.parent = parent
		self.num = self.field1 * 100 + self.field2 * 10 + self.field3
		temp = str.split("\n")
		self.num_string = temp[0]
		self.children = []
		self.order = 0
		self.digit = 0
		if parent != object:
			self.depth = parent.depth + 1
		else:
			self.depth = 0
		self.h = 0

def is_forbidden(child,forbidden):
	# forbidden is a list of strings
	for str in forbidden:
		if str == child.num_string:
			return True
	return False

def generate_children(state,forbidden):
	while (state.order < 6):
		new_child = generate_child(state)
		if len(new_child.num_string) != 0 and not is_forbidden(new_child,forbidden):
			state.children.append(new_child)

def generate_child(state):
	child = State()
	num_string = ""
	if state.order == 0:
		if state.digit != 1 and state.field1 != 0:
			num_string = str(state.field1 - 1) + str(state.field2) + str(state.field3)
			child.init(num_string,state)
			child.digit = 1
	elif state.order == 1:
		if state.digit != 1 and state.field1 != 9:
			num_string = str(state.field1 + 1) + str(state.field2) + str(state.field3)
			child.init(num_string,state)
			child.digit = 1
	elif state.order == 2:
		if state.digit != 2 and state.field2 != 0:
			num_string = str(state.field1) + str(state.field2 - 1) + str(state.field3)
			child.init(num_string,state)
			child.digit = 2
	elif state.order == 3:
		if state.digit != 2 and state.field2 != 9:
			num_string = str(state.field1) + str(state.field2 + 1) + str(state.field3)
			child.init(num_string,state)
			child.digit = 2
	elif state.order == 4:
		if state.digit != 3 and state.field3 != 0:
			num_string = str(state.field1) + str(state.field2) + str(state.field3 - 1)
			child.init(num_string,state)
			child.digit = 3
	elif state.order == 5:
		if state.digit != 3 and state.field3 != 9:
			num_string = str(state.field1) + str(state.field2) + str(state.field3 + 1)
			child.init(num_string,state)
			child.digit = 3
	else:
		return 1

	state.order = state.order + 1
	return child

def main(argv):
	# search mode
	search_mode = argv[0]
	# start and goal state
	start_st = State()
	goal_st = State()
	# forbidden list
	forbidden = []
	# input file
	f = open(argv[1])
	lines = f.readlines()

	if (len(lines) < 2):
		return 1

	temp = lines[0].split("\n")
	if (len(temp[0]) != 3):
		return 1
	start_st.init(temp[0],object)

	temp = lines[1].split("\n")
	if (len(temp[0]) != 3):
		return 1
	goal_st.init(temp[0],object)

	if (len(lines) == 3):
		nums = lines[2].split(",")
		for x in nums:
			x = x.split("\n")
			forbidden.append(x[0])
	f.close()

	#add_child(start_st)
	#print (start_st.children[0].parent.num)

	if search_mode == "B":
		BFS(start_st,goal_st,forbidden)
	elif search_mode == "D":
		DFS(start_st,goal_st,forbidden)
	elif search_mode == "I":
		IDS(start_st,goal_st,forbidden)
	elif search_mode == "G":
		Greedy(start_st,goal_st,forbidden)
	elif search_mode == "H":
		Hill_climbing(start_st,goal_st,forbidden)
	elif search_mode == "A":
		A(start_st,goal_st,forbidden)
	else:
		# invalid input
		return 1;

	return 1;

def eval_function(state1,state2):
	x = abs(state1.field1 - state2.field1) + abs(state1.field2 - state2.field2) + abs(state1.field3 - state2.field3)
	return x

def already_expanded(current,expanded):
	for state in expanded:
		if current.num_string == state.num_string:
			if has_same_children(current,state):
				return True

	return False

def has_same_children(state1,state2):
	if len(state1.children) == 0 or len(state2.children) == 0:
		return False

	if len(state1.children) != len(state2.children):
		return False

	for i in range(len(state1.children)):
		if state1.children[i].num_string != state2.children[i].num_string:
			return False

	return True

def is_goal_st(current,goal_st):
	# if (current.num_string == "110"):
	# 	print (current.num_string)
	# 	print (goal_st.num_string)
	if current.num_string == goal_st.num_string:
		return True

	return False

def BFS(start_st,goal_st,forbidden):
	current = start_st
	expanded = []
	fringe = []
	limit = 1000
	while(len(expanded) != limit):
		generate_children(current,forbidden)
		if not already_expanded(current,expanded):
			expanded.append(current)
			fringe = fringe + current.children
			if is_goal_st(current,goal_st):
				return print_sol(current,expanded)
			else:
				if (len(fringe) == 0):
					return (object,expanded)
				current = fringe[0]
				fringe.pop(0)
		else:
			if (len(fringe) == 0):
				return (object,expanded)
			current = fringe[0]
			fringe.pop(0)

	return print_sol(object,expanded)

def DFS(start_st,goal_st,forbidden):
	current = start_st
	expanded = []
	fringe = []
	limit = 1000
	while(len(expanded) != limit):
		generate_children(current,forbidden)
		if not already_expanded(current,expanded):
			expanded.append(current)
			fringe = current.children + fringe
			if is_goal_st(current,goal_st):
				return print_sol(current,expanded)
			else:
				if (len(fringe) == 0):
					return (object,expanded)
				current = fringe[0]
				fringe.pop(0)
		else:
			if (len(fringe) == 0):
				return (object,expanded)
			current = fringe[0]
			fringe.pop(0)

	return print_sol(object,expanded)

def IDS(start_st,goal_st,forbidden):
	current = start_st
	expanded = []
	expanded_iter = []
	fringe = []
	limit = 1000
	iteration_limit = 1
	while(len(expanded) <= limit):
		while (current.depth < iteration_limit):
			generate_children(current,forbidden)
			if not already_expanded(current,expanded_iter):
				expanded_iter.append(current)
				if (current.depth != iteration_limit - 1):
					fringe = current.children + fringe
				if is_goal_st(current,goal_st):
					expanded = expanded + expanded_iter
					return print_sol(current,expanded)
				else:
					if (len(fringe) == 0):
						break
					current = fringe[0]
					fringe.pop(0)
			else:
				if (len(fringe) == 0):
					break
				current = fringe[0]
				fringe.pop(0)
		expanded = expanded + expanded_iter
		expanded_iter = []
		current = start_st
		fringe = []
		iteration_limit = iteration_limit + 1

	return print_sol(object,expanded)

def min_h(fringe,goal_st):
	h = []
	for i in range(len(fringe)):
		h.append([fringe[i],eval_function(goal_st,fringe[i]),i])
	min = h[0]
	for x in h:
		if x[1] <= min[1]:
			min = x

	return min

def min_h_a(fringe,goal_st):
	h = []
	for i in range(len(fringe)):
		h.append([fringe[i],eval_function(goal_st,fringe[i])+fringe[i].depth,i])
	min = h[0]
	for x in h:
		if x[1] <= min[1]:
			min = x

	return min

def Greedy(start_st,goal_st,forbidden):
	current = start_st
	expanded = []
	fringe = []
	limit = 1000
	while(len(expanded) != limit):
		generate_children(current,forbidden)
		if not already_expanded(current,expanded):
			expanded.append(current)
			fringe = fringe + current.children
			if is_goal_st(current,goal_st):
				return print_sol(current,expanded)
			else:
				if (len(fringe) == 0):
					return (object,expanded)
				x = min_h(fringe,goal_st)
				current = fringe[x[2]]
				fringe.pop(x[2])
		else:
			if (len(fringe) == 0):
				return (object,expanded)
			x = min_h(fringe,current)
			current = fringe[x[2]]
			fringe.pop(x[2])

	return print_sol(object,expanded)

def Hill_climbing(start_st,goal_st,forbidden):
	current = start_st
	expanded = []
	fringe = []
	limit = 1000
	while(len(expanded) != limit):
		generate_children(current,forbidden)
		if not already_expanded(current,expanded):
			expanded.append(current)
			if is_goal_st(current,goal_st):
				return print_sol(current,expanded)
			if len(current.children) == 0:
				return print_sol(object,expanded)
			x = min_h(current.children,goal_st)
			y = eval_function(goal_st,current)
			if y > x[1]:
				current = current.children[x[2]]
			else:
				return print_sol(object,expanded)

	return print_sol(object,expanded)

def A(start_st,goal_st,forbidden):
	current = start_st
	expanded = []
	fringe = []
	limit = 1000
	while(len(expanded) != limit):
		generate_children(current,forbidden)
		if not already_expanded(current,expanded):
			expanded.append(current)
			fringe = fringe + current.children
			if is_goal_st(current,goal_st):
				return print_sol(current,expanded)
			else:
				if (len(fringe) == 0):
					return (object,expanded)
				x = min_h_a(fringe,goal_st)
				current = fringe[x[2]]
				fringe.pop(x[2])
		else:
			if (len(fringe) == 0):
				return (object,expanded)
			x = min_h_a(fringe,current)
			current = fringe[x[2]]
			fringe.pop(x[2])

	return print_sol(object,expanded)

def print_sol(current,expanded):
	path = get_path(current)
	if (len(path) == 0):
		print ("No solution found.")
	else:
		for i in range(len(path)):
			print (path[i].num_string,end="")
			if (i == len(path) - 1):
				print ("")
			else:
				print(",",end="")
	for i in range(len(expanded)):
		print (expanded[i].num_string,end="")
		if i == len(expanded) - 1 or i == 999:
			print ("")
			break
		else:
			print(",",end="")

def get_path(current):
	path = []
	while (current != object):
		path.insert(0,current)
		current = current.parent
	return path

if __name__ == "__main__":
   main(sys.argv[1:])