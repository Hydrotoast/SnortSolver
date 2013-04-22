import sys
import os
sys.path.append(os.path.join(os.getcwd(), '../demo'))

import GameState
import unittest

import networkx as nx

import labels as Label

class GameStateTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.G = nx.Graph()
		cls.G.add_nodes_from([0, 1, 2])

	def test_init(self):
		"""Tests the initialization of a GameState"""
		GameStateTest.G.add_edge(0, 1)
		state = GameState.GameState(GameStateTest.G)
		self.assertEquals(state.turn, Label.RED)
		self.assertFalse(state.is_gameover())
		self.assertFalse(state.is_terminal())

	def test_normal_play(self):
		"""Tests a normal game."""
		state = GameState.GameState(GameStateTest.G)

		self.assertEquals(state.turn, Label.RED)
		state.make_move(0)
		self.assertFalse(state.check_gameover())
		state.alternate_turn()

		self.assertEquals(state.turn, Label.BLUE)
		state.make_move(1)
		self.assertFalse(state.check_gameover())
		state.alternate_turn()

		self.assertEquals(state.turn, Label.RED)
		state.make_move(2)
		self.assertTrue(state.check_gameover())
		state.alternate_turn()

		self.assertEquals(state.turn, Label.BLUE)
		self.assertTrue(state.is_gameover())
		self.assertTrue(state.is_terminal())
		self.assertEquals(state.winner, Label.RED)

	def test_terminal_state(self):
		"""Tests proper terminal state."""
		GameStateTest.G.add_edge(0, 1)
		GameStateTest.G.add_node(3)
		GameStateTest.G.add_edge(2, 3)
		state = GameState.GameState(GameStateTest.G)

		self.assertEquals(state.turn, Label.RED)
		state.make_move(0)
		state.alternate_turn()
		state.make_move(2)

		self.assertFalse(state.is_gameover())
		self.assertTrue(state.is_terminal())

	def test_gameover_state(self):
		"""Tests proper gameover state."""
		state = GameState.GameState(GameStateTest.G)
		state.make_move(0)
		state.make_move(1)
		state.make_move(2)
		self.assertEquals(state.turn, Label.RED)
		self.assertTrue(state.is_gameover())
		self.assertTrue(state.is_terminal())
	
	def test_available_moves(self):
		"""
		Tests that valid moves are returned when queried especially after
		a move has been made.
		"""
		GameStateTest.G.add_edge(0, 1)
		state = GameState.GameState(GameStateTest.G)
		self.assertEquals(state.get_available_moves(), [0, 1, 2])

		state.make_move(0)
		state.alternate_turn()
		self.assertEquals(state.get_available_moves(), [2])

	def test_invalid_move(self):
		"""Tests that invalid moves raise an exception"""
		GameStateTest.G.add_edge(0, 1)
		state = GameState.GameState(GameStateTest.G)
		state.make_move(0)
		state.make_move(1)
		self.assertRaises(GameState.InvalidMoveException)
	
	def test_available_count(self):
		state = GameState.GameState(GameStateTest.G)
		self.assertEquals(state.count_available(), 3)

		state.make_move(0)
		self.assertEquals(state.count_available(), 2)

		state.make_move(1)
		self.assertEquals(state.count_available(), 1)

		state.make_move(2)
		self.assertEquals(state.count_available(), 0)

if __name__ == '__main__':
	unittest.main()
