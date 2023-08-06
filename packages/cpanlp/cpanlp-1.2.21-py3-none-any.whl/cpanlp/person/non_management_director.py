from cpanlp.person.directors_supervisors_and_senior_executives.supervisor import *
from cpanlp.person.directors_supervisors_and_senior_executives.director import *

#Non-management directors are members of a company's board of directors who are not part of the company's management team. They are typically elected by the shareholders and are responsible for overseeing the company's management, ensuring that the company is run in the best interest of its shareholders, and making important decisions about the company's strategy and future direction.

#Non-management directors are often considered to be independent and provide a crucial check on the actions of the management team. They are not involved in the day-to-day operations of the company and can bring a fresh perspective and outside expertise to the board. Their role is to provide oversight and offer a balanced view, and they are typically not beholden to the management team or any particular interest group.  
class NonManagementDirector(Supervisor,Director):
    def __init__(self, name, expertise=None, term_length=None, company=None,shares=None,expected_return=None, risk_preference=None, portfolio=None,age=None, wealth=None,utility_function=None):
        Supervisor.__init__(self, name, age,wealth,utility_function)
        Director.__init__(self, name,shares,expected_return, risk_preference, portfolio,age, wealth,utility_function)
        self.expertise = expertise
        self.term_length = term_length
        self.company = company

    def oversee(self):
        print(f"{self.name}, a non-management director with expertise in {self.expertise}, is overseeing the management of {self.company} for a term of {self.term_length} years.")