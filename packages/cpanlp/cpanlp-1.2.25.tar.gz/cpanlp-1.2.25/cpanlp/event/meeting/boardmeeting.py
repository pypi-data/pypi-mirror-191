from cpanlp.event.meeting.meeting import *

class BoardMeeting(Meeting):
    def __init__(self, company,session_number, meeting_number,resolution,date=None, location=None):
        super().__init__(company,session_number, meeting_number,resolution,date, location)