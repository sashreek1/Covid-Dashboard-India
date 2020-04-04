import requests 
from bs4 import BeautifulSoup 
from tabulate import tabulate 
import os 
import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import state_list

extract_contents = lambda row: [x.text.replace('\n', '') for x in row] 
URL = 'https://www.mohfw.gov.in/'

SHORT_HEADERS = ['SNo', 'State','Total-Confirmed','Cured','Death'] 


########################## Get data from ministry of health #####################################

response = requests.get(URL).content 
soup = BeautifulSoup(response, 'html.parser') 
header = extract_contents(soup.tr.find_all('th')) 

stats = [] 
all_rows = soup.find_all('tr') 
for row in all_rows: 
	stat = extract_contents(row.find_all('td')) 
	if stat: 
		if len(stat) == 4: 
			stat = ['', *stat] 
			stats.append(stat) 
		elif len(stat) == 5:
			stat[1] = stat[1].replace(" and "," & ")
			stat[1] = stat[1].replace("Delhi","NCT of Delhi")
			stat[1] = stat[1].replace("Telengana","Telangana")
			stat[1] = stat[1].replace("Arunachal","Arunanchal")
			stat[1] = stat[1].replace("Andaman & Nicobar Islands","Andaman & Nicobar Island")
			stat[1] = stat[1].replace("Dadra & Nagar Haveli","Dadara & Nagar Havelli")

			stats.append(stat) 
prev_sno = int(stats[-2][0])
stats[-1][1] = "Total Cases"
stats[-1][0] = str(prev_sno+1)
objects = [] 
for row in stats : 
	objects.append(row[1]) 
	row[2]=row[2].strip("#")

y_pos = np.arange(len(objects)-1) 

data = stats[0:-1]
data.insert(0,["SNo","State","Total-Confirmed","Cured","Death"])

performance = [] 
for row in stats :
	try:
		performance.append(int((row[2].strip("#")).strip("*")))
	except:
		performance.append(int((row[2].strip("#").strip("*"))))

for i in range(len(data)):
	for j in range(len(data[i])):
		if data[i][j].isdigit():
			data[i][j] = int(data[i][j])


column_names = data.pop(0)
df_1 = pd.DataFrame(data, columns=column_names)


column_names = state_list.stats_edit.pop(0)
df_2 = pd.DataFrame(state_list.stats_edit, columns=column_names)



df_data = pd.merge(left=df_2, right=df_1, how='left', left_on='State-def', right_on='State')


################################## Print Table ######################################

table = tabulate(stats, headers=SHORT_HEADERS) 
print(table)
performance.pop(-1)
objects.pop(-1)

################################### Plot bar chart ##################################

plt.barh(y_pos, performance, align='center', alpha=0.5, 
                 color=(256/256.0, 0/256.0, 0/256.0), 
                 edgecolor=(106/256.0, 27/256.0, 154/256.0)) 
  
plt.yticks(y_pos, objects, fontsize=10) 
plt.xlim(1,max(performance))
plt.xlabel('Number of Cases') 
plt.title('Corona Virus Cases') 
 
############################### Plot pie chart ####################################### 
def my_autopct(pct):
    return ('%.2f' % pct) if pct > 3 else ''

for i in range(len(objects)):
	if (performance[i]/sum(performance))*100 <= 3:
		objects[i] = ''

fig1, ax1 = plt.subplots()
ax1.pie(performance, labels=objects, autopct=my_autopct,
        shadow=True, startangle=90)
ax1.axis('equal')

######################### plot shape files ###########################################


fp = "Igismap/Indian_States.shp"
map_df = gpd.read_file(fp)
df_data = df_data.fillna(0)
merged = map_df.set_index('st_nm').join(df_data.set_index('State-def'))



# Plot the number of confirmed cases

fig, ax = plt.subplots(1, figsize=(10, 6))
ax.set_facecolor('black')
ax.axis('off')
ax.set_title('Covid-19 cases per State', fontdict={'fontsize': '25', 'fontweight' : '3'})
merged.plot(column='Total-Confirmed', cmap='YlOrRd', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)

# Plot the number of cured cases 

fig, ax = plt.subplots(1, figsize=(10, 6))
ax.axis('off')
ax.set_title('Cured COVID-19 patients per State', fontdict={'fontsize': '25', 'fontweight' : '3'})
merged.plot(column='Cured', cmap='Blues', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)

# Plot the number of Deaths

fig, ax = plt.subplots(1, figsize=(10, 6))
ax.axis('off')
ax.set_title('Covid-19 deaths per State', fontdict={'fontsize': '25', 'fontweight' : '3'})
merged.plot(column='Death', cmap='Reds', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)

plt.show() 



