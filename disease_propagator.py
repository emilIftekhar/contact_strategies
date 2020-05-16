import numpy as np
import random
import copy

from contact_counter import Contact_Counter

class Disease_Propagator:
    def __init__(
        self,
        time_limit,
        time_until_recovery,
        mean_time_until_quarantine,
        std_dev_time_until_quarantine,
        asymptomatic_probabilty,
        infection_probability
    ):
        self.time_limit = time_limit

        self.time_until_recovery = time_until_recovery
        self._time_until_quarantine = {
            "mean": mean_time_until_quarantine,
            "std_dev": std_dev_time_until_quarantine,
        }
        self.asymptomatic_probabilty = asymptomatic_probabilty
        self.infection_probability = infection_probability

    def infect(self, person):
        self.S.remove(person.ID)

        # symptomatic
        time = int(
            np.random.normal(
                self._time_until_quarantine["mean"],
                self._time_until_quarantine["std_dev"],
            )
        )
        # asymptomatic
        if random.uniform(0,1) < self.asymptomatic_probabilty:
            time *=2
            person.asymptomatic = True
        person.time_to_quarantine = time if time > 0 else 0
        self.I.append(person.ID)

    def interaction(self, person2):
        if person2.ID in self.S:
            self.infect(person2)

    # MAIN ---------------------------------------------------------------------
    def simulate(self, network, p, number_of_first_infected, contacts_per_timestep):
        """
        Docstring todo
        """

        population_size = network.population_size

        # Initialize compartment ID lists
        population = network.get_population()
        self.S = list(population.keys())  # Susceptibles
        self.I = []
        self.R = []

        # Initialize contact counter
        #self.contact_counter = Contact_Counter(population.keys())

        # ------------------------------------------------------------------------------ #
        # First infected
        # ------------------------------------------------------------------------------ #
        for i in range(number_of_first_infected):
            first_infected_ID = random.choice(self.S)
            first_infected = population[first_infected_ID]
            self.infect(first_infected)

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
            #random_order = np.random.permutation(population_size)

            #For every person we draw N random contacts from therer contacts list
            #and try to infect them this is depending on weights
            for node_ID in self.I:
                edge_IDs = network.edges(node_ID)
                weights = [network.edges[edge_ID]["weights"][node_ID] for edge_ID in edge_IDs]
                neighbor_nodes = [edge_ID[1] for edge_ID in edge_IDs]

                neighbor_nodes_random = np.random.choice(neighbor_nodes,contacts_per_timestep,weights)
                for neighbor_node_random in neighbor_nodes_random:
                    if random.uniform(0,1) < self.infection_probability:
                        self.interaction(network.nodes[neighbor_node_random]["person"])

            # Random infection in public
            """infected = []
            for ID in copy.deepcopy(self.S):
                person = network.nodes[ID]["person"]
                if random.uniform(0, 1) < p * len(self.I) / (len(self.S) + len(self.I) + len(self.R)):
                    self.infect(person)"""

            # Quarantining infectious people
            # or recovering them if they were asymptotic
            quarantined = []
            for ID in self.I:
                person = network.nodes[ID]["person"]
                person.time_to_quarantine -= 1
                if person.time_to_quarantine < 1:
                    quarantined.append(ID)
                    if person.asymptomatic:
                        person.asymptomatic = False
                        self.R.append(ID)
                    else:
                        person.time_to_recovery = self.time_until_recovery
                        self.Q.append(ID)
            for ID in quarantined:
                self.I.remove(ID)

            # Recovery
            recovered = []
            for ID in self.Q:
                person = network.nodes[ID]["person"]
                person.time_to_recovery -= 1
                if person.time_to_recovery < 1:
                    recovered.append(ID)
                    self.R.append(ID)
            for ID in recovered:
                self.Q.remove(ID)

            # Update compartment numbers
            S_t.append(len(self.S))
            I_t.append(len(self.I) + len(self.Q))

            simulation_time += 1

        # Average contact counts
        #self.contact_counter.calculate_average_daily_contacts(self.time_limit)
        #average_daily_contact = self.contact_counter.calculate_population_average_daily_contacts()

        return (S_t, I_t)
