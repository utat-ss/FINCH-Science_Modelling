import pandas as pd
import numpy as np
import pytools4dart as ptd
import time
tic = time.time()
size = 1000
prospect_properties = pd.DataFrame({'N': np.random.uniform(1.72,2.10,size),
                                    'Cab': np.random.uniform(1.360,1.361,size),
                                    'Car': np.random.uniform(5.150,5.151,size),
                                    'Cm': np.random.uniform(0.0031,0.0035,size),
                                    'Cw': np.random.uniform(0.0021,0.0080,size)})
db_file = ptd.getdartenv()['DART_LOCAL'] / 'database' / 'vop2.db'
prospect_properties = ptd.dbtools.prospect_db(db_file, **prospect_properties)
toc = time.time()
print(toc - tic)