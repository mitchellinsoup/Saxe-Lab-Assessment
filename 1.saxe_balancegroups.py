import os
import numpy as np
import secrets #https://docs.python.org/3/library/secrets.html
from itertools import permutations
import pandas as pd

# Welcome to FoodFoodFood Foundation, where we put the food in, well, your food!
# In an effort to support our subjects -
# I mean, loyal customers, we're trying to do more research to see you humans-
# I mean, we humans, tend to eat your - 
# I mean, our food!
# 
# Here, we propose a simple experiment, take give 4 groups of you 4 different food groups we call FactorA, 
# and we ask you to eat it in 4 different, very human, methods FactorB and FactorC.
# Naturally, FactorA includes: [icecream=1, soup=2, pasta=3, salsa=4], FactorB includes: [chopsticks=X, toes=Y] (intuitive?), and 
# FactorC: [Left hand (L), Right elbow (R)]. Just like at home! Here's your group assigment below and the order in which
# you must eat your food. Salutations.
# From, 
# FoodFoodFOOOOD (scary monster sound)

def create_subj(n):
    subjects = []
    for i in range(round(n)):
        subjects.append("Subject_" + str(i+1))
    return subjects    

subjects = create_subj(100) # example with n = 100

def oopsImeanCUSTOMERS(subjects):  # create sample
    customers = []
    for i in range(len(subjects)):
        customers.append("Customer_"+ subjects[i].split("_")[1])
    return customers    

subjects = oopsImeanCUSTOMERS(subjects) # glad we caught that!

FactorB = ["X", "Y"]
FactorC = ["L", "R"]

task_permut = list(permutations(FactorB + FactorC)) # get all permutations of this set

A_1 = []    # FactorA grouping
A_2 = []  
A_3 = []  
A_4 = []      

task_assign = [] # where we'll put the task sequences for participants 

for i in range(len(subjects)): # initial randomization to groups + add in 
    random_num = secrets.randbelow(len(subjects))

    task_assign.append(task_permut[secrets.randbelow(len(task_permut))]) #taking a random element from all permutations of FactorB and C

    if random_num%4 == 0: #depending on remainder, we get group assignment to 0,1,2,3 (or 1,2,3,4)
        A_1.append(subjects[i])
    if random_num%4 == 1:
        A_2.append(subjects[i])
    if random_num%4 == 2:
        A_3.append(subjects[i])
    if random_num%4 == 3:
        A_4.append(subjects[i])

groups = [A_1, A_2, A_3, A_4]
sizes = [len(groups[0]), len(groups[1]), len(groups[2]), len(groups[3])] # organize groups sizes to prepare balancing

var = np.var(sizes)

while var > 0:    # to balance, minimize size variance between groups, if loop leaves us with constant var, break
    
    max = pd.Series(sizes).idxmax()
    min = pd.Series(sizes).idxmin()
    groups[min].append(groups[max][-1]) # add element from max group to min group
    groups[max] = groups[max][:-1] # remove element and repeat as needed
    sizes = [len(groups[0]), len(groups[1]), len(groups[2]), len(groups[3])]

    var_old = var
    var = np.var(sizes)
    if var == var_old: #break if we reach a floor in variance minimization
        break

group_labels = []

for i in range(len(sizes)):
    group_labels = group_labels + [str(i+1)]*sizes[i] # produce column of labels based on size of each group

subjects = groups[0] + groups[1] + groups[2] + groups[3] #combining all subjects in order based on group

assignments = pd.DataFrame({'Group': group_labels, 'Subject/Customer': subjects, 'Task seq':task_assign}) #organize in DF

assignments.to_csv('AssignmentEX.csv', index=False) # output csv
