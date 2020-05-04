import network

class Network_Handler:
    def __init__(base_network):
        self.base_network = base_network

    def random_reduction(self):
        randomly_reduced_network = self.base_network.copy()
