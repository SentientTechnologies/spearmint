
from spearmintlite.spearmintlite import one_generation
from spearmintlite.SimpleEvaluationStateProvider import SimpleEvaluationStateProvider
from spearmintlite.SimpleHyperParameterStateProvider import SimpleHyperParameterStateProvider
from spearmintlite.rosenbrocks_valley.rosenbrock import rosenbrocks_valley
from spearmintlite.braninhoo.braninhoo import braninhoo
import collections
import numpy as np
import json

if __name__ == '__main__':

    grid_size = 2000
    grid_seed = 1
    chooser_module = 'GPEIOptChooser'
    chooser_args = 'mcmc_iters = 10, noiseless = 1'

    hyper_parameters_provider = SimpleHyperParameterStateProvider()

    variables = json.load(open('/Users/asaliou/Documents/workspace/spearmint/spearmintlite/rosenbrocks_valley/config.json'), object_pairs_hook=collections.OrderedDict)
    #variables = json.load(
    #    open('/Users/asaliou/Documents/workspace/spearmint/spearmintlite/braninhoo/config.json'),
    #    object_pairs_hook=collections.OrderedDict)

    nb_iter = 50
    nb_examples_per_iter = 2

    values = np.array([])
    complete = np.array([])
    durations = np.array([])

    hyper_param_state_provider = SimpleHyperParameterStateProvider()

    for i in range(nb_iter):
        pending = np.array([])
        all_params = []
        for j in range(nb_examples_per_iter):
            state_provider = SimpleEvaluationStateProvider(pending, values, complete, durations)

            params = one_generation(grid_size, grid_seed, chooser_module, chooser_args, variables, state_provider, \
                           hyper_parameters_provider)

            params_arr = np.array([param for param in params])
            if pending.shape[0] > 0:
                pending = np.vstack((pending, params_arr))
            else:
                pending = np.matrix(params_arr)
            all_params.append(params_arr)

        for params_arr in all_params:
            value = rosenbrocks_valley(np.array(params_arr).copy())
            #value = braninhoo(np.array(params_arr).copy())
            if type(values) is float or values.shape[0] > 0:
                values = np.vstack((values, value))
                complete = np.vstack((complete, params_arr))
                durations = np.vstack((durations, 0.))
            else:
                values = float(value)
                complete = np.matrix(params_arr)
                durations = float(0.)
