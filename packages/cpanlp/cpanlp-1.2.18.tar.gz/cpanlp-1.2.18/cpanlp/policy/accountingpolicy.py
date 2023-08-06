from cpanlp.policy.policy import *


class AccountingPolicy(Policy):
    def __init__(self, name,policy_type, purpose):
        super().__init__(name, policy_type, purpose)
