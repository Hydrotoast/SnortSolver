from  gamestate import GameState, GameoverException
import labels as Label

import networkx as nx
import matplotlib.pyplot as plt

import copy

class Solver(object):
	def __init__(self, label):
		self.label = label

	def solve(self, state):
		self.label = state.get_current_label()
		move, best_state, score = self.minimax(state)
		print '\tPlayer', state.turn
		print '\tThe payoff of this state is', score 
		best_state.draw()
		plt.show()

	def minimax(self, state):
		moves = state.get_available_moves()
		best_state = state
		best_move = moves[0]
		best_score = float('-inf')
		for i in moves:
			clone = copy.deepcopy(state)
			clone.make_move(i)
			clone.alternate_turn()
			ret_state, score = self.min(clone)
			if score > best_score:
				best_score = score
				best_move = i
				best_state = ret_state
		return best_move, best_state, best_score

	def min(self, state):
		if state.is_terminal() or state.is_gameover():
			return self.eval(state)
		moves = state.get_available_moves()
		best_state = state
		best_score = float('+inf')
		for i in moves:
			clone = copy.deepcopy(state)
			clone.make_move(i)
			clone.alternate_turn()
			ret_state, score = self.max(clone)
			if score < best_score:
				best_score = score
				best_state = ret_state
		return best_state, best_score

	def max(self, state):
		if state.is_terminal() or state.is_gameover():
			return self.eval(state)
		moves = state.get_available_moves()
		best_state = state
		best_score = float('-inf')
		for i in moves:
			clone = copy.deepcopy(state)
			clone.make_move(i)
			clone.alternate_turn()
			ret_state, score = self.min(clone)
			if score > best_score:
				best_score = score
				best_state = ret_state
		return best_state, best_score

	def eval(self, state):
		acc = 0
		for i in state.graph.nodes_iter():
			if state.graph.node[i]['label'] == self.label:
				acc += 1
			elif state.graph.node[i]['label'] == self.get_opponent_label():
				acc -= 1

		# Move advantage
		if state.turn == self.get_opponent_label():
			acc += 0.5
		return state, acc

	def get_opponent_label(self):
		return Label.RED if self.label is Label.BLUE else Label.BLUE
