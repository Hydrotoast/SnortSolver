from solver import Solver

import os


class Player(object):
    def __init__(self, label):
        self.label = label


class HumanPlayer(Player):
    def get_move(self, state):
        """Returns a valid move from the human player."""
        moves = state.get_available_moves()
        print 'Player', self.label, '\'s turn.'
        print 'Recommended move:', self.recommend_move(state.graph, moves)
        while not state.is_gameover():
            v = input("Select a vertex: ")
            if v in moves:
                break
            print "Invalid move:", v
        print self.label, 'plays:', v, os.linesep
        return v

    def recommend_move(self, graph, moves):
        """Recommends a move for the human player."""
        best_move = moves[0]
        best_degree = graph.degree(moves[0])
        for i in moves:
            if graph.degree(i) > best_degree:
                best_degree = graph.degree(i)
                best_move = i
        return best_move


class BotPlayer(Player):
    def get_move(self, state):
        """Returns a valid move from the computer player."""
        solver = Solver(self.label)
        print 'Player', self.label, '\'s turn.'
        try:
            move, ret_state, score = solver.minimax(state)
            print 'Bot plays:', move, 'with value', score, os.linesep
            return move
        except Exception, e:
            print 'Bot Error:', e

