#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests

page = requests.get("https://www.cricbuzz.com/cricket-series/3130/indian-premier-league-2020/points-table")
soup = BeautifulSoup(page.text)
tbl = soup.find("table",class_='table cb-srs-pnts')

col_names = [x.get_text() for x in tbl.find_all('td',class_="cb-srs-pnts-th")]
col_names[5]='pts'
team_names = [x.get_text() for x in tbl.find_all('td',class_="cb-srs-pnts-name")]
pnt_tbl = [x.get_text() for x in tbl.find_all('td',class_="cb-srs-pnts-td")]

np_pnt_tbl = (np.array(pnt_tbl)).reshape(len(team_names),7) #reshaping array into shape (7,7)
np_pnt_tbl = np.delete(np_pnt_tbl,6,1)
np_pnt_tbl = np_pnt_tbl.astype(int)
consol_tbl = pd.DataFrame(np_pnt_tbl,index=team_names,columns=col_names)
consol_tbl.columns.name = "Teams"
print(consol_tbl)

team_abr = []

for team in team_names:
    short_form = ''
    for initial in team.split(' '):
       short_form = short_form + initial[0]
    team_abr.append(short_form)


title = 'IPL Points table Bar graph of 2021'
val_ticks = [1,2,3,4,5,6,7,8]
lost_ticks=[1.4,2.4,3.4,4.4,5.4,6.4,7.4,8.4]

plt.bar(val_ticks,np_pnt_tbl[:,1],width=0.4,color='y',alpha=0.8,label='Won')
plt.bar(lost_ticks,np_pnt_tbl[:,2],width=0.4,color='b',alpha=0.8,label='Lost')
plt.yticks(val_ticks)
plt.ylabel("Number of matches")
plt.xticks(val_ticks,team_names,rotation='vertical')
plt.grid(False)
plt.legend()
plt.title(title)
plt.show()

