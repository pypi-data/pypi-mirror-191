from cpanlp.information.information import *

class AsymmetricInformation(Information):
    def __init__(self, sender, receiver, message, hidden_information):
        super().__init__(message)
        self.sender = sender
        self.receiver = receiver
        self.hidden_information = hidden_information
    def reveal_hidden_information(self):
        print(f"{self.sender.name} reveals hidden information to {self.receiver.name}: {self.hidden_information}")
    @property
    def is_information_complete(self):
        return self.hidden_information is None
    @property
    def negotiate(self):
        if self.hidden_information is not None:
            print(f"{self.sender.name} and {self.receiver.name} are negotiating to resolve the asymmetric information problem...")
            self.hidden_information = None
            print("Asymmetric information problem resolved")
        else:
            print("No asymmetric information to resolve")
    def add_hidden_information(self, new_hidden_information):
        if self.hidden_information is None:
            self.hidden_information = new_hidden_information
        else:
            self.hidden_information += "; " + new_hidden_information
    def get_hidden_information(self):
        return self.hidden_information
    @property
    def use_information(self):
        if self.hidden_information is not None:
            print(f"{self.receiver.name} uses the information received from {self.sender.name} to make a decision")
        else:
            print("Not enough information to make a decision")
    @property
    def is_information_useful(self):
        return self.hidden_information is None
    @property
    def get_advantage(self):
        if self.hidden_information is not None:
            print(f"{self.sender.name} has an advantage over {self.receiver.name} due to asymmetric information")
        else:
            print("No advantage due to symmetric information")
