import requests
import os
import dill
import time
import pandas as pd

#Extracting and compiling information from dill files containing yelp data
dict_1 = dill.load(open('dict_latlong_batch1.pkd', 'rb'))
dict_2 = dill.load(open('dict_latlong_batch2.pkd', 'rb'))
dict_3 = dill.load(open('dict_latlong_batch3.pkd', 'rb'))

dict_all=[]
dict_all=dict_1
for j in range(0,2000):
    dict_all[2000+j]=dict_2[j]
for j in range(len(dict_3)):
    dict_all[4000+j]=dict_3[j]

#Converting to dictionary and adding h3_loc to relate to lat long information of hexagons
df_dict=pd.DataFrame()
j=0
for i in range(len(dict_all)):
    df_1=pd.DataFrame(dict_all[i])
    df_1['h3_loc']=i
    print(j)
    j+=1
    df_dict=df_dict.append(df_1,ignore_index=True)

#Dropping locations where same food place occurs multiple times, keeping closest hex to food place
df_final=df_dict.sort_values('distance').drop_duplicates('id', keep='first')
df_final=df_final.sort_values('h3_loc').reset_index()

#Extracting category names
df_final1=df_final.reset_index()
df2=df_final1['categories'].apply(pd.Series)

#Extracting categories
title1=df2[0].apply(pd.Series)['title']
title1=title1.reset_index()
title1=title1.rename(columns={'index':'level_0','title':'category1'})

#For plotting
df_final1=df_final1.merge(title1)
df_final1.to_csv('allentrieswCat1.csv')

# Getting top 100 categories
a=title1.groupby('category1').agg('count')
top100_category1=a.sort_values('level_0',ascending=False)[0:100]

df_top100_category1=pd.DataFrame()
for i in range(len(top100_category1)):
    df_top100_category1=df_top100_category1.append(df_final1[df_final1['category1']==top100_category1.index[i]])

df_top100_category1_pivoted=df_top100_category1.pivot_table(index='h3_loc', columns='category1',
                        aggfunc=len, fill_value=0).reset_index()
df_top100_category1_pivoted = df_top100_category1_pivoted['alias']
df_top100_category1_pivoted['h3_loc']=df_top100_category1['h3_loc']
df_top100_category1_pivoted=df_top100_category1_pivoted.set_index('h3_loc')

# Saving for ML model
df_top100_category1_pivoted.to_csv('ByCategory1top100_pivoted.csv')
