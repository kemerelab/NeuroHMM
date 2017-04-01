# NeuroHMM—Analysis of neural data using hidden Markov models.
Example notebooks and discussions for the analysis of neural data using hidden Markov models on publically accessible data from crcns.org.

Of particular interest are the following:
 * [**StateClustering**.ipynb](../master/StateClustering.ipynb)—validation that HMMs can learn (robustly) place fields in the absence of positional data; several follow-up analyses showing how behavioral states, different contexts, etc. are captured and clustered in the inferred model states (in progress, first half complete)
 * [**StateOrdering**.ipynb](../master/StateOrdering.ipynb)—post-ordering hidden states for interpretation and evaulation (complete)
 * [**ModelSelection**.ipynb](../master/ModelSelection.ipynb)—sensitivity analysis and discussion on selecting appropriate model parameters (complete)
 * [**KLscore**.ipynb](../bmaster/KLscore.ipynb)—preliminary results and proof-of-concept for a Kullback-Leibler based sequence score (almost complete)
 * [**BootstrappingHMMs**.ipynb](../master/BootstrappingHMMs.ipynb)—using synthesized data to augment our training set (incomplete)
 * [**OnlineScoring**.ipynb](../master/OnlineScoring.ipynb)—using HMMs for the analysis of continuous chronic recordings (incomplete)
 

