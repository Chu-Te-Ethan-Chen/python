from windrose import WindroseAxes
from matplotlib import  pyplot as plt
import pandas as pd


# Create ind speed and direction variables
data = pd.read_excel('HW02aout.xlsx', sheet_name='Sheet1')
ws = data['風速(m/s)'].astype(int)
wd = data['風向(360degree)'].astype(float)
wsMax = data['最大陣風(m/s)'].astype(int)
wdMax = data['最大陣風風向(360degree)'].astype(float)

ax = WindroseAxes.from_ax()
###3.1## A stacked histogram with normed (displayed in percent) results
#ax.bar(wd, ws, normed=True, opening=0.8, edgecolor='white')
ax.bar(wdMax, wsMax, normed=True, opening=0.8, edgecolor='white')
ax.set_legend()
plt.show()