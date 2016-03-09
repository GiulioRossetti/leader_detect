import math
import networkx as nx
from collections import defaultdict


class Diffusion(object):
    def __init__(self, graph_file, action_file, listening_file):
        """
        constructor
        :param graph_file: edgelist format
        :param action_file: actions in gurumine format
        """
        self.__load_data(graph_file, action_file, listening_file)

    def get_action_list(self):
        """
        Get the action list
        """
        return list(self.action2node2time.keys())

    def __load_data(self, graph_file, action_file, listening_file):
        """
        Load the graph and action data

        :param graph_file: edgelist format
        :param action_file: actions in gurumine format
        """

        #loading the full social graph
        self.G = nx.Graph()
        edges = open(graph_file, "r")
        for e in edges:
            part = e.split()
            u = int(part[0])
            v = int(part[1])
            self.G.add_edge(u, v)

        #loading the actions
        self.action2node2time = {}

        self.node2weight = {}

        actions = open(action_file, "r")
        for a in actions:
            part = a.split("::")
            nid = int(part[1])
            time = int(part[0])
            act = int(part[2])
            weight = int(part[3])

            if act in self.action2node2time:
                v = self.action2node2time.get(act)
                v[nid] = time
            else:
                node2time = {nid: time}
                self.action2node2time[act] = node2time

            self.node2weight[nid] = weight

        #loading listening file
        self.user_action_total_listen = defaultdict(lambda : defaultdict(lambda : defaultdict(int)))
        listening = open(listening_file, "r")
        for l in listening:
            part = l.split("::")
            nid = int(part[0])
            act = int(part[1])
            tot_listen = int(part[2])
            weeks = int(part[3])
            self.user_action_total_listen[nid][act] = tot_listen

    def build_action_subgraph(self, action, delta):
        """
        Compute the directed induced subgraph for the given action

        :param action: action id
        :param delta: temporal displacement
        """
        nodes2time = self.action2node2time.get(action)
        nodes = nodes2time.keys()

        #induced subgraph for action
        isg = self.G.subgraph(nodes)

        #cleaning the edges and building the digraph
        disg = nx.DiGraph()

        for e in isg.edges():
            diff = abs((nodes2time.get(e[0]) - nodes2time.get(e[1])))
            if diff != 0 and diff <= delta:
                if nodes2time.get(e[0]) < nodes2time.get(e[1]):
                    disg.add_edge(e[0], e[1])
                else:
                    disg.add_edge(e[1], e[0])

        return disg

    def compute_action_leaders(self, disg):
        """
        Compute the leaders for the given action

        :param disg: directed graph induced for the specific action
        """
        #compute the leaders for this action
        leaders = []
        for n in disg.nodes():
            n_ind = disg.in_degree(n)
            n_odg = disg.out_degree(n)
            if n_ind == 0 and not (n_odg == 0):
                leaders.append(n)

        return leaders

    def compute_max_depth(self, tree, leader, frontier):
        """
        Compute the maximal depth for the given diffusion tree

        :param tree: the action tree
        :param leader: root of the tree
        :param frontier: leafs of the tree
        """
        max_depth = 0

        for f in frontier:
            l = len(nx.shortest_path(tree, leader, f))
            if l > max_depth:
                max_depth = l

        return max_depth

    def compute_width(self, tree, leader):
        """
        Compute the ratio between leaders neighbors in the full graph and
        the ones in the diffusion tree

        :param tree: the diffusion tree
        :param leader: leader of the tribe
        """
        leader_neighbors = self.G.neighbors(leader)
        tribe_restricted_neighbors = tree.neighbors(leader)

        ratio = float(len(tribe_restricted_neighbors)) / float(len(leader_neighbors))

        return ratio

    def compute_strength(self, tree, leader, distance_factor):
        """
        Compute the strength for the given diffusion tree, leader and distance factor

        weight = sum_{n \in tree} strength_{n}^{-distanceFactor * shortestPath(leader, n)}

        :param tree:
        :param leader:
        :param distance_factor:
        """
        strength = 0
        t_nodes = tree.nodes()

        for n in t_nodes:
            if n is not leader:
                l = len(nx.shortest_path(tree, leader, n))
                w = self.node2weight[n]
                strength += float(w) * math.exp(-distance_factor * (l - 1))

        return strength

    def compute_level_strength(self, tree, leader, distance_factor, action):
        """
        Compute the strength for the given diffusion tree, leader and distance factor

        :param tree:
        :param leader:
        :param distance_factor:
        :param action:
        """
        strength = 0
        t_nodes = tree.nodes()

        level_to_weight = {}

        for n in t_nodes:
            if n is not leader:
                l = len(nx.shortest_path(tree, leader, n))
                w = self.node2weight[n]
                total_listens = self.user_action_total_listen[n][action]
                if not l in level_to_weight:
                    level_to_weight[l] = float(w) / total_listens
                else:
                    level_to_weight[l] += float(w) / total_listens

        for l in level_to_weight:
            strength += (distance_factor ** l) * level_to_weight[l]

        return strength
