class NetlogoSimulationParameters:

    #Number of ticks before stopping the simulation
    NumberOfTicks = 100

    WarningWeight = 10
    ReiterateWeight = 3
    StaticWeight = 5
    GoWeight = 2

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
    
    def __init__(self):
        pass