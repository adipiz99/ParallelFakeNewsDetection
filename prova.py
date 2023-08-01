import pandas as pd
import tensorflow as tf
import numpy as np
from tensorflow import keras
import pyNetLogo
import os
from collections import deque
import random
from environment.fake_news_diffusion_env import FakeNewsSimulation
from netlogo.simulation_controls import NetlogoCommands
import seaborn as sns
import matplotlib.pyplot as plt
import gymnasium as gym
import time
from mpi4py import MPI
from netlogo.simulation_parameters import NetlogoSimulationParameters

netlogo = pyNetLogo.NetLogoLink(gui=False)
modelfile = os.path.abspath('./netlogo/FakeNewsSimulation.nlogo')
netlogoCommands = NetlogoCommands(netlogo, modelfile)
env = FakeNewsSimulation(netlogoCommands)
env.netlogo.setup()

is_rewiring_active = env.netlogo.get_rewire()
rewire_prob = env.netlogo.get_rewire_probability()

if( not is_rewiring_active):
    is_rewiring_active = env.netlogo.toggle_rewire()

env.netlogo.export_network("test.csv")

# Input
data_file = "./netlogo/test.csv"

# Delimiter
data_file_delimiter = ','

# The max column count a line in the file could have
largest_column_count = 0

# Loop the data lines
with open(data_file, 'r') as temp_f:
    # Read the lines
    lines = temp_f.readlines()

    for l in lines:
        # Count the column count for the current line
        column_count = len(l.split(data_file_delimiter)) + 1
        
        # Set the new most column count
        largest_column_count = column_count if largest_column_count < column_count else largest_column_count

# Generate column names (will be 0, 1, 2, ..., largest_column_count - 1)
column_names = [i for i in range(0, largest_column_count)]

# Read csv
df = pd.read_csv(data_file, header=None, delimiter=data_file_delimiter, names=column_names)

begin_index = 0
end_index = 0
counting_agents = False
max_agent_id = 0
super_agent_id = 0

#read lines one by one
for index, row in df.iterrows():
    if(row[0] == 'TURTLES'):
        counting_agents = True
        begin_index = index + 2 #skip "TURTLES" and header

    if(counting_agents and index >= begin_index):
        if(row[0] == 'PATCHES'):
            counting_agents = False
            break

        value = int(row[0])
        if(value > max_agent_id):
            max_agent_id = value
        
        if(row[8] == '{breed super-agents}'):
            super_agent_id = value

print("max agent id: " + str(max_agent_id))
print("super agent id: " + str(super_agent_id))

rewiring = False

for index, row in df.iterrows():
    if(row[0] == 'LINKS'):
        begin_index = index + 2 #skip "LINK" and header
        rewiring = True

    if(row[0] == 'PLOTS'):
        rewiring = False
        break

    if(rewiring and index >= begin_index):
        #calculate rewiring probability
        if(random.random() > rewire_prob):
            #generate a random between 0 and max_agent_id
            random_agent_id = random.randint(0, max_agent_id)
            if random_agent_id != super_agent_id:
                df.at[index, 1] = '{basic-agent ' + str(random_agent_id) + '}'
                #df[row][1] = '{basic-agent ' + str(random_agent_id) + '}'
            else:
                df.at[index, 1] = '{super-agent ' + str(random_agent_id) + '}'
                #df[row][1] = '{super-agent ' + str(random_agent_id) + '}'

#remove header
df1 = df.tail(-1)
df1.to_csv("./netlogo/test_import.csv", index=False, header=False)

env.netlogo.import_network("test_import.csv")
env.netlogo.export_network("test2.csv")
env.netlogo.export_network("test3.csv")

env.netlogo.kill_workspace()