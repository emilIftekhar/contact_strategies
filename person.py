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

    
