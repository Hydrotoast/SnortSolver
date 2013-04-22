import networkx as nx
import matplotlib.pyplot as plt

import labels as Label

class InvalidMoveException(Exception):
	def __init__(self, move):
		self.move = move

	def __str__(self):
		return repr(self.move), ' is an invalid move.'

class GameoverException(Exception):
	def __str__(self):
		return 'Game has ended.'

class GameState(object):
	def __init__(self, graph):
		self.graph = graph
		for i in self.graph.nodes_iter():
			self.graph.node[i]['label'] = Label.AVAILABLE
	
	def get_available_moves(self):
		"""Returns the set of available move."""
		if self.is_gameover():
			raise GameoverException()
		moves = []
		for i in self.graph.nodes_iter():
			if self.graph.node[i]['label'] == Label.AVAILABLE \
				or self.graph.node[i]['label'] == self.get_current_label():
				moves.append(i)
		if len(moves) == 0:
			raise GameoverException()
		return moves

	def make_move(self, move):
		"""
		Makes a move in the current game state. Each move will disconnect a 
		vertex from the graph by making it UNAVAILABLE and then removing
		its neighboring edges. Hence, neighbors are also updated.
		"""
		if self.is_gameover():
			raise GameoverException()
		if move not in self.get_available_moves():
			raise InvalidMoveException(move)

		# Perform a limited AC3 algorithm for arc-consistency
		self.graph.node[move]['label'] = Label.UNAVAILABLE
		for i in self.graph.neighbors(move):
			neighbor = self.graph.node[i]
			self.graph.remove_edge(move, i)
			if neighbor['label'] == Label.AVAILABLE:
				neighbor['label'] = self.get_current_label()
				for j in self.graph.neighbors(i):
					if self.graph.node[j]['label'] == self.get_current_label():
						self.graph.remove_edge(i, j)
			elif neighbor['label'] == self.get_opponent_label():
				neighbor['label'] = Label.UNAVAILABLE
				for j in self.graph.neighbors(i):
					self.graph.remove_edge(i, j)
		
		# Gameover check
		if self.check_gameover():
			self.gameover = True
			self.winner = self.get_current_label()

	def check_gameover(self):
		"""Checks if the game has ended after a move has been applied."""
		for i in self.graph.nodes_iter():
			if self.graph.node[i]['label'] == Label.AVAILABLE \
				or self.graph.node[i]['label'] == self.get_opponent_label():
				return False
		return True

	def alternate_turn(self):
		"""Alternates the turn such that the next player can move."""
		self.turn = Label.BLUE if self.turn is Label.RED else Label.RED

	def get_current_label(self):
		"""Returns the label of the current player."""
		return Label.RED if self.turn is Label.RED else Label.BLUE

	def get_opponent_label(self):
		"""Returns the label of the current, opposing player."""
		return Label.BLUE if self.turn is Label.RED else Label.RED

	def is_terminal(self):
		"""Returns true if the state is a terminal state."""
		return nx.number_connected_components(self.graph) == self.graph.number_of_nodes() and self.count_available() == 0

	def is_gameover(self):
		"""Returns true if the game has ended."""
		return self.gameover

	def count_available(self):
		"""Returns the number of available-labeled nodes."""
		return len([i for i in self.graph.nodes_iter() if self.graph.node[i]['label'] == Label.AVAILABLE])

	def draw(self):
		"""Draws the current game state."""
		unavailables = []
		availables = []
		reds = []
		blues = []
		for i in self.graph.nodes_iter():
			if self.graph.node[i]['label'] == Label.AVAILABLE:
				availables.append(i)
			elif self.graph.node[i]['label'] == Label.RED:
				reds.append(i)
			elif self.graph.node[i]['label'] == Label.BLUE:
				blues.append(i)
			else:
				unavailables.append(i)
		labels = {}
		for i in self.graph.nodes_iter():
			labels[i] = i
		pos = nx.circular_layout(self.graph)
		nx.draw_networkx_edges(self.graph, pos,
			edgelist=self.graph.edges(),
			width=4)
		nx.draw_networkx_nodes(self.graph, pos,
			nodelist=availables,
			node_color='w',
			node_size=500,
			alpha=1)
		nx.draw_networkx_nodes(self.graph, pos, 
			nodelist=reds,
			node_color='r',
			node_size=500,
			alpha=1)
		nx.draw_networkx_nodes(self.graph, pos, 
			nodelist=blues,
			node_color='b',
			node_size=500,
			alpha=1)
		nx.draw_networkx_nodes(self.graph, pos, 
			nodelist=unavailables,
			node_color='black',
			node_size=500,
			alpha=0.6)
		nx.draw_networkx_labels(self.graph, pos, labels, font_size=16)

	@property
	def gameover(self):
		try:
			return self._gameover
		except AttributeError:
			self._gameover = False
		return self._gameover

	@gameover.setter
	def gameover(self, value):
		self._gameover = value

	@property
	def turn(self):
		try:
			return self._turn
		except AttributeError:
			self._turn = Label.RED
		return self._turn

	@turn.setter
	def turn(self, label):
		self._turn = label

	@property
	def winner(self):
		if not self.is_gameover():
			raise Exception('No winner yet')
		return self._winner

	@winner.setter
	def winner(self, label):
		self._winner = label
