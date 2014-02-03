from snortsolver.solver import Solver
from snortsolver.gamestate import GameState
import snortsolver.labels as Label

import networkx as nx

if __name__ == '__main__':
    for i in range(1,12):
        g = nx.cycle_graph(i)
        state = GameState(g)

        solver = Solver(Label.RED)
        solver.solve(state)
