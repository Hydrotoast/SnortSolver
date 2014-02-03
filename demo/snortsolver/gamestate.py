import networkx as nx

import labels


class InvalidMoveException(Exception):
    def __init__(self, move):
        self.move = move

    def __str__(self):
        return str('%d is an invalid move.' % self.move)


class GameoverException(Exception):
    def __str__(self):
        return 'Game has ended.'


class GameState(object):
    def __init__(self, graph):
        self.__gameover = None
        self.__turn = None
        self.__winner = None

        self.graph = graph
        for i in self.graph.nodes_iter():
            self.graph.node[i]['label'] = labels.AVAILABLE

    def get_available_moves(self):
        """Returns the set of available move."""
        if self.is_gameover():
            raise GameoverException()
        moves = []
        for i in self.graph.nodes_iter():
            if self.graph.node[i]['label'] == labels.AVAILABLE:
                moves.append(i)
            if self.graph.node[i]['label'] == self.get_current_label():
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
        self.graph.node[move]['label'] = labels.UNAVAILABLE
        for i in self.graph.neighbors(move):
            neighbor = self.graph.node[i]
            self.graph.remove_edge(move, i)
            if neighbor['label'] == labels.AVAILABLE:
                neighbor['label'] = self.get_current_label()
                for j in self.graph.neighbors(i):
                    if self.graph.node[j]['label'] == self.get_current_label():
                        self.graph.remove_edge(i, j)
            elif neighbor['label'] == self.get_opponent_label():
                neighbor['label'] = labels.UNAVAILABLE
                for j in self.graph.neighbors(i):
                    self.graph.remove_edge(i, j)

        # Gameover check
        if self.check_gameover:
            self.gameover = True
            self.winner = self.get_current_label()

    def check_gameover(self):
        """Checks if the game has ended after a move has been applied."""
        for i in self.graph.nodes_iter():
            if self.graph.node[i]['label'] == labels.AVAILABLE:
                return False
            if self.graph.node[i]['label'] == self.get_opponent_label():
                return False
        return True

    def alternate_turn(self):
        """Alternates the turn such that the next player can move."""
        self.turn = labels.BLUE if self.turn is labels.RED else labels.RED

    def get_current_label(self):
        """Returns the label of the current player."""
        return labels.RED if self.turn is labels.RED else labels.BLUE

    def get_opponent_label(self):
        """Returns the label of the current, opposing player."""
        return labels.BLUE if self.turn is labels.RED else labels.RED

    def is_terminal(self):
        """Returns true if the state is a terminal state."""
        return nx.number_connected_components(
            self.graph) == self.graph.number_of_nodes() and self.count_available() == 0

    def is_gameover(self):
        """Returns true if the game has ended."""
        return self.gameover

    def count_available(self):
        """Returns the number of available-labeled nodes."""
        return len([i for i in self.graph.nodes_iter() if self.graph.node[i]['label'] == labels.AVAILABLE])

    def draw(self):
        """Draws the current game state."""
        unavailables = []
        availables = []
        reds = []
        blues = []
        for i in self.graph.nodes_iter():
            if self.graph.node[i]['label'] == labels.AVAILABLE:
                availables.append(i)
            elif self.graph.node[i]['label'] == labels.RED:
                reds.append(i)
            elif self.graph.node[i]['label'] == labels.BLUE:
                blues.append(i)
            else:
                unavailables.append(i)
        node_labels = {}
        for i in self.graph.nodes_iter():
            node_labels[i] = i
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
        nx.draw_networkx_node_labels(self.graph, pos, node_labels, font_size=16)

    @property
    def gameover(self):
        try:
            return self.__gameover
        except AttributeError:
            self.__gameover = False
        return self.__gameover

    @gameover.setter
    def gameover(self, value):
        self.__gameover = value

    @property
    def turn(self):
        try:
            return self.__turn
        except AttributeError:
            self.__turn = labels.RED
        return self.__turn

    @turn.setter
    def turn(self, label):
        self.__turn = label

    @property
    def winner(self):
        if not self.is_gameover():
            raise Exception('No winner yet')
        return self.__winner

    @winner.setter
    def winner(self, label):
        self.__winner = label
