from cpanlp.person.consumer import *
class Employee(Consumer):
    def __init__(self, name, age=None,wealth=None,utility_function=None, salary=None, department=None):
        super().__init__(name, age,wealth,utility_function)
        self.emp_id = None
        self.salary = salary
        self.department = department
        self.job_title = None
        self.experience = None
        self.education = None
def main():
    employee1 = Employee("zhang",19,221333,0,2000,"accounting")
    employee2 = Employee("zhang12",29,222233,0,2000,"accounting")
