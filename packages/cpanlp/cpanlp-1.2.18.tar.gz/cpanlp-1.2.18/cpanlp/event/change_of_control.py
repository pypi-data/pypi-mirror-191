class ChangeOfControl:
    def __init__(self, company_name, current_controller, new_controller):
        self.company_name = company_name
        self.current_controller = current_controller
        self.new_controller = new_controller

    def set_company_name(self, company_name):
        self.company_name = company_name

    def set_current_controller(self, current_controller):
        self.current_controller = current_controller

    def set_new_controller(self, new_controller):
        self.new_controller = new_controller
