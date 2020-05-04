import network
import random
import copy

class Network_Handler:
    def __init__(self, base_network):
        self.base_network = base_network

    # Randomly sever ties for every contact.
    # Per node select randomly chosen edge and delete it.
    # The other node of the edge does NOT have to delete an additional tie later.
    def random_reduction(self):
        temp_network = copy.deepcopy(self.base_network)
        nodes = list(temp_network.nodes)
        for node in list(temp_network.nodes):
            if node in nodes:
                edges = list(temp_network.edges(node))
                if len(edges) > 0:
                    random_edge = random.choice(edges)
                    other_node = random_edge[1]

                    # remove other node from iteration
                    if other_node in nodes:
                        nodes.remove(other_node)

                    temp_network.remove_edge(node, other_node)

        randomly_reduced_network = temp_network
        return randomly_reduced_network
