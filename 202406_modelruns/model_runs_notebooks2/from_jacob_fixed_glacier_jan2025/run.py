#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 16:56:57 2022

@author: hirschbe
"""

# from SedCas import SedCas
from SedCas_glacier_sed import SedCas


model = SedCas()
model.load_climate()
model.Rsw = model.Rsw / 8
model.load_params()
model.run_hydro()
model.run_sediment()

#%% 

import matplotlib.pyplot as plt

def plot_water_balance(Pr, Q, AET, PET, title):
    
    plt.figure()
    
    prm = Pr.resample('m').sum()
    prm_mean = prm.groupby(by=prm.index.month).mean()
    pry_mean = prm_mean.sum()
    
    Qm = Q.resample('m').sum()
    Qm_mean = Qm.groupby(by=Qm.index.month).mean()
    Qy_mean = Qm_mean.sum()
    
    AETm = AET.resample('m').sum()
    AETm_mean = AETm.groupby(by=AETm.index.month).mean()
    AETy_mean = AETm_mean.sum()

    PETm = PET.resample('m').sum()
    PETm_mean = PETm.groupby(by=PETm.index.month).mean()
    PETy_mean = PETm_mean.sum()
    
    plt.plot(prm_mean, label='precip (%i mm/y)'%pry_mean)
    plt.plot(Qm_mean, label='Q (%i mm/y)'%Qy_mean)
    plt.plot(AETm_mean, label='AET (%i mm/y)'%AETy_mean)
    plt.plot(PETm_mean, label='PET (%i mm/y)'%PETy_mean)
    
    plt.legend()
    plt.title(title)
    
for i,hru in enumerate(model.HRUs):
    Pr = model.HRU_hydro[i].Pr
    Q = model.HRU_hydro[i].Q
    AET = model.HRU_hydro[i].AET
    PET = model.HRU_hydro[i].PET

    plot_water_balance(Pr, Q, AET, PET, hru)

# catchment scale
Pr = model.hydro.Pr
Q = model.hydro.Q
AET = model.hydro.AET
PET = model.hydro.PET
plot_water_balance(Pr, Q, AET, PET, 'catchment')

GMm = model.hydro.glacier_melt.resample('m').sum()
GMm_mean = GMm.groupby(by=GMm.index.month).mean()
GMy_mean = GMm_mean.sum()
plt.plot(GMm_mean, label='GM (%i mm/y)'%GMy_mean)
plt.legend()
    
#%% plot glacier hru time series

plt.figure()
plt.plot(model.HRU_hydro[2].Pr, label='Pr')
plt.plot(model.HRU_hydro[2].Q, label='Q')
plt.plot(model.HRU_hydro[2].snow, label='snow')
plt.plot(model.HRU_hydro[2].glacier_melt, label='GM')
plt.legend()