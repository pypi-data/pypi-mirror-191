class Appointment:
    def __init__(self, appointee, position, date, appointing_authority):
        self.appointee = appointee
        self.position = position
        self.date = date
        self.appointing_authority = appointing_authority

    def __str__(self):
        return f"Appointee: {self.appointee}\nPosition: {self.position}\nDate: {self.date}\nAppointing Authority: {self.appointing_authority}"
