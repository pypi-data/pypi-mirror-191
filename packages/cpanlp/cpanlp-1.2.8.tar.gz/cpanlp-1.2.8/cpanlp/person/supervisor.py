from cpanlp.person.consumer import *

class Supervisor(Consumer):
    def __init__(self, name, age=None,wealth=None,utility_function=None):
        super().__init__(name, age,wealth,utility_function)
    def inspect_financials(self):
        """Inspect the company's financials"""
        pass
    def supervise_board_and_senior_management(self):
        """Supervise the actions of the board and senior management in carrying out their duties, and propose the dismissal of directors and senior management who violate laws, regulations, the company's articles of association or resolutions of the shareholders' meeting."""
        pass
    def request_corrective_action(self):
        """When the actions of the board and senior management harm the interests of the company, require them to take corrective action"""
        pass
    def propose_extraordinary_shareholders_meeting(self):
        """Propose a special shareholders' meeting, and convene and preside over the meeting when the board fails to fulfill its duty to convene and preside over shareholders' meetings"""
        pass
    def propose_resolutions(self):
        """Propose resolutions to shareholders' meeting"""
        pass
    def sue_board_and_senior_management(self):
        """Sue the board and senior management according to the provisions of Article 151 of this Law"""
        pass
    def other_responsibilities(self):
        """Other responsibilities as specified in the company's bylaws"""
        pass