class NetlogoSimulationParameters:

    #Number of ticks before stopping the simulation
    NumberOfTicks = 100

    WarningWeight = 10
    ReiterateWeight = 3
    StaticWeight = 5
    GoWeight = 2
    
    growth_percentages = [80, 60, 50, 30, 20, 10] # Percentages of network growth
    growth_ticks = [50, 100, 200, 300, 400, 500] # Ticks necessary to reach the next growth percentage

    def setWarningWeight(self, value):
        self.WarningWeight = value

    def setReiterateWeight(self, value):
        self.ReiterateWeight = value
    
    def setStaticWeight(self, value):
        self.StaticWeight = value
    
    def setGoWeight(self, value):
        self.GoWeight = value
    
    def setNumberOfTicks(self, value):
        self.NumberOfTicks = value

    def getWarningWeight(self):
        return self.WarningWeight
    
    def getReiterateWeight(self):
        return self.ReiterateWeight
    
    def getStaticWeight(self):
        return self.StaticWeight
    
    def getGoWeight(self):
        return self.GoWeight
    
    def getNumberOfTicks(self):
        return self.NumberOfTicks
    
    def getSimulationParameters(self):
        return [self.WarningWeight, self.ReiterateWeight, self.StaticWeight, self.GoWeight, self.NumberOfTicks]
    
    def setSimulationParameters(self, parameters):
        self.WarningWeight = parameters[0]
        self.ReiterateWeight = parameters[1]
        self.StaticWeight = parameters[2]
        self.GoWeight = parameters[3]
        self.NumberOfTicks = parameters[4]

    def getGrowthPercentages(self):
        return self.growth_percentages
    
    def getGrowthTicks(self):
        return self.growth_ticks
    
    def setGrowthPercentages(self, percentages):
        if(len(percentages) == len(self.growth_ticks)):
            self.growth_percentages = percentages
            return True
        return False

    def setGrowthTicks(self, ticks):
        if(len(ticks) == len(self.growth_percentages)):
            self.growth_ticks = ticks
            return True
        return False

    def setGrowthParameters(self, percentages, ticks):
        if(len(percentages) == len(ticks)):
            self.growth_percentages = percentages
            self.growth_ticks = ticks
            return True
        return False
    
    def __init__(self):
        pass