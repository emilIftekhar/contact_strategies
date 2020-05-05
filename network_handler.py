import network
import random
import copy
import numpy

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

        self.randomly_reduced_network = temp_network
        self.randomly_reduced_network.update_contacts()
        return self.randomly_reduced_network

    # calculate how many edges there are less in the randomly reduced network compared to the base network
    def calculate_reduced_number_of_edges(self):
        edge_difference = len(list(self.base_network.edges)) - len(list(self.randomly_reduced_network.edges))
        return edge_difference

    # Triadic strategy.
    # Remove edges so that we have as many as in the random reduction case.
    # But preferably keep edge AB if BC exists for any contact C of A.
    def triadic_strategy(self):
        temp_network = copy.deepcopy(self.base_network)
        nodes = list(temp_network.nodes)
        for node in list(temp_network.nodes):
            if node in nodes:
                edges = list(temp_network.edges(node))
                alters = [edge[1] for edge in edges]
                edge_not_deleted = True
                i = 0

                # try to find contact without mutual friends and delete edge
                while len(edges) > 0 and edge_not_deleted and i<10*len(alters):
                    random_alter = random.choice(alters)
                    edges_of_alter = list(temp_network.edges(random_alter))

                    # get third contacts of other node
                    contacts_of_alter = [edge[1] for edge in edges_of_alter]
                    contacts_of_alter.remove(node)

                    # check if they have mutual contacts
                    # if not / if disjoint==True remove edge
                    if set(alters).isdisjoint(contacts_of_alter):

                        # remove other node from iteration
                        if random_alter in nodes:
                            nodes.remove(random_alter)

                        temp_network.remove_edge(node, random_alter)
                        edge_not_deleted = False

                    i += 1

                # if it didnt work then just delete random edge
                if len(alters) > 0 and edge_not_deleted:
                    random_edge = random.choice(edges)
                    other_node = random_edge[1]

                    # remove other node from iteration
                    if other_node in nodes:
                        nodes.remove(other_node)

                    temp_network.remove_edge(node, other_node)


        temp_network.update_contacts()
        return temp_network

    # Repeating contacts strategy
    # Compared to network G have half the edges but double weights on remaining
    def repeating_contacts(self, G, contact_number_allowance):
        temp_network = copy.deepcopy(G)
        nodes = list(temp_network.nodes)
        for node in list(temp_network.nodes):
            if node in nodes:
                edges = list(temp_network.edges(node))
                contact_number = len(edges)

                # select and delete random edges so that node has not more than allowed edges
                if contact_number > contact_number_allowance:
                    edges_random_order = numpy.random.permutation(edges)
                    edges_to_be_deleted = edges_random_order[(contact_number_allowance-1):]
                    for edge in edges_to_be_deleted:
                        temp_network.remove_edge(edge[0], edge[1])

                # increase contact probabilities on remaining edges
                # so that the total contact probability is the same as in G
                multiplication_factor = contact_number / contact_number_allowance
                remaining_edges = list(temp_network.edges(node))
                for edge in remaining_edges:
                    temp_network.edges[edge]['weight'] *= multiplication_factor

        temp_network.update_contacts()
        return temp_network

    def analyze_network(self, G):
        nx.info(network_base)
        nx.average_shortest_path_length(network_base)
        nx.average_clustering(network_base)
