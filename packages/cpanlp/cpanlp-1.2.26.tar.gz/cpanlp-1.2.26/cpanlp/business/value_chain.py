from cpanlp.business.activity import *
from typing import List
class ValueChain:
    def __init__(self, activities: List[Activity]):
        self.activities = activities

    def add_activity(self, activity: Activity):
        self.activities.append(activity)

    def remove_activity(self, activity: Activity):
        self.activities.remove(activity)

    def get_activities(self):
        return self.activities

    def get_value(self):
        value = 0
        for activity in self.activities:
            value += activity.get_value_added()
        return value
