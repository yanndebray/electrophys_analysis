# SPADE is a method to detect repeated spatio-temporal activity patterns 
# in parallel spike train data that occur in excess to chance expectation. 
# We will use SPADE to detect the simplest type of such patterns, 
# synchronous events that are found across a subset of the neurons considered 

import numpy as np
import quantities as pq
import neo
import elephant
np.random.seed(4542)

# In a first step, let use generate 10 random spike trains, 
# each modeled after a Poisson statistics, in which a certain proportion 
# of the spikes is synchronized across the spike trains.

spiketrains = elephant.spike_train_generation.compound_poisson_process(
   rate=5*pq.Hz, amplitude_distribution=[0]+[0.98]+[0]*8+[0.02], t_stop=10*pq.s)
len(spiketrains)

# In a second step, we add 90 purely random Poisson spike trains using 
# the homogeneous_poisson_process()| function, such that in total we have 
# 10 spiketrains that exhibit occasional synchronized events, 
# and 90 uncorrelated spike trains.

for i in range(90):
    spiketrains.append(elephant.spike_train_generation.homogeneous_poisson_process(
        rate=5*pq.Hz, t_stop=10*pq.s))
    
# In the next step, we run the spade() method to extract the synchronous patterns.
patterns = elephant.spade.spade(
    spiketrains=spiketrains, binsize=1*pq.ms, winlen=1, min_spikes=3,
    n_surr=100,dither=5*pq.ms,
    psr_param=[0,0,0],
    output_format='patterns')['patterns']

# The output patterns of the method contains information on the found patterns.
patterns
