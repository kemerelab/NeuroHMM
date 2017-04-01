# NeuroHMM—Analysis of neural data using hidden Markov models.
This repository contains some selected example notebooks and discussions for the analysis of neural data using hidden Markov models on publically accessible data from [crcns.org](https://crcns.org/data-sets/hc/hc-3/about-hc-3).

# Current and future developments: [nelpy](https://github.com/eackermann/nelpy)
All the results shown in these notebooks can be (re-)generated using the accompanying code in this repository, along with publically accessible data from the hc-3 dataset on [crcns.org](crcns.org). However, active development has shifted away from this repository, and we are currently actively developing [nelpy](https://github.com/eackermann/nelpy) to make it easier to do common (yet complex) analysis tasks with neuroelectrophysiology data.

# Overview

## How to use this repository

The easiest way to use this repository is to take a look at the various Jupyter notebooks. These are all the files ending with the `.ipynb` extensions. These files can be rendered directly in github, so you can look at the code, analysis, and results, all in your browser, without the need to install any additional software, or to execute any code.

The notebooks of particular interest, and in a loosley logical order, are briefly described below.
 * [**StateClustering**.ipynb](../master/StateClustering.ipynb)—demonstration that HMMs can (robustly) learn place fields in the absence of positional data; several follow-up analyses showing how behavioral states, different contexts, etc. are captured and clustered in the inferred model states (status: in progress, first half complete)
 * [**StateOrdering**.ipynb](../master/StateOrdering.ipynb)—post-ordering hidden states for interpretation and evaulation (status: complete)
 * [**ModelSelection**.ipynb](../master/ModelSelection.ipynb)—sensitivity analysis and discussion on selecting appropriate model parameters (status: complete)
 * [**KLscore**.ipynb](../bmaster/KLscore.ipynb)—preliminary results and proof-of-concept for a Kullback-Leibler based sequence score (status: almost complete)
 * [**BootstrappingHMMs**.ipynb](../master/BootstrappingHMMs.ipynb)—using synthesized data to augment our training set (status: not yet started)
 * [**OnlineScoring**.ipynb](../master/OnlineScoring.ipynb)—using HMMs for the analysis of continuous chronic recordings (status: incomplete)
 
Of course, you can also clone or download this repository, which will allow you to modify the code to see the effect of changing parameters, and so on. For this, you would need Python 3, and several additional packages. Following any god Python tutorial should help you get up and running pretty fast.

## Where to get the data

The data used here is publically available free-of-charge at [http://crcns.org](http://crcns.org), the data sharing website funded by the Collaborative Research in Computational Neuroscience (CRCNS) program. More specifically we have used dataset `hc-3` here, and from that dataset, this repository shows results for animal `gor01`.
