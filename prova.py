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

netlogo = pyNetLogo.NetLogoLink(gui=True)
modelfile = os.path.abspath('./netlogo/FakeNewsSimulation.nlogo')
netlogoCommands = NetlogoCommands(netlogo, modelfile)
env = FakeNewsSimulation(netlogoCommands)
env.netlogo.setup()

rewired = env.rewire()
growth = env.grow()
leave = env.leave()

print("Rewired: " + str(rewired))
print("Growth: " + str(growth))
print("Leave: " + str(leave))

env.netlogo.toggle_rewire()
env.netlogo.toggle_growth()
env.netlogo.toggle_leaving()

growth = env.grow()
# growth = env.grow()
# growth = env.grow()

leave = env.leave()
leave = env.leave()
# leave = env.leave()
# leave = env.leave()
rewired = env.rewire()
print("Leave: " + str(leave))
print("Rewired: " + str(rewired))
print("Growth: " + str(growth))

env.netlogo.kill_workspace()