import numpy as np
import random

class Disease_Propagator:
    def __init__(self, time_limit, mean_time_until_quarantine, std_dev_time_until_quarantine):
        self.time_limit = time_limit
        self.time = 0
        # Initialize compartment size time series
        self.S_t = [] # Number of susceptibles
        self.I_t = [] # Number of infected

        self._time_until_quarantine = {  "mean": mean_time_until_quarantine,
                                        "std_dev": std_dev_time_until_quarantine}


    def simulate(self, network, S, I, Q, time_until_recovery, p):
        """
        Docstring todo
        """

        population_size = network.population_size
        
        while self.time < self.time_limit:
            # Simulate one random interaction process for each person in population
            random_order = np.random.permutation(population_size)
            for ID in random_order:
                person1 = network.nodes[ID]['person']
                contact_ID = random.choice(person1.contacts)
                person2 =  network.nodes[contact_ID]['person']
                if person1.ID in S and person2.ID in I:
                    S.remove(person1.ID)
                    time = int(np.random.normal(self._time_until_quarantine['mean'], self._time_until_quarantine['std_dev']))
                    person1.time_to_quarantine = time if time>0 else 0
                    I.append(person1.ID)
                elif  person1.ID in I and person2.ID in S:
                    S.remove(person2.ID)
                    time = int(np.random.normal(self._time_until_quarantine['mean'], self._time_until_quarantine['std_dev']))
                    person2.time_to_quarantine = time if time>0 else 0
                    I.append(person2.ID)

            # Random infection in public
            infected = []
            for ID in S: 
                person = network.nodes[ID]['person']
                if random.uniform(0,1) < p*len(I)/(len(S)+len(I)):
                    infected.append(ID)
                    time = int(np.random.normal(self._time_until_quarantine['mean'], self._time_until_quarantine['std_dev']))
                    person.time_to_quarantine = time if time>0 else 0
                    I.append(person.ID)
            for ID in infected:
                S.remove(ID)

            # Quarantining infectious people
            quarantined = []
            for ID in I:
                person = network.nodes[ID]['person']
                person.time_to_quarantine -= 1
                if person.time_to_quarantine == 0:
                    quarantined.append(person.ID)
                    person.time_to_recovery = time_until_recovery
                    Q.append(person.ID)
            for ID in quarantined:
                I.remove(ID)

            # Recovery
            recovered = []
            for ID in Q:
                person = network.nodes[ID]['person']
                person.time_to_recovery -= 1
                if person.time_to_recovery == 0:
                    recovered.append(person.ID)
                    S.append(person.ID)
            for ID in recovered:
                Q.remove(ID)

            # Update compartment numbers
            self.S_t.append(len(S))
            self.I_t.append(len(I)+len(Q))

            self.time += 1
            
        return (self.S_t, self.I_t)