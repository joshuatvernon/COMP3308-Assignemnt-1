class Queue(object):
	"""
	Implementation of a Queue in Python. A Queue is a FIFO (First-In-First-Out) data structure where
	data is enqueued onto the Queue and dequeued from least recent to most recent.
	"""
	def __init__(self):
		""" Initalises a list to use as a Queue.
		"""
		self.values = []

	def is_empty(self):
		""" Returns True if the Queue is empty and False otherwise.
		"""
		return self.values == []

	def enqueue(self, value):
		""" Add (put/enqueue) the value at the end of the Queue.
		"""
		self.values.insert(0, value)

	def dequeue(self):
		""" Returns and removes (pop/dequeue) the value from the front of the Queue.
		"""
		return self.values.pop()
		
	def front(self):
		""" Returns but doesn't remove the value from the front of the Queue.
		"""
		return self.values[len(self.values) - 1]

	def size(self):
		""" Returns the size of the Queue.
		"""
		return len(self.values)
		
	def to_string(self):
		""" Returns the Queue as string.
		"""
		return str(self.values)
		
	def empty(self):
		""" Clears all values from the Queue.
		"""
		self.values = []