from selenium import webdriver
import time
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import animation
chormepath=r'D:\Wpy\WPy-3710\python-3.7.1.amd64\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe'
url='(website)'
course='Data Analysis'
driver=webdriver.Chrome(chormepath)
driver.get(url)
time.sleep(3)
inputID=driver.find_element_by_name('id')
inputID.clear()
inputID.send_keys('account')
inputpass=driver.find_element_by_name('pass')
inputpass.clear()
inputpass.send_keys('password')
driver.find_element_by_name('btn1').click()
driver.switch_to.frame(0)
driver.find_element_by_link_text(course).click()
driver.switch_to.frame(2)
driver.find_element_by_link_text('授課教材').click()
time.sleep(3)
driver.find_element_by_partial_link_text('教材預覽').click()
time.sleep(3)
driver.switch_to.default_content()
driver.switch_to.frame('target')
driver.switch_to.frame('html')
trlist=driver.find_elements_by_tag_name('tr')
headlist=[th.text for th in trlist[1].find_elements_by_tag_name('th')]
datasets=[]
for row in trlist[3:]:
    dataset=[td.text for td in row.find_elements_by_tag_name('td')]
    datasets.append(dataset)
df=pd.DataFrame(datasets, columns=headlist)
df.to_excel('HW02bout.xlsx')
data = pd.read_excel('HW02bout.xlsx', sheet_name='Sheet1')
fig, ax = plt.subplots()
x = data['觀測時間(hour)'].astype(int)
y = data['降水量(mm)'].astype(float)
nFrame = len(x)
fbar, =ax.plot([], [], animated=True)
xdata=[]
ydata=[]

def init():
    ax.set_xlim(0, len(x))
    ax.set_ylim(0, y.max())
    xdata.append(x[0])
    ydata.append(y[0])
    return fbar,

def animate(i):
    xdata.append(x[i])
    ydata.append(y[i])
    fbar.set_data(xdata, ydata)
    if(i==len(x)-2):
        xdata.clear()
        ydata.clear()
    return fbar,
ani = animation.FuncAnimation(fig, animate, len(x)-1, init_func=init, blit=True)
#should install imagemagick and ffmpeg first
ani.save('Ani_precipitation.gif', writer='imagemagick', fps=150)
plt.show()