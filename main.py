import requests 
from bs4 import BeautifulSoup 
from tabulate import tabulate 
import os 
import numpy as np 
import matplotlib.pyplot as plt 
extract_contents = lambda row: [x.text.replace('\n', '') for x in row] 
URL = 'https://www.mohfw.gov.in/'

SHORT_HEADERS = ['SNo', 'State','Total-Confirmed','Cured','Death'] 

response = requests.get(URL).content 
soup = BeautifulSoup(response, 'html.parser') 
header = extract_contents(soup.tr.find_all('th')) 

stats = [] 
all_rows = soup.find_all('tr') 
for row in all_rows: 
	stat = extract_contents(row.find_all('td')) 
	if stat: 
		if len(stat) == 4: 
			# last row 
			stat = ['', *stat] 
			stats.append(stat) 
		elif len(stat) == 5: 
			stats.append(stat) 

stats[-1][1] = "Total Cases"
objects = [] 
for row in stats : 
	objects.append(row[1]) 
	row[2]=row[2].strip("#")

y_pos = np.arange(len(objects)-1) 

performance = [] 
for row in stats :
	try:
		performance.append(int(row[2].strip("#")))
	except:
		performance.append(int(row[2].strip("#")))


table = tabulate(stats, headers=SHORT_HEADERS) 
print(table)
performance.pop(-1)
objects.pop(-1)

plt.barh(y_pos, performance, align='center', alpha=0.5, 
                 color=(234/256.0, 128/256.0, 252/256.0), 
                 edgecolor=(106/256.0, 27/256.0, 154/256.0)) 
  
plt.yticks(y_pos, objects) 
plt.xlim(1,max(performance))
plt.xlabel('Number of Cases') 
plt.title('Corona Virus Cases') 

def my_autopct(pct):
    return ('%.2f' % pct) if pct > 3 else ''

for i in range(len(objects)):
	if (performance[i]/sum(performance))*100 <= 3:
		objects[i] = ''

fig1, ax1 = plt.subplots()
ax1.pie(performance, labels=objects, autopct=my_autopct,
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.


plt.show() 
