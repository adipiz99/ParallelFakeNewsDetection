import os
import pyNetLogo
import pandas as pd
from pathlib import Path
from test_1_parameters import *

netlogo_path = os.path.abspath("/home/musimathicslab/FakeNewsDetection/NetLogo 6.2.2")
netlogo = pyNetLogo.NetLogoLink(gui=False, netlogo_home=netlogo_path)
modelfile = os.path.abspath('netlogo/FakeNewsSimulation.nlogo')
netlogo.load_model(modelfile)
netlogoCommands = NetlogoCommands(netlogo, modelfile)

ticks = netlogoCommands.get_total_ticks()
ticks = int(ticks)

tresholds = test_1.tresholds
network_polarization = test_1.network_polarization[0:3]

netlogoCommands.set_opinion_polarization(0)
netlogoCommands.set_initial_opinion_metric_value(0.5)


global_cascades = []
global_cascades_means = []
df = pd.DataFrame({"Treshold": [], "Network Polarization": [],'Virality': []})

for i in range(len(network_polarization)):
    netlogoCommands.set_network_polarization(network_polarization[i])
    print("P_N is set to: {}".format(netlogo.report("P_N")))
    for j in range(len(tresholds)):
        netlogoCommands.set_treshold(tresholds[j])
        print("teta is set to: {}".format(netlogo.report("teta")))
        global_cascades = []
        for k in range (test_1.number_of_iterations):
            netlogoCommands.setup()
            for l in range (ticks):
                netlogoCommands.go()
            global_cascades.append(netlogoCommands.get_global_cascade_fraction())

        new_df = pd.DataFrame({"Treshold": [tresholds[j]], "Network Polarization": [network_polarization[i]], 'Virality': [calculate_fraction(global_cascades)]})
        df = pd.concat([df, new_df], ignore_index=True)

filepath = Path(test_1.path + 'test_1_1.csv')  
filepath.parent.mkdir(parents=True, exist_ok=True)  
df.to_csv(filepath)

netlogo.kill_workspace()
