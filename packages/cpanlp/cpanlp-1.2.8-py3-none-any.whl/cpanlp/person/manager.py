from cpanlp.person.consumer import *











class Manager(Consumer):
    def __init__(self, name, age=None,wealth=None,utility_function=None,title=None, department=None):
        super().__init__(name, age,wealth,utility_function)
        self.title = title
        self.department = department
        self.powers = []
    def manage_production_and_operations(self):
        """Manage the company's production and operations"""
        pass
    def implement_board_resolutions(self):
        """Organize and implement the board's resolutions"""
        pass
    def implement_annual_business_plan(self):
        """Organize and implement the company's annual business plan and investment strategy"""
        pass
    def formulate_internal_management_structure(self):
        """Formulate the company's internal management structure"""
        pass
    def formulate_basic_management_system(self):
        """Formulate the company's basic management system"""
        pass
    def formulate_specific_regulations(self):
        """Formulate the company's specific regulations"""
        pass
    def propose_hiring_or_dismissal(self):
        """Propose the hiring or dismissal of the company's vice manager and financial officer"""
        pass
    def hire_or_dismiss_staff(self):
        """Decide on the hiring or dismissal of management personnel, except those that should be decided by the board"""
        pass
    def set_strategy(self, strategy):
        self.strategy = strategy
        print(f'{self.name}, {self.title} of {self.department} has set a new strategy: {strategy}')
    def make_decision(self, decision):
        print(f'{self.name}, {self.title} of {self.department} has made a decision: {decision}')
    def delegate_task(self, task, employee):
        print(f'{self.name}, {self.title} of {self.department} has delegated task: {task} to employee {employee}')
    def responsible_for_board(self):
        print("I am responsible for the board.")  