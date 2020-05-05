import numpy as np
import random

class Disease_Propagator:
    def __init__(self, time_limit, time_until_recovery, mean_time_until_quarantine, std_dev_time_until_quarantine):
        self.time_limit = time_limit

        self.time_until_recovery = time_until_recovery
        self._time_until_quarantine = {  "mean": mean_time_until_quarantine,
                                        "std_dev": std_dev_time_until_quarantine}


    def interaction(self, person1, person2):
        if person1.ID in self.S and person2.ID in self.I:
            self.S.remove(person1.ID)
            time = int(np.random.normal(self._time_until_quarantine['mean'], self._time_until_quarantine['std_dev']))
            person1.time_to_quarantine = time if time>0 else 0
            self.I.append(person1.ID)
        elif  person1.ID in self.I and person2.ID in self.S:
            self.S.remove(person2.ID)
            time = int(np.random.normal(self._time_until_quarantine['mean'], self._time_until_quarantine['std_dev']))
            person2.time_to_quarantine = time if time>0 else 0
            self.I.append(person2.ID)

    def simulate(self, network, p):
        """
        Docstring todo
        """

        population_size = network.population_size

        # Initialize compartment ID lists
        population = network.get_population()
        self.S = list(population.keys()) # Susceptibles
        first_infected = random.choice(list(population.values()))
        first_infected.time_to_quarantine = np.random.normal(self._time_until_quarantine['mean'], self._time_until_quarantine['std_dev'])
        self.I = [first_infected.ID] # Infectious
        self.S.remove(first_infected.ID)
        self.Q = [] # Quarantined

        # Initialize compartment size time series
        S_t = [] # Number of susceptibles
        I_t = [] # Number of infected

        simulation_time = 0
        while simulation_time < self.time_limit:
            # Simulate one random interaction process for each person in population
            random_order = np.random.permutation(population_size)
            for ID in random_order:
                person1 = network.nodes[ID]['person']
                for contact_ID in np.random.permutation(person1.contacts):
                    person2 =  network.nodes[contact_ID]['person']
                    if random.uniform(0,1) < network.edges[(ID,contact_ID)]['weight']:
                        self.interaction(person1, person2)

            # Random infection in public
            infected = []
            for ID in self.S:
                person = network.nodes[ID]['person']
                if random.uniform(0,1) < p*len(self.I)/(len(self.S)+len(self.I)):
                    infected.append(ID)
                    time = int(np.random.normal(self._time_until_quarantine['mean'], self._time_until_quarantine['std_dev']))
                    person.time_to_quarantine = time if time>0 else 0
                    self.I.append(person.ID)
            for ID in infected:
                self.S.remove(ID)

            # Quarantining infectious people
            quarantined = []
            for ID in self.I:
                person = network.nodes[ID]['person']
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
                person = network.nodes[ID]['person']
                person.time_to_recovery -= 1
                if person.time_to_recovery < 1:
                    recovered.append(person.ID)
                    self.S.append(person.ID)
            for ID in recovered:
                self.Q.remove(ID)

            # Update compartment numbers
            S_t.append(len(self.S))
            I_t.append(len(self.I)+len(self.Q))

            simulation_time += 1

        return (S_t, I_t)
