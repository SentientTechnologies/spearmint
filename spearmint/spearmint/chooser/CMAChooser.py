from cma import CMAEvolutionStrategy
from spearmint import util
import Locker

def init(expt_dir, arg_string):
    args = util.unpack_args(arg_string)
    return CMAChooser(expt_dir, **args)

"""
Chooser module for the CMA-ES evolutionary optimizer.
"""
class CMAChooser:

    def __init__(self):

        raise NotImplementedError('The CMA chooser is not yet implemented!')

        self.optimizer = CMAEvolutionStrategy(params)

    def _real_init(self, dims, values):

        raise NotImplementedError('The CMA chooser is not yet implemented!')


    def next(self, grid, values, durations, candidates, pending, complete):

        raise NotImplementedError('The CMA chooser is not yet implemented!')

        # Perform the real initialization.
        if self.D == -1:
            self._real_init(grid.shape[1], values[complete])

        # Grab out the relevant sets.
        comp = grid[complete,:]
        cand = grid[candidates,:]
        pend = grid[pending,:]
        vals = values[complete]

        # TODO: tell the optimizer about any new f-values, get the next proposed
        # sample, or maybe generate a population of samples and iterate through
        # them?

#    ...         X = es.ask()    # get list of new solutions
#    ...         fit = [cma.fcts.rastrigin(x) for x in X]  # evaluate each solution
#    ...         es.tell(X, fit) # besides for termination only the ranking in fit is used
