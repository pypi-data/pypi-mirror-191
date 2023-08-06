class ExecutiveSeveranceAndRetentionIncentivePlan:
    def __init__(self, name, eligible_executives, severance_package, retention_bonus, amended=False,restated=False):
        self.name = name
        self.eligible_executives = eligible_executives
        self.severance_package = severance_package
        self.retention_bonus = retention_bonus
        self.amended = amended
        self.restated=restated

    def __str__(self):
        amended_info = " (Amended and Restated)" if self.amended_and_restated else ""
        return f"{self.name}{amended_info}\nEligible Executives: {self.eligible_executives}\nSeverance Package: {self.severance_package}\nRetention Bonus: {self.retention_bonus}"
