from cpanlp.control.power import *
class SignificantInfluence(VotingPower):
    def __init__(self, name, voting_weight):
        super().__init__(name, voting_weight)
        if not 0.2 < self.voting_weight < 0.5 :
            raise ValueError("Significant Influence requires a voting weight between 20% and 50%")
    