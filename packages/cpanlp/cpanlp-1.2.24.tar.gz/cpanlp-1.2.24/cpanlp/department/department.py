class Department:
    def __init__(self, name, goals=None, incentives=None):
        self.name = name
        self.goals = goals
        self.incentives = incentives
        self.legal_status = "Registered"
        self.responsibility = []
        self.powers =  []