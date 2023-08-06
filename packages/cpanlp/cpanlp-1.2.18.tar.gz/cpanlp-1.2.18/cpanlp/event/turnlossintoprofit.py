class TurnLossIntoProfit:
    def __init__(self, revenue, expenses):
        self.revenue = revenue
        self.expenses = expenses
    def is_profit(self):
        return self.revenue > self.expenses
    def calculate_profit(self):
        return self.revenue - self.expenses
    def suggest_cost_cutting_measures(self):
        if not self.is_profit():
            print("The company is currently incurring a loss. Suggestions for cost cutting measures:")
            print("1. Reduce marketing expenses")
            print("2. Optimize employee utilization")
            print("3. Cut back on discretionary spending")
            print("4. Re-negotiate supplier contracts")