import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
from scipy import interpolate
#####loading data from excel#####
graph = pd.read_excel('HW01a.xlsx', sheet_name='Graph')
series = pd.read_excel('HW01a.xlsx', sheet_name='Series')
data = pd.read_excel('HW01a.xlsx', sheet_name='Data')
#####set the graph#####
set = graph['Value']
params={'font.family':set[3],
        'font.weight':set[4],
        'font.size':set[2],
        }
rcParams.update(params)
#####process the data#####
titleList=series.columns.values.tolist()
numberOfLine=len(titleList)-1
fig, ax = plt.subplots()

for i in range(numberOfLine):
        seriesNow=series.iloc[:,i+1]
        sdata = data.sort_values(by=seriesNow[0])
        x = sdata[seriesNow[0]]
        y = sdata[seriesNow[1]]
        sample=sdata['Sample']
        X = np.linspace(x.min(), x.max(), 201)
        model = interpolate.InterpolatedUnivariateSpline(x, y)
        Y = model(X)
        #####darw the graph#####
        ax.set_xlabel('Pb')
        ax.set_ylabel('concentration')
        ax.plot(X, Y, marker=seriesNow[2], markerfacecolor=seriesNow[3], markersize=0.1,
                linestyle=seriesNow[5], color=seriesNow[6], linewidth=seriesNow[7], label=seriesNow[1])
        ax.scatter(x, y, marker=seriesNow[2], c=seriesNow[3], s=seriesNow[4])
        if set[8]==1 :#tag_name
                for s, x, y in zip(sample, x, y):
                        ax.annotate("(%s,%d,%d)" % (s, x, y), xy=(x, y), xytext=(-2, 5), textcoords='offset points',
                        fontsize=10, color=seriesNow[3])
ax.legend(loc='upper right', shadow=True, fontsize='xx-small')
plt.show()