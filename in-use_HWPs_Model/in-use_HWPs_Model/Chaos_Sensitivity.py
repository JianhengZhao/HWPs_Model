# Sobol' sensitivity indices from chaos
# Xinyuan Wei
# 2021/7/12

from __future__ import print_function
import numpy as np
import pandas as pd
import openturns as ot
import openturns.viewer as viewer
from matplotlib import pylab as plt
ot.Log.Show(ot.Log.NONE)

# Read data.
para_file='Factor.csv'
resu_file='HWPs_Data.csv'

para_data=pd.read_csv(para_file, sep=',')
resu_data=pd.read_csv(resu_file, sep=',')

para_name=list(para_data.columns)
resu_name=list(resu_data.columns)

print(para_name)
print(resu_name)

dimension=len(para_name)

var=resu_name[1]
print(var)

# %%
# Read parameter file and model estimates.

X=ot.Sample(para_data.to_numpy())
#X=ot.Sample(np.delete(para_data.to_numpy(),len(para_data.to_numpy())-1,0))
#print(X)
 
resu_var=resu_data[var].to_numpy()
Y=ot.Sample(len(resu_var),1)

for i in range (len(resu_var)):
    Y[i]=[resu_var[i]]
#print(Y)

# %%
# create a functional chaos model
algo = ot.FunctionalChaosAlgorithm(X, Y)
algo.run()
result = algo.getResult()
print(result.getResiduals())
print(result.getRelativeErrors())

# Quick summary of sensitivity analysis
sensitivityAnalysis = ot.FunctionalChaosSobolIndices(result)
print(sensitivityAnalysis.summary())

# draw Sobol' indices
# %%
# draw Sobol' indices
first_order = [sensitivityAnalysis.getSobolIndex(i) for i in range(dimension)]
print(first_order)
np.savetxt('first_order.txt',first_order)

total_order = [sensitivityAnalysis.getSobolTotalIndex(i) for i in range(dimension)]
print(total_order)
np.savetxt('total_order.txt',total_order)

graph = ot.SobolIndicesAlgorithm.DrawSobolIndices(para_name, first_order, total_order)
view = viewer.View(graph)

# %%
# We saw that total order indices are close to first order,
# so the higher order indices must be all quite close to 0
result_arr=[]
for i in range(dimension):
    for j in range(i):
        temp=[]
        #print(input_names[i] + ' & '+ input_names[j], ":", sensitivityAnalysis.getSobolIndex([i, j]))
        temp.append(para_name[i] + ' & '+ para_name[j])
        temp.append(sensitivityAnalysis.getSobolIndex([i, j]))
        result_arr.append(temp)

np.savetxt('SobolIndex.txt',result_arr,fmt='%s')
plt.show()
