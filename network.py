import networkx as nx
import random
from person import Person

class Network(nx.Graph):
    def __init__(self, population_size, average_degree, random_edge_probability):
        super().__init__()
        self.connected_watts_strogatz_graph(population_size, average_degree, random_edge_probability)

        # Attributes
        self.__population = {}
        self.random_edge_probability = random_edge_probability
        self.population_size = population_size
        self.average_degree = average_degree

        # Set starting weights
        self.set_weights()

        # Create population dict see below
        # EMIL: I wondering if we even need that and should just use the network structure instead.
        self.create_population_dict()

        # Add contacts to node attribute
        for node, value in self.__population.items():
            self.nodes[node]['person'] = value

    def set_weights(self):
        for ID in list(self.edges):
            self.edges[ID]["weights"]= {}

        for node in self.nodes:
            for ID in list(self.edges(node)):
                #if type(self.edges[ID]["weights"]) is None:
                self.edges[ID]["weights"][node] = 1/len(self.edges(node))

    def create_population_dict(self):
        for i in range(self.population_size):
            # Get the edgeds for each node (connected other nodes)
            contacts = [edge[1] for edge in self.edges(i)]
            person = Person(i, contacts)
            self.__population[i] = person

    def update_contacts(self):
        for i in range(self.population_size):
            # Get the edgeds for each node (connected other nodes)
            contacts = [edge[1] for edge in self.edges(i)]
            self.__population[i].contacts = contacts

    def get_population(self):
        return self.__population

################################################################################

    def watts_strogatz_graph(self, n, k, p, seed=None):
        if k>=n:
            raise nx.NetworkXError("k>=n, choose smaller k or larger n")
        if seed is not None:
            random.seed(seed)

        self.name="watts_strogatz_graph(%s,%s,%s)"%(n,k,p)
        nodes = list(range(n)) # nodes are labeled 0 to n-1
        # connect each node to k/2 neighbors
        for j in range(1, k // 2+1):
            targets = nodes[j:] + nodes[0:j] # first j nodes are now last in list
            self.add_edges_from(zip(nodes,targets))
        # rewire edges from each node
        # loop over all nodes in order (label) and neighbors in order (distance)
        # no self loops or multiple edges allowed
        for j in range(1, k // 2+1): # outer loop is neighbors
            targets = nodes[j:] + nodes[0:j] # first j nodes are now last in list
            # inner loop in node order
            for u,v in zip(nodes,targets):
                if random.random() < p:
                    w = random.choice(nodes)
                    # Enforce no self-loops or multiple edges
                    while w == u or self.has_edge(u, w):
                        w = random.choice(nodes)
                        if self.degree(u) >= n-1:
                            break # skip this rewiring
                    else:
                        self.remove_edge(u,v)
                        self.add_edge(u,w)

    def connected_watts_strogatz_graph(self, n, k, p, tries=100, seed=None):
        self.watts_strogatz_graph(n,k,p)
        t=1
        while not nx.is_connected(self):
            self.watts_strogatz_graph(n, k, p, seed)
            t=t+1
            if t>tries:
                raise nx.NetworkXError("Maximum number of tries exceeded")
