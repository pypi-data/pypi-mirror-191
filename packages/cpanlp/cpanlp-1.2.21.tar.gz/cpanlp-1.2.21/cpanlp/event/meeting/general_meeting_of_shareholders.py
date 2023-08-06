from cpanlp.event.meeting.meeting import *
#A resolution is a formal decision made by a meeting, typically at a General Meeting of Shareholders. It is a written statement that outlines the actions or decisions that the meeting participants agree to take. A resolution is typically passed by a vote of the attendees and, once approved, it has the force of law within the organization.
class GeneralMeetingOfShareholders(Meeting):
    def __init__(self, company,session_number, meeting_number,resolution,date=None, location=None):
        super().__init__(company,session_number, meeting_number,resolution,date, location)

    def approve_financial_reports(self):
        # Approve the annual financial reports
        print("Financial reports approved.")
        
    def appoint_directors(self):
        # Appoint directors
        print("Directors appointed.")
        
    def distribute_dividends(self):
        # Distribute dividends
        print("Dividends distributed.")
        
    def conduct_routine_business(self):
        self.approve_financial_reports()
        self.appoint_directors()
        self.distribute_dividends()