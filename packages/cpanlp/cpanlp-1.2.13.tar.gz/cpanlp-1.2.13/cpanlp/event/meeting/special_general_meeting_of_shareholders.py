from cpanlp.event.meeting.meeting import *

class SpecialGeneralMeetingOfShareholders(Meeting):
    def __init__(self, company,session_number, meeting_number,resolution,date=None, location=None):
        super().__init__(company,session_number, meeting_number,resolution,date, location)
  
    def change_company_strategy(self):
        # Change the company strategy
        print("Company strategy changed.")
        
    def acquire_company(self):
        # Acquire another company
        print("Company acquired.")
        
    def issue_new_shares(self):
        # Issue new shares
        print("New shares issued.")
        
    def remove_directors(self):
        # Remove directors
        print("Directors removed.")