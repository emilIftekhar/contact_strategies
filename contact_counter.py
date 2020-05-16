

class Contact_Counter:
    def __init__(self, population_IDs):
        self.contact_counts = {}
        for ID in population_IDs:
            self.contact_counts[ID] = 0

    def count_contacts(self, person1_ID, person2_ID):
        self.contact_counts[person1_ID] += 1
        self.contact_counts[person2_ID] += 1

    def calculate_average_daily_contacts(self, number_of_days):
        self.average_daily_contacts = {}
        for ID in self.contact_counts.keys():
            self.average_daily_contacts[ID] = self.contact_counts[ID] / number_of_days

    def calculate_population_average_daily_contacts(self):
        total = sum(self.average_daily_contacts.values())
        length = len(self.average_daily_contacts)
        average = total / length
        print("The average number of daily contacts that a person has each day is {}".format(average))
        return average
