class NetlogoSimulationParameters:

    #Number of ticks before stopping the simulation
    NumberOfTicks = 100

    WarningWeight = 10
    ReiterateWeight = 3
    StaticWeight = 5
    GoWeight = 2
    
    growth_percentages = [10, 15, 14, 26, 17, 10, 10, 16, 14, 5] # Percentages of network growth
    growth_ticks = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100] # Ticks necessary to reach the next growth percentage
    leave_percentages = [2, 3, 3, 5, 2, 2, 3, 3, 4, 2] # Percentages of leaving nodes
    leave_ticks = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]# Ticks necessary to reach the next leave percentage
    repetition_bias_values = [0.05, 0.10, 0.15, 0.20] # Values of bias growth
    bias_ticks = [30, 50, 70, 100] # Number of consecutive news necessary to reach the next value of bias growth

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
    
    def getLeaveTicks(self):
        return self.leave_ticks
    
    def getLeavePercentages(self):
        return self.leave_percentages
    
    def setGrowthPercentages(self, percentages):
        if(len(percentages) == len(self.growth_ticks)):
            self.growth_percentages = percentages
            return True
        return False

    def setLeavePercentages(self, percentages):
        if(len(percentages) == len(self.leave_ticks)):
            self.leave_percentages = percentages
            return True
        return False

    def setGrowthTicks(self, ticks):
        if(len(ticks) == len(self.growth_percentages)):
            self.growth_ticks = ticks
            return True
        return False
    
    def setLeaveTicks(self, ticks):
        if(len(ticks) == len(self.leave_percentages)):
            self.leave_ticks = ticks
            return True
        return False

    def setLeaveParameters(self, percentages, ticks):
        if(len(percentages) == len(ticks)):
            self.leave_percentages = percentages
            self.leave_ticks = ticks
            return True
        return False

    def setGrowthParameters(self, percentages, ticks):
        if(len(percentages) == len(ticks)):
            self.growth_percentages = percentages
            self.growth_ticks = ticks
            return True
        return False
    
    def getRepetitionBiasValues(self):
        return self.repetition_bias_values
    
    def getBiasTicks(self):
        return self.bias_ticks
    
    def setRepetitionBiasValues(self, values):
        if(len(values) == len(self.bias_ticks)):
            self.repetition_bias_values = values
            return True
        return False
    
    def setBiasTicks(self, ticks):
        if(len(ticks) == len(self.repetition_bias_values)):
            self.bias_ticks = ticks
            return True
        return False
    
    def setRepetitionBiasParameters(self, values, ticks):
        if(len(values) == len(ticks)):
            self.repetition_bias_values = values
            self.bias_ticks = ticks
            return True
        return False
    
    def __init__(self):
        pass