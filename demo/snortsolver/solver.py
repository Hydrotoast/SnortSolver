import labels

import matplotlib.pyplot as plt

import copy
import threading


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

        num_moves = len(moves)
        move_states = [None] * num_moves
        move_scores = [0] * num_moves

        threads = []

        for i in range(num_moves):
            clone = copy.deepcopy(state)
            clone.make_move(moves[i])
            clone.alternate_turn()
            if clone.is_gameover():
                return moves[i], clone, float('+inf')
            minimax_thread = Minimax(self.label, clone, move_states, move_scores, i)
            minimax_thread.start()
            threads.append(minimax_thread)

        for thread in threads:
            thread.join()

        for i in range(num_moves):
            if move_scores[i] > best_score:
                best_score = move_scores[i]
                best_move = moves[i]
                best_state = move_states[i]

        return best_move, best_state, best_score


class Minimax(threading.Thread):
    """Thread-safe minimax algorithm."""

    def __init__(self, label, state, move_states, move_scores, move):
        threading.Thread.__init__(self)
        self.label = label
        self.state = state

        self.move_states = move_states
        self.move_scores = move_scores
        self.move = move

    def run(self):
        best_move, best_state, best_score = self.minimax(self.state)

        # Thread safe assignments
        self.move_states[self.move] = best_state
        self.move_scores[self.move] = best_score


    def minimax(self, state):
        moves = state.get_available_moves()
        best_state = state
        best_move = moves[0]
        best_score = float('+inf')
        for i in moves:
            clone = copy.deepcopy(state)
            clone.make_move(i)
            clone.alternate_turn()
            ret_state, score = self.max(clone)
            if score < best_score:
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
        return labels.RED if self.label is labels.BLUE else labels.BLUE
