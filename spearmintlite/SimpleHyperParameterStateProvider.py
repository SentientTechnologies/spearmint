


#This is a simple cache not thread safe for initial experimentations
#Cache is used to keep spearmint bpo statistics

class SimpleHyperParameterStateProvider(object):

    def __init__(self, state=None):
        if state is not None:
            self.state = state.copy()
        else:
            self.state = None

    def get_state(self):
        if self.state is not None:
            return self.state.copy()
        else:
            return None

    def set_state(self, state):
        self.state = state.copy()
