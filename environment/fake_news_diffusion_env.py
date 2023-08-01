from gymnasium import Env, spaces
import numpy as np
import random
import pandas as pd
from environment.environment_utils import EnvironmentUtils
from netlogo.simulation_controls import NetlogoCommands
from netlogo.simulation_parameters import NetlogoSimulationParameters

class FakeNewsSimulation(Env):
    netlogo = 0
    environment_utils = 0
    def __init__(self, netlogoCommands : NetlogoCommands):
        super(FakeNewsSimulation, self).__init__()

        print("Initialinzing the environment...")
        
        self.netlogo = netlogoCommands
        self.environment_utils = EnvironmentUtils()

        low = np.array([0.0, 0.0, 0.0])
        high = np.array([1.0, 1.0, 1.0])
        self.observation_space = spaces.Box(low, high, dtype=np.float32)
        self.action_space = spaces.Discrete(4)

        self.global_cascade = 0
        self.most_influent_b_nodes = 0
        self.global_opinion_metric_mean = 0
        self.node_span = 0
        self.criteria = ""
        self.warning = False
        self.static_b = False
        self.elements = []
    
    def set_most_influent_a_nodes_criteria(self, node_span, criteria):
        self.node_span = node_span
        self.criteria = criteria

    def reset(self, seed = None, options = None):

        super().reset(seed=seed)

        self.netlogo.setup() 
        self.global_cascade = self.netlogo.get_global_cascade_fraction()
        self.most_influent_b_nodes = self.netlogo.get_most_influent_a_nodes(self.node_span, self.criteria)
        self.global_opinion_metric_mean = self.netlogo.get_global_opinion_metric_mean()
        self.environment_utils.ResetList()
        self.environment_utils.AddValue(self.global_cascade)
        self.warning = False
        self.static_b = False
        return self.get_obs(), {}

    def get_info(self):
        return {
        }
    
    def get_obs(self):
        value = (self.global_cascade, self.most_influent_b_nodes, self.global_opinion_metric_mean)
        return np.array(value,dtype=np.float32)
    
    def step(self, action):

        terminated = False

        assert self.action_space.contains(action), "Invalid Action"

        reward = 1
        
        current_tick = self.netlogo.get_current_tick()

        self.netlogo.choose_action(action)

        if (current_tick >= NetlogoSimulationParameters.NumberOfTicks):
            terminated = True
         
        self.global_cascade = self.netlogo.get_global_cascade_fraction()
        self.most_influent_b_nodes = self.netlogo.get_most_influent_a_nodes(self.node_span, self.criteria)
        self.global_opinion_metric_mean = self.netlogo.get_global_opinion_metric_mean()

        self.environment_utils.AddValue(self.global_cascade)
        reward = self.environment_utils.CalculateReward1(action, int(self.netlogo.get_current_tick()), self.global_cascade, self.most_influent_b_nodes,
                                                          self.global_opinion_metric_mean, self.warning, self.static_b)

        if (action == 1):
            self.warning = True
        
        if (action == 3):
            self.static_b = True

        return self.get_obs(), reward, terminated, False, self.get_info()
    
    def close(self):
        self.netlogo.kill_workspace()

    def rewire(self):
        is_rewiring_active = self.netlogo.get_rewire()
        rewire_prob = self.netlogo.get_rewire_probability()
        self.netlogo.export_network("world.csv")

        if(not is_rewiring_active):
            return False

        # Input
        data_file = "./netlogo/world.csv"

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
                    current_agent_id = int(row[0].split(' ')[1].split('}')[0])

                    while random_agent_id == current_agent_id:
                        random_agent_id = random.randint(0, max_agent_id)

                    if random_agent_id != super_agent_id:
                        df.at[index, 1] = '{basic-agent ' + str(random_agent_id) + '}'
                    else:
                        df.at[index, 1] = '{super-agent ' + str(random_agent_id) + '}'

        #remove header
        df1 = df.tail(-1)
        df1.to_csv("./netlogo/world.csv", index=False, header=False)

        return True

        self.netlogo.import_network("world.csv")

