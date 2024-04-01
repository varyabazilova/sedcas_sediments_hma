# this file should be saved one level higher than the climate directories

import os
from run import run

ls_ = os.listdir('./timeseries')
ls = [d for d in ls_ if not d.startswith('.')]
dir0 = os.getcwd()

for d in ls:
    path = os.path.join(dir0, 'timeseries', d)
    os.chdir(path)
    run()
    os.chdir(dir0)
