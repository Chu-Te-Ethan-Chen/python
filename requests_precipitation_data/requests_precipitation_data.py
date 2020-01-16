import requests
import urllib3
from bs4 import BeautifulSoup as bs
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import animation
from matplotlib import rcParams

sess = requests.Session()
url = '(website)'
data = {
    'id': '(account)',
    'pass': '(password)',
    'ver': 'C' }
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging = sess.post(url, params=data, verify=False)
urlc='(website)'
html= sess.get(urlc)
html.encoding='big5'
bhtml=bs(html.text, "lxml")
table=bhtml.find('table', attrs={'id': 'MyTable'})
HeadList=[th.get_text() for th in table.find('tr', attrs={'class':'second_tr'}).find_all("th")]
datasets=[]
for row in table.find_all('tr')[3:]:
    dataset=[td.get_text().strip() for td in row.find_all('td')]
    datasets.append(dataset)
df=pd.DataFrame(datasets, columns=HeadList)
df.to_excel('HW02aout.xlsx')
data = pd.read_excel('HW02aout.xlsx', sheet_name='Sheet1')
fig, ax = plt.subplots()
x = data['觀測時間(hour)'].astype(int)
y = data['降水量(mm) '].astype(float)
nFrame = len(x)
fbar, =ax.plot([], [], animated=True)
xdata=[]
ydata=[]

def init():
    ax.set_xlim(0, len(x))
    ax.set_ylim(0, y.max())
    ax.set_xlabel('Time(hour)')
    ax.set_ylabel('Precipitation(mm)')
    xdata.append(x[0])
    ydata.append(y[0])
    return fbar,

def animate(i):
    xdata.append(x[i+1])
    ydata.append(y[i+1])
    fbar.set_data(xdata, ydata)
    if(i==len(x)-2):
        xdata.clear()
        ydata.clear()
    return fbar,
ani = animation.FuncAnimation(fig, animate, len(x)-1, init_func=init, blit=True)
#should install imagemagick and ffmpeg first
ani.save('Ani_precipitation.gif', writer='imagemagick', fps=150)
plt.show()
