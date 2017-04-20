class State(object):
	"""
	Implementation of a State in Python.
	"""

	# Initalise state with optional parent and children
	def __init__(self, state, parent_state=None, children_states=None):
		self.state = state
		self.parent_state = parent_state
		if children_states:
		    self.children_states = children_states
		else:
		    self.children_states = []


	# return state
	def get_state(self):
	    return self.state


	# return parent state
	def get_parent(self):
	    return self.parent_state


	# return children states
	def get_children(self):
	    return self.children_states


	# set state
	def set_state(self, state):
	    self.state = state


	# set parent state
	def set_parent(self, parent_state):
	    self.parent_state = parent_state


	# set children states
	def set_children(self, children_states):
	    self.children_states = children_states


	# return true if same state value, parent state value and children state values, else false
	def __cmp__(self, other_state):
		return other_state.get_state() == self.state and \
		       other_state.get_parent() == self.parent_state and \
			   other_state.get_children() == self.children_states
