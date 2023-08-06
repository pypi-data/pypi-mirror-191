class Election:
    def __init__(self, election_type, date, candidates):
        self.election_type = election_type
        self.date = date
        self.candidates = candidates

    def __str__(self):
        candidate_str = ""
        for candidate in self.candidates:
            candidate_str += str(candidate) + "\n"
        return f"Election Type: {self.election_type}\nDate: {self.date}\nCandidates:\n{candidate_str}"
