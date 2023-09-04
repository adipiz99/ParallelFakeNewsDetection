from gymnasium import Env, spaces
import numpy as np
import random
import copy
import pandas as pd
from environment.environment_utils import EnvironmentUtils
from netlogo.simulation_controls import NetlogoCommands
from netlogo.simulation_parameters import NetlogoSimulationParameters

class FakeNewsSimulation(Env):
    netlogo = 0
    environment_utils = 0
    params = NetlogoSimulationParameters()
    tick_count_started = False
    proc_id = 0

    def __init__(self, netlogoCommands : NetlogoCommands, process_id):
        super(FakeNewsSimulation, self).__init__()

        print("Initialinzing the environment...")
        
        self.netlogo = netlogoCommands
        self.environment_utils = EnvironmentUtils()
        self.proc_id = process_id

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
        rewiring = self.netlogo.get_rewire()
        if (not rewiring):
            self.netlogo.toggle_rewire()

        growing = self.netlogo.get_growth()
        if (not growing):
            self.netlogo.toggle_growth()

        leaving = self.netlogo.get_leaving()
        if (not leaving):
            self.netlogo.toggle_leaving()

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
        self.netlogo.export_network("world_{}.csv".format(self.proc_id))

        if(not is_rewiring_active):
            return False

        # Input
        data_file = "./netlogo/world_{}.csv".format(self.proc_id)

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
        df = pd.read_csv(data_file, header=None, delimiter=data_file_delimiter, names=column_names, low_memory=False)

        begin_index = 0
        end_index = 0
        counting_agents = False
        max_agent_id = 0
        super_agent_id = 0
        agent_ids = []

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
                    #saving every existing id
                    agent_ids.append(value)
                
                if(row[8] == '{breed super-agents}'):
                    super_agent_id = value

        # print(len(agent_ids))
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
                if(random.random() <= rewire_prob):
                    #generate a random between 0 and max_agent_id
                    random_agent_id = random.choice(agent_ids)
                    current_agent_id = int(row[0].split(' ')[1].split('}')[0])

                    while random_agent_id == current_agent_id:
                        random_agent_id = random.choice(agent_ids)

                    if random_agent_id != super_agent_id:
                        df.at[index, 1] = '{basic-agent ' + str(random_agent_id) + '}'
                    else:
                        df.at[index, 1] = '{super-agent ' + str(random_agent_id) + '}'

        #remove header
        df1 = df.tail(-1)
        df1.to_csv("./netlogo/world_{}.csv".format(self.proc_id), index=False, header=False)

        self.netlogo.import_network("world_{}.csv".format(self.proc_id))
        return True

    def grow(self):
        is_network_growing = self.netlogo.get_growth()

        if(is_network_growing):
            if(self.tick_count_started):
                tick = self.netlogo.get_current_tick()
            else:  
                self.tick_count_started = True
                tick = 0
        
            growth_ticks = self.params.getGrowthTicks()
            growth_percentages = self.params.getGrowthPercentages()
            index = 0

            for tick_step in growth_ticks:
                if(tick > tick_step):
                    index += 1
                elif(tick <= tick_step):
                    break

            if index >= len(growth_percentages): # if the index is out of bounds, set it to the last index
                index = len(growth_percentages) - 1

            if(tick == growth_ticks[index]):
                # print("grow attivata")
                growth_percentage = growth_percentages[index]
                basic_agents = self.netlogo.get_total_agents()
                agents_to_add = int((basic_agents/100)*growth_percentage)

                self.netlogo.add_agents(agents_to_add)
                return True
        return False
    
    def leave(self):
        is_nodes_leaving = self.netlogo.get_leaving()

        if(is_nodes_leaving):
            if(self.tick_count_started):
                tick = self.netlogo.get_current_tick()
            else:  
                self.tick_count_started = True
                tick = 0
            leave_ticks = self.params.getLeaveTicks()
            leave_percentages = self.params.getLeavePercentages()
            index = 0

            for tick_step in leave_ticks:
                if(tick > tick_step):
                    index += 1
                elif(tick <= tick_step):
                    break

            if index >= len(leave_percentages): # if the index is out of bounds, set it to the last index
                index = len(leave_percentages) - 1

            if(tick == leave_ticks[index]):
                # print("leave attivata")
                leave_percentage = leave_percentages[index]
                basic_agents = self.netlogo.get_total_agents()
                agents_to_remove = int((basic_agents/100)*leave_percentage)

                self.netlogo.remove_agents(agents_to_remove)
                return True
        return False
    
    def calculate_repetition_bias(self, agents_with_counters):
        new_dictionary = {}
        ids = self.netlogo.get_agent_ids()

        for id in ids:
            prev_a_count, prev_b_count, a_news_in_row, b_news_in_row = agents_with_counters[id]
            new_a_count = self.netlogo.get_a_counter_by_id(id)
            new_b_count = self.netlogo.get_b_counter_by_id(id)
            print("id: " + str(id) + " prev a: " + str(prev_a_count)+ " new a: " + str(new_a_count))
            print("id: " + str(id) + " prev b: " + str(prev_b_count)+ " new b: " + str(new_b_count))

            # se arriva una nuova notizia di tipo a aumentiamo il bias di a
            if new_a_count > prev_a_count:

                old_a_news_in_row = copy.copy(a_news_in_row)
                a_news_in_row += (new_a_count - prev_a_count)

                # setto il nuovo valore del bias di a (se vengo esposto da più notizie di tipo a che di b)
                # e setto il bias di b a 0 poichè uno solo dei due può essere attivo
                # questo permette anche di poter calcolare il bias sulla quantità di notizie consecutive di un determinato tipo
                if new_a_count > new_b_count:
                    a_bias = self.netlogo.get_repetition_a_bias_by_id(id)
                    # scelgo di quanto deve aumentare il bias in base a quante a news di fila ha ricevuto
                    b_news_in_row = 0
                    rep_bias_value= self.calculate_repetition_bias_growth(a_news_in_row, old_a_news_in_row)
                    print("rep bias to add: " + str(rep_bias_value))

                    self.netlogo.set_repetition_a_bias(a_bias[0] + rep_bias_value, id)
                    self.netlogo.set_repetition_b_bias(0, id)
                    # per la print
                    a_bias = self.netlogo.get_repetition_a_bias_by_id(id)
                    print("id: " + str(id) + "  a bias: " + str(a_bias[0]))
                new_dictionary[id] = (new_a_count, prev_b_count, a_news_in_row, b_news_in_row)

            # se arriva una nuova notizia di tipo b aumentiamo il bias di b
            if new_b_count > prev_b_count:
                
                old_b_news_in_row = copy.copy(b_news_in_row)
                b_news_in_row += (new_b_count - prev_b_count)

                if new_b_count > new_a_count:
                    b_bias = self.netlogo.get_repetition_b_bias_by_id(id)
                    # scelgo di quanto deve aumentare il bias in base a quante b news di fila ha ricevuto
                    a_news_in_row = 0
                    rep_bias_value= self.calculate_repetition_bias_growth(b_news_in_row, old_b_news_in_row)
                    print("rep bias to add: " + str(rep_bias_value))

                    self.netlogo.set_repetition_b_bias(b_bias[0] + rep_bias_value, id)
                    self.netlogo.set_repetition_a_bias(0, id)
                    # per la print
                    b_bias = self.netlogo.get_repetition_b_bias_by_id(id)
                    print("id: " + str(id) + "  b bias: " + str(b_bias[0]))
                new_dictionary[id] = (prev_a_count, new_b_count, a_news_in_row, b_news_in_row)
            
            # se non arriva nessuna notizia settiamo i vecchi valori (e il bias non viene aggiornato)
            if (new_a_count == prev_a_count and new_b_count == prev_b_count):
                new_dictionary[id] = (prev_a_count, prev_b_count, a_news_in_row, b_news_in_row)


        return new_dictionary
    
    def calculate_repetition_bias_growth(self, news_in_row, old_news_in_row):
        bias_ticks = self.params.getBiasTicks()
        rep_bias_values = self.params.getRepetitionBiasValues()
        rep_bias_value = 0
        index = 0

        for step in bias_ticks:
            if(news_in_row > step):
                index += 1
            elif(news_in_row <= step):
                break

        if index >= len(rep_bias_values): # if the index is out of bounds, set it to the last index
            index = len(rep_bias_values) - 1

        # aggiungiamo il bias ogni 5 news ricevute di fila
        if news_in_row % 5 == 0:
            rep_bias_value = rep_bias_values[index]
        # aggiungiamo anche un aggiornamento se ha superato un multiplo di 5 
        elif news_in_row > 5 and (old_news_in_row // 5) < (news_in_row // 5):
            rep_bias_value = rep_bias_values[index]

        return rep_bias_value
