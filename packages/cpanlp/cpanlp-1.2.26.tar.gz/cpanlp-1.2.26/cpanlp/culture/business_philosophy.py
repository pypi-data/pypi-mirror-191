class BusinessPhilosophy:
    def __init__(self, mission, values, long_term_goals):
        self.mission = mission
        self.values = values
        self.long_term_goals = long_term_goals

    def update_philosophy(self, new_mission, new_values, new_long_term_goals):
        self.mission = new_mission
        self.values = new_values
        self.long_term_goals = new_long_term_goals
        print("Business philosophy updated:")
        print("Mission: {}".format(self.mission))
        print("Values: {}".format(self.values))
        print("Long-term goals: {}".format(self.long_term_goals))

def main():
    philosophy = BusinessPhilosophy("To provide quality products and services",
                                ["Integrity", "Innovation", "Customer satisfaction"],
                                "To become a leader in the industry")

    philosophy.update_philosophy("To create value for our customers and society",
                             ["Transparency", "Sustainability", "Excellence"],
                             "To be the preferred choice in the market")
if __name__ == '__main__':
    main()