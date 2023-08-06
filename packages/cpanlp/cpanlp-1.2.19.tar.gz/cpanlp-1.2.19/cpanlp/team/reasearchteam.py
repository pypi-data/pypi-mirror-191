from cpanlp.team.team import *
class ResearchTeam(Team):
    def __init__(self, name,area_of_research, members=None,leader=None):
        Team.__init__(self, name, members,leader)
        self.area_of_research = area_of_research