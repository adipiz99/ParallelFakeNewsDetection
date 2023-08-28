import os
import time
import pyNetLogo
import pandas as pd
from pathlib import Path
from environment.fake_news_diffusion_env import FakeNewsSimulation
from deepq_simulation import DeepQLearning
from test_5_parameters import *
from mpi4py import MPI

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size() # Number of processes
file_name = "test_" + str(rank + 1) + ".csv"
netlogo_path = os.path.abspath("/home/musimathicslab/FakeNewsDetection/NetLogo 6.2.2")


params = test_sa_5()
netlogo = pyNetLogo.NetLogoLink(gui=False, netlogo_home=netlogo_path)
modelfile = os.path.abspath('netlogo/FakeNewsSimulation.nlogo')
netlogo.load_model(modelfile)
netlogoCommands = NetlogoCommands(netlogo, modelfile)
env = FakeNewsSimulation(netlogoCommands)

netlogoCommands = NetlogoCommands(netlogo, modelfile)
netlogoCommands.set_opinion_polarization(test_sa_5.opinion_polarization)
netlogoCommands.set_initial_opinion_metric_value(0.5)
netlogoCommands.set_echo_chamber_fraction(test_sa_5.echo_chamber_fraction)
netlogoCommands.set_opinion_metric_step(test_sa_5.opinion_metric_step)
netlogoCommands.set_nodes(test_sa_5.nb_nodes)
env.set_most_influent_a_nodes_criteria(10, test_sa_5.choose_method)
netlogoCommands.set_warning(test_sa_5.warning)
netlogoCommands.set_node_range_static_b(test_sa_5.node_range_static_b)
netlogoCommands.set_node_range(test_sa_5.node_range)
netlogoCommands.set_warning_impact(test_sa_5.warning_impact)
netlogoCommands.set_warning_impact_neutral(test_sa_5.warning_impact_neutral)

# Setup dynamic network params
rewiring = env.rewire()
if (not rewiring):
    env.netlogo.toggle_rewire()

growing = env.grow()
if (not growing):
    env.netlogo.toggle_growth()

leaving = env.leave()
if (not leaving):
    env.netlogo.toggle_leaving()

growth_percentages = [80, 60, 50, 30, 20, 10] # Percentages of network growth
growth_ticks = [20, 30, 50, 70, 90, 100] # Ticks necessary to reach the next growth percentage
leave_percentages = [5, 10, 15, 20, 25, 30] # Percentages of leaving nodes
leave_ticks = [20, 30, 50, 70, 90, 100] # Ticks necessary to reach the next leave percentage
rewire_probability = 0.3 # Probability of rewiring a node

env.params.setGrowthPercentages(growth_percentages)
env.params.setGrowthTicks(growth_ticks)
env.params.setLeavePercentages(leave_percentages)
env.params.setLeaveTicks(leave_ticks)
netlogoCommands.set_rewire_probability(rewire_probability)

# end dynamic network params

total_nodes = netlogoCommands.get_total_agents()
total_ticks = netlogoCommands.get_total_ticks()

ticks = netlogoCommands.get_total_ticks()
ticks = int(ticks)
dql = DeepQLearning()

tresholds = test_sa_5.tresholds
params.set_dynamic_network_polarization(size)
network_polarization = []

for i in range(0, size):
    if (rank == i):
        network_polarization = [params.network_polarization[i]]

global_cascades = []
global_cascades_means = []
df = pd.DataFrame({"Treshold": [], "Network Polarization": [],'Virality': []})
print("Warning impact set to {}".format(netlogo.report("warning-impact")))
print("Warning impact neutral set to {}".format(netlogo.report("warning-impact-neutral")))
start_time = time.time()

for i in range(len(network_polarization)):
    netlogoCommands.set_network_polarization(network_polarization[i])
    print("P_N is set to: {}".format(netlogo.report("P_N")))
    for j in range(len(tresholds)):
        netlogoCommands.set_treshold(tresholds[j])
        print("teta is set to: {}".format(netlogo.report("teta")))
        global_cascades = []

        print("Training model")
        dql.run_model_training(env, netlogoCommands, test_sa_5.number_of_iterations)

        print("Testing model")
        for k in range (test_sa_5.number_of_iterations):
            obs = env.reset()
            for l in range (ticks):
                if (l == 0):
                    obs = env.step(0)
                elif (l % test_sa_5.sa_delay == 0):
                    obs = dql.predict_sa_action(env, obs)
                else:
                    obs = env.step(0)
            global_cascades.append(netlogoCommands.get_global_cascade_fraction())

        new_df = pd.DataFrame({"Treshold": [tresholds[j]], "Network Polarization": [network_polarization[i]], 'Virality': [calculate_fraction(global_cascades)]})
        df = pd.concat([df, new_df], ignore_index=True)

total_time = (time.time() - start_time)/60
print("Total time %s minutes ---" % total_time)
filepath = Path(test_sa_5.path + file_name)  
filepath.parent.mkdir(parents=True, exist_ok=True)  
df.to_csv(filepath)

netlogo.kill_workspace()