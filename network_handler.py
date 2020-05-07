import network
import random
import copy
import numpy

class Network_Handler:
    def __init__(self, base_network):
        self.base_network = base_network



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
                number_of_deleted_edges = 0
                for alter in alters:
                    edges_of_alter = list(temp_network.edges(alter))

                    # get third contacts of other node
                    contacts_of_alter = [edge[1] for edge in edges_of_alter]
                    contacts_of_alter.remove(node)

                    # check if they have mutual contacts
                    # if not / if disjoint==True remove edge
                    if set(alters).isdisjoint(contacts_of_alter):
                        temp_network.edges[(node, alter)]['weights'][node] = 0
                        number_of_deleted_edges += 1

                # Make weights probabilites again
                effective_edge_number = len(edges)-number_of_deleted_edges
                if effective_edge_number > 0:
                    for edge in edges:
                        temp_network.edges[edge]['weights'][node] /= effective_edge_number

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
