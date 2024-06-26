#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 16:56:57 2022

@author: hirschbe
"""

# from SedCas import SedCas
from SedCas_glacier_sed import SedCas

def run():
	model = SedCas()
	model.load_climate()
	model.load_params()
	model.run_hydro()
	model.run_sediment()
	model.save_output()
	# model.plot_sedyield_monthly()

if '__name__' == '__main__':
	run()
