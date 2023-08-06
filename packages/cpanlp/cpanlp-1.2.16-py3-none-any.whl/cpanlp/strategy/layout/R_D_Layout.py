from cpanlp.strategy.layout.layout import *

class R_DLayout(Layout):
    def __init__(self, market_position, resource_allocation, competitive_environment, research_focus):
        super().__init__(market_position, resource_allocation, competitive_environment)
        self.research_focus = research_focus

    def set_research_focus(self, research_focus):
        self.research_focus = research_focus
