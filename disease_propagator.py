import numpy as np
import random


class Disease_Propagator:
    def __init__(
        self,
        time_limit,
        time_until_recovery,
        mean_time_until_quarantine,
        std_dev_time_until_quarantine,
    ):
        self.time_limit = time_limit

        self.time_until_recovery = time_until_recovery
        self._time_until_quarantine = {
            "mean": mean_time_until_quarantine,
            "std_dev": std_dev_time_until_quarantine,
        }

    def interaction(self, person1, person2):
        if person1.ID in self.S and person2.ID in self.I:
            self.S.remove(person1.ID)
            time = int(
                np.random.normal(
                    self._time_until_quarantine["mean"],
                    self._time_until_quarantine["std_dev"],
                )
            )
            person1.time_to_quarantine = time if time > 0 else 0
            self.I.append(person1.ID)
        elif person1.ID in self.I and person2.ID in self.S:
            self.S.remove(person2.ID)
            time = int(
                np.random.normal(
                    self._time_until_quarantine["mean"],
                    self._time_until_quarantine["std_dev"],
                )
            )
            person2.time_to_quarantine = time if time > 0 else 0
            self.I.append(person2.ID)

    def simulate(self, network, p, number_of_first_infected, contacts_per_timestep):
        """
        Docstring todo
        """

        population_size = network.population_size

        # Initialize compartment ID lists
        population = network.get_population()
        self.S = list(population.keys())  # Susceptibles
        self.I = []

        # ------------------------------------------------------------------------------ #
        # First infected
        # ------------------------------------------------------------------------------ #
        for i in range(number_of_first_infected):
            first_infected_ID = random.choice(self.S)
            first_infected = population[first_infected_ID]
            first_infected.time_to_quarantine = np.random.normal(
                self._time_until_quarantine["mean"], self._time_until_quarantine["std_dev"]
            )
            self.I.append(first_infected.ID)  # Infectious
            self.S.remove(first_infected.ID)



        self.Q = []  # Quarantined
        # Initialize compartment size time series
        S_t = [len(self.S)]  # Number of susceptibles
        I_t = [len(self.I)]  # Number of infected
        simulation_time = 0
        while simulation_time < self.time_limit:
            # ------------------------------------------------------------------------------ #
            # Simulate one random interaction process for each person in population
            # ------------------------------------------------------------------------------ #
            # We go randomly thru the population
            random_order = np.random.permutation(population_size)

            #For every person we draw N random contacts from therer contacts list
            #and try to infect them this is depending on weights
            for node_ID in random_order:
                node = network.nodes[node_ID]
                edge_IDs = network.edges(node_ID)
                weights = [network.edges[edge_ID]["weights"][node_ID] for edge_ID in edge_IDs]
                neighbor_nodes = [edge_ID[1] for edge_ID in edge_IDs]

                neighbor_nodes_random = np.random.choice(neighbor_nodes,contacts_per_timestep,weights)
                for neighbor_node_random in neighbor_nodes_random:
                    self.interaction(network.nodes[node_ID]["person"], network.nodes[neighbor_node_random]["person"])

            # Random infection in public
            infected = []
            for ID in self.S:
                person = network.nodes[ID]["person"]
                if random.uniform(0, 1) < p * len(self.I) / (len(self.S) + len(self.I)):
                    infected.append(ID)
                    time = int(
                        np.random.normal(
                            self._time_until_quarantine["mean"],
                            self._time_until_quarantine["std_dev"],
                        )
                    )
                    person.time_to_quarantine = time if time > 0 else 0
                    self.I.append(person.ID)
            for ID in infected:
                self.S.remove(ID)

            # Quarantining infectious people
            quarantined = []
            for ID in self.I:
                person = network.nodes[ID]["person"]
                person.time_to_quarantine -= 1
                if person.time_to_quarantine < 1:
                    quarantined.append(person.ID)
                    person.time_to_recovery = self.time_until_recovery
                    self.Q.append(person.ID)
            for ID in quarantined:
                self.I.remove(ID)

            # Recovery
            recovered = []
            for ID in self.Q:
                person = network.nodes[ID]["person"]
                person.time_to_recovery -= 1
                if person.time_to_recovery < 1:
                    recovered.append(person.ID)
                    self.S.append(person.ID)
            for ID in recovered:
                self.Q.remove(ID)

            # Update compartment numbers
            S_t.append(len(self.S))
            I_t.append(len(self.I) + len(self.Q))

            simulation_time += 1

        return (S_t, I_t)
