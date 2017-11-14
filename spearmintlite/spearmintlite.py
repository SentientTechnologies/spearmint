##
# Copyright (C) 2012 Jasper Snoek, Hugo Larochelle and Ryan P. Adams
#
# This code is written for research and educational purposes only to
# supplement the paper entitled "Practical Bayesian Optimization of
# Machine Learning Algorithms" by Snoek, Larochelle and Adams Advances
# in Neural Information Processing Systems, 2012
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see
# <http://www.gnu.org/licenses/>.

import importlib

from ExperimentGrid  import *
try: import simplejson as json
except ImportError: import json
import optparse

#
# There are two things going on here.  There are "experiments", which are
# large-scale things that live in a directory and in this case correspond
# to the task of minimizing a complicated function.  These experiments
# contain "jobs" which are individual function evaluations.  The set of
# all possible jobs, regardless of whether they have been run or not, is
# the "grid".  This grid is managed by an instance of the class
# ExperimentGrid.
#
# The spearmint.py script can run in two modes, which reflect experiments
# vs jobs.  When run with the --wrapper argument, it will try to run a
# single job.  This is not meant to be run by hand, but is intended to be
# run by a job queueing system.  Without this argument, it runs in its main
# controller mode, which determines the jobs that should be executed and
# submits them to the queueing system.
#


##############################################################################
##############################################################################
def one_generation(grid_size, grid_seed, chooser, variables, evaluation_state, \
    hyper_parameters_provider):

    pending = evaluation_state.get_pending()
    values = evaluation_state.get_values()
    complete = evaluation_state.get_complete()
    durations = evaluation_state.get_durations()


    # Load up the chooser module.
    #module  = importlib.import_module('spearmint.spearmint.chooser.' + chooser_module, package='spearmint')
    #chooser = module.init(chooser_args)

    vkeys = [k for k in variables]
    gmap = GridMap([variables[k] for k in vkeys], grid_size)


    #Map the parameters in the hypersphere
    if complete.shape[0] > 0:
        complete = np.array([gmap.to_unit(np.squeeze(np.asarray(x)).tolist()) for x in complete])
    if pending.shape[0] > 0:
        pending = np.array([gmap.to_unit(np.squeeze(np.asarray(x)).tolist()) for x in pending])

    # Read in parameters and values observed so far

    # Let's print out the best value so far
    if type(values) is not float and len(values) > 0:
        best_val = np.min(values)
        best_val_index = np.argmin(values)
        best_job = np.argmin(values)
        sys.stderr.write("Current best: %f at %s (job %d)\n" % (best_val, str(complete[best_val_index]), best_job))

    # Now lets get the next job to run
    # First throw out a set of candidates on the unit hypercube
    # Increment by the number of observed so we don't take the
    # same values twice
    off = pending.shape[0] + complete.shape[0]
    candidates = gmap.hypercube_grid(grid_size,
                                     grid_seed+off)

    # Ask the chooser to actually pick one.
    # First mash the data into a format that matches that of the other
    # spearmint drivers to pass to the chooser modules.
    grid = candidates
    if (complete.shape[0] > 0):
        grid = np.vstack((complete, candidates))
    if (pending.shape[0] > 0):
        grid = np.vstack((grid, pending))
    grid = np.asarray(grid)
    grid_idx = np.hstack((np.zeros(complete.shape[0]),
                          np.ones(candidates.shape[0]),
                          1.+np.ones(pending.shape[0])))


    job_id = chooser.next(grid, np.squeeze(values), durations,
                          np.nonzero(grid_idx == 1)[0],
                          np.nonzero(grid_idx == 2)[0],
                          np.nonzero(grid_idx == 0)[0], hyper_parameters_provider)

    # If the job_id is a tuple, then the chooser picked a new job not from
    # the candidate list
    if isinstance(job_id, tuple):
        (job_id, candidate) = job_id
    else:
        candidate = grid[job_id,:]

    params = gmap.unit_to_list(candidate)

    return params

