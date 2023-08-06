class Business:
    def __init__(self, name, industry):
        self.name = name
        self.industry = industry

    def description(self):
        return f"{self.name} is a business in the {self.industry} industry."
