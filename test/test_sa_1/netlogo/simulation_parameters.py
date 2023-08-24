class NetlogoSimulationParameters:

    #Number of ticks before stopping the simulation
    NumberOfTicks = 100

    WarningWeight = 10
    ReiterateWeight = 3
    StaticWeight = 5
    GoWeight = 2

    # rewiring params
    rewiring = True
    rewire_prob = 0.1 # probability of rewiring a single edge. If the treshold is not met, the edge is not rewired.

    def __init__(self):
        pass

    def get_rewiring(self):
        return self.rewiring