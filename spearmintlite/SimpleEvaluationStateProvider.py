

class SimpleEvaluationStateProvider(object):

    def __init__(self, pending, values, complete, durations):
        self.pending = pending
        self.values = values
        self.complete = complete
        self.durations = durations

    def get_pending(self):
        return self.pending

    def get_values(self):
        return self.values

    def get_complete(self):
        return self.complete

    def get_durations(self):
        return self.durations
