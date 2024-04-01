    def run_sediment(self):
        
        # initialization of variables for stochastic sediment supply

        n = len(self.Pr)                                                   # length of time series
        n_days = len(self.Pr.resample('24h').sum())                        # number of days 

        class sed:
            pass
        sed.index = self.Pr.index                                      # index for date
        sed.ls = np.zeros([n, self.M])                                 # sediment input from landslides
        sed.sc = np.zeros([n, self.M])                                 # sediment channel storage [mm], shape(time series length, number of simulations)
        sed.sh = np.zeros([n, self.M])                                 # sediment hillslope storage [mm]
        sed.so = np.zeros([n, self.M])                                 # sediment catchment output [mm]
        sed.sopot = np.zeros([n, self.M])                              # potential sediment catchment output [mm], i.e. transport-limited case
        sed.dfs = np.zeros([n, self.M])                                # debris flows, from 'so' values above threshold and summed consecutive values
        sed.dfspot = np.zeros(n)                                       # debris flows potential (only 1 because only 1 climate)
        
        # sediment module with stochastic landslide magnitudes
        print('running sediment module...', sep='\n', end='\n')
        seed = 0
        for m in tqdm(range(self.M)):  
            lrgls = mod.large_ls(self.Ta, self.Pr, self.hydro.snow, self.Tsd, self.Tpr, self.Tsa, self.ls_xmin, self.ls_alpha, self.ls_cutoff, self.Tfreeze, self.LStrig, self.area, seed=seed)                # large landslided
            N = len(lrgls[lrgls.mag > 0])
            sls = mod.small_ls(n_days, N, self.ls_xmin, self.area, seed=seed)                         # small landslides
            sls.index = lrgls.index                                     # date index for small landslides


            sed_run = mod.sedcas(lrgls, sls, self.hydro, self.qdf, self.smax, self.rhc, self.shcap, self.area, 'exp', self.LStrig, self.Tpr, shinit=self.shcap, mindf=self.mindf, smax_nodf=self.smax_nodf, b=self.b)
            sed.ls[:,m] = sed_run.ls.values
            sed.sc[:,m] = sed_run.sc
            sed.sh[:,m] = sed_run.sh
            sed.so[:,m] = sed_run.so
            sed.sopot[:,m] = sed_run.sopot
            sed.dfs[:,m] = sed_run.dfs
            seed += 1
        sed.dfspot[:] = sed_run.dfspot
            
        self.sed = sed