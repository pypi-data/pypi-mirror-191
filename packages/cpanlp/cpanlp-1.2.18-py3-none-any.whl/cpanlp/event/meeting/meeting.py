class Meeting:
    def __init__(self, company,session_number, meeting_number,resolution,date=None, location=None):
        self.company_name = company
        self.date = date
        self.location = location
        self.session_number = session_number
        self.meeting_number = meeting_number
        self.resolution = resolution
