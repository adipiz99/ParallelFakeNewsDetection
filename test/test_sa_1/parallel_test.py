import os
import time
import pyNetLogo
import pandas as pd
from pathlib import Path
from environment.fake_news_diffusion_env import FakeNewsSimulation
from deepq_simulation import DeepQLearning
from test_1_parameters import *
from mpi4py import MPI

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size() # Number of processes
file_name = "test_" + str(rank + 1) + ".csv"

#Netlogo info (linux only)
netlogo_path = os.path.abspath("/home/musimathicslab/FakeNewsDetection/NetLogo 6.2.2")
# netlogo_version = "6.3.0"

params = test_sa_1()
netlogo = pyNetLogo.NetLogoLink(gui=False)#, netlogo_home=netlogo_path)#, netlogo_version=netlogo_version)
modelfile = os.path.abspath('netlogo/FakeNewsSimulation.nlogo')
netlogo.load_model(modelfile)
netlogoCommands = NetlogoCommands(netlogo, modelfile)
env = FakeNewsSimulation(netlogoCommands, rank)

netlogoCommands = NetlogoCommands(netlogo, modelfile)
netlogoCommands.set_opinion_polarization(test_sa_1.opinion_polarization)
netlogoCommands.set_initial_opinion_metric_value(0.5)
netlogoCommands.set_echo_chamber_fraction(test_sa_1.echo_chamber_fraction)
# netlogoCommands.set_opinion_metric_step(test_sa_1.opinion_metric_step)
netlogoCommands.set_nodes(test_sa_1.nb_nodes)
env.set_most_influent_a_nodes_criteria(10, test_sa_1.choose_method)
netlogoCommands.set_warning(test_sa_1.warning)
netlogoCommands.set_node_range_static_b(test_sa_1.node_range_static_b)
netlogoCommands.set_node_range(test_sa_1.node_range)
netlogoCommands.set_warning_impact(test_sa_1.warning_impact)
netlogoCommands.set_warning_impact_neutral(test_sa_1.warning_impact_neutral)

# Setup dynamic network params
rewiring = env.netlogo.get_rewire()
if (not rewiring):
    env.netlogo.toggle_rewire()

growing = env.netlogo.get_growth()
if (not growing):
    env.netlogo.toggle_growth()

leaving = env.netlogo.get_leaving()
if (not leaving):
    env.netlogo.toggle_leaving()

growth_percentages = [10, 15, 14, 26, 17, 10, 10, 16, 14, 5] # Percentages of network growth
growth_ticks = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100] # Ticks necessary to reach the next growth percentage
leave_percentages = [2, 3, 3, 5, 2, 2, 3, 3, 4, 2] # Percentages of leaving nodes
leave_ticks = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]# Ticks necessary to reach the next leave percentage
rewire_probability = 0.3 # Probability of rewiring a node
# repetition_bias_values = [0.05, 0.10, 0.15, 0.20] # Values of bias growth
# bias_ticks = [30, 50, 70, 100] # Number of consecutive news necessary to reach the next value of bias growth

env.params.setGrowthPercentages(growth_percentages)
env.params.setGrowthTicks(growth_ticks)
env.params.setLeavePercentages(leave_percentages)
env.params.setLeaveTicks(leave_ticks)
netlogoCommands.set_rewire_probability(rewire_probability)
# end dynamic network params
# env.params.setRepetitionBiasValues(repetition_bias_values)
# env.params.setBiasTicks(bias_ticks)
# end bias params

total_nodes = netlogoCommands.get_total_agents()
total_ticks = netlogoCommands.get_total_ticks()

ticks = netlogoCommands.get_total_ticks()
ticks = int(ticks)
dql = DeepQLearning()

tresholds = test_sa_1.tresholds
params.set_dynamic_network_polarization(size)
network_polarization = []

for i in range(0, size):
    if (rank == i):
        network_polarization = [params.network_polarization[i]]


global_cascades = []
global_cascades_means = []
df = pd.DataFrame({"Treshold": [], "Network Polarization": [],'Virality': []})
start_time = time.time()

for i in range(len(network_polarization)):
    netlogoCommands.set_network_polarization(network_polarization[i])
    print("P_N is set to: {}".format(netlogo.report("P_N")))
    for j in range(len(tresholds)):
        netlogoCommands.set_treshold(tresholds[j])
        print("teta is set to: {}".format(netlogo.report("teta")))
        global_cascades = []

        print("Training model")
        dql.run_model_training(env, netlogoCommands, test_sa_1.number_of_iterations)

        print("Testing model")
        for k in range (test_sa_1.number_of_iterations):
            obs = env.reset()
            for l in range (ticks):
                if (l == 0):
                    obs = env.step(0)
                elif (l % test_sa_1.sa_delay == 0):
                    obs = dql.predict_sa_action(env, obs)
                else:
                    obs = env.step(0)
            global_cascades.append(netlogoCommands.get_global_cascade_fraction())

        new_df = pd.DataFrame({"Treshold": [tresholds[j]], "Network Polarization": [network_polarization[i]], 'Virality': [netlogoCommands.calculate_fraction(global_cascades)]})
        df = pd.concat([df, new_df], ignore_index=True)

total_time = (time.time() - start_time)/60
print("Total time %s minutes ---" % total_time)
filepath = Path(test_sa_1.path + file_name)  
filepath.parent.mkdir(parents=True, exist_ok=True)  
df.to_csv(filepath)

netlogo.kill_workspace()