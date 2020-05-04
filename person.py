# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 14:16:10 2020

@author: iftek
"""

class Person:
    def __init__(self, ID, input_contact_list):
        self.ID = ID
        
        self.time_to_quarantine = 0
        self.time_to_recovery = 0
        
        self.contacts = input_contact_list
      
    def add_contact(self, contactID):
        self.list_of_contacts.append(contactID)
        
    def set_list_of_contacts(self, input_list_of_contacts):
        self.list_of_contacts = input_list_of_contacts

            
    def print_data(self):
        str1 = "Data of person with ID {}:".format(self.ID)
        #str2 = "Type: {}".format(self.type)
        str3 = "Conacts: {}".format(self.contacts)
        str4 = "Degree: {}".format(self.degree)
        print(str1)
        print(str2)
        print(str4)
        print(str3)
        if self.recruited:
            print("Recruiter ID: {}".format(self.recruiter))