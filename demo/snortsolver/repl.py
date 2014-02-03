from  gamestate import GameState, GameoverException
import player

import networkx as nx
import matplotlib.pyplot as plt
import os

import labels


class REPL(object):
    def __init__(self):
        n = input("Number of vertices: ")
        p = input("Edge probability: ")
        color = raw_input("Select your color (R/B): ")
        G = nx.erdos_renyi_graph(n, p)
        self.state = GameState(G)

        if color == 'R':
            self.red = player.HumanPlayer(labels.RED)
            self.blue = player.BotPlayer(labels.BLUE)
        else:
            self.red = player.BotPlayer(labels.RED)
            self.blue = player.HumanPlayer(labels.BLUE)

        print os.linesep, 'GAME HAS BEGUN', os.linesep

        plt.ion()
        plt.axis('off')
        plt.show()

    def error(self, e):
        print e

    def run(self):
        while not self.state.is_gameover():
            plt.clf()
            self.state.draw()
            try:
                if self.state.turn is labels.RED:
                    move = self.red.get_move(self.state)
                else:
                    move = self.blue.get_move(self.state)
                if move is None:
                    print move, 'is none'
                self.state.make_move(move)
                self.state.alternate_turn()
                plt.draw()
            except GameoverException, e:
                break
        winner = self.state.winner
        print winner, "is the winner."
