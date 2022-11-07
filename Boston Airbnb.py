import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import date as dt

file = r'C:/Users/e085865/Desktop/Python/Udacity/1. Introduction/Blog Project/Boston Airbnb Data.csv'

original_df = pd.read_csv(file,index_col=0)

df = original_df[['name','summary','description','transit','neighbourhood_cleansed','zipcode',
         'latitude','longitude','room_type','accommodates','bathrooms',	'bedrooms','beds',
         'amenities','price','guests_included','availability_30',	
         'availability_60','availability_90','availability_365','number_of_reviews',
         'first_review','review_scores_rating','reviews_per_month']]


### Dealing with NAN ###
#print(df.isnull().mean())



#####################
### Cleaning Data ###
#####################

#Make neighbouthood cleansed categorical to pass through to scatter plot
### Potentially REMOVE ###
"""nb = df['neighbourhood_cleansed'].value_counts().index
color = {}
count= 1
for i in nb:
    color[i] = count
    count+=1
    
for i, group in df.groupby('neighbourhood_cleansed'):
    g_ind = group.index
    df.loc[g_ind,'categorical_nb'] = color[i]"""
    

#Remove symbols from Price col
def remove_sign(col):
    col = col.replace('$','')
    col = col.replace(',','')
    return float(col)

df['price'] = df['price'].apply(remove_sign)


#Fill NAN for bathrooms, bedrooms, and beds using median of each group
#Group by number of accommodations
cols = ['bathrooms','bedrooms','beds']

for col in cols:    
    for ids, group in df.groupby(['accommodates']):
        grp_ind = group[group[col].isnull()].index
        df.loc[grp_ind,col] = group[col].median()


#change review date col to date data type
df['first_review'] = pd.to_datetime(df['first_review']).dt.date
df['first_review'] = dt.today() - df['first_review']

print(df.isnull().mean())


#standardizing availability and covert to Utilization Rate
df['utilization_30'] = df['availability_30'].apply(lambda x: 1 - (x/30))
df['utilization_60'] = df['availability_60'].apply(lambda x: 1 - (x/60))
df['utilization_90'] = df['availability_90'].apply(lambda x: 1 - (x/90))
df['utilization_365'] = df['availability_365'].apply(lambda x: 1 - (x/365))

df['utilization_30'].plot(kind='hist')

#df.to_excel(r'C:/Users/e085865/Desktop/Python/Udacity/1. Introduction/Blog Project/CLEAN Boston Airbnb Data.xlsx')

##############################
### Neighbourhood Analysis ###
##############################

#how many Airbnbs are per neighborhood? Do we need to remove any that are too small of a sample?
nb_counts = df['neighbourhood_cleansed'].value_counts().sort_values()


for nb, group in df.groupby('neighbourhood_cleansed'):
    count = len(group)
    df.loc[group.index,'count'] = count
    
#Filter out based off your own sample threshold. Original df has 3565 observations
#For this analysis, I chose to only look at neighborhoods with atleast 50 listings.
df = df[df['count'] >= 50] #input the minimum sample size


#what are the top 10 neighborhoods with the highest AVG utilization rate in the year?
utl_df = df.groupby('neighbourhood_cleansed')['utilization_365'].median()
utl_df.columns = ['utilization%']

#Plot the top 10 in a Horizontal Bar chart
top_10_util = utl_df.sort_values(ascending=False).iloc[0:10]

colors = []

for util in top_10_util:
    if util/top_10_price.max() >= .85:
        colors.append('tomato')
    else:
        colors.append('salmon')

#Graph Edits
top_10_util.plot(kind='barh',legend=None,color=colors)
plt.xlabel('Median Utilization Rate')
plt.ylabel('')
plt.title('Top 10 Most Utilized Airbnbs in the Boston Area')


#what are the top 10 neighborhoods with the highest Median Price
price_df = df.groupby('neighbourhood_cleansed')['price'].median()
price_df.columns = ['median_price']

#Plot the top 10 in Horizontal Bar Chart
top_10_price = price_df.sort_values(ascending=False).iloc[0:10]


#Graph Edits
top_10_price.plot(kind='barh',legend=None,color='tomato')
plt.xlabel('Median Price per Night')
plt.ylabel('')
plt.title('Top 10 Most Expensive Airbnbs Prices per Night in the Boston Area')


#What are the top 10 neighbourhoods with the highest median projected revenue?
df['revenue_projection'] = (df['price']*365) * df['utilization_365']
rev_df = df.groupby('neighbourhood_cleansed')['revenue_projection'].median()

#Plot the top 10 in Horizontal Bar Chart
top_10_rev = rev_df.sort_values(ascending=False).iloc[0:10]


#Graph Edits
top_10_rev.plot(kind='barh',legend=None)
plt.xlabel('Median Revenue in a Year')
plt.ylabel('')
plt.title('Top 10 Boston Neighbourhoods with the Highest Project Revenues on Airbnb')


##################################
### ROI for All neighbourhoods ###
##################################

#Lets look at the ROI for the houses

#House data from RedFin
#https://www.redfin.com/
median_house_prices = {
    'Leather District':979500,
    'Fenway':1064500,
    'Roslindale':699000,
    'Dorchester':690000,
    'West Roxbury':750000,
    'Roxbury':739900,
    'Mattapan':610000,
    'Hyde Park':615000,
    'Bay Village':2878750,
    'East Boston':675000,
    'Brighton':500000,
    'Jamaica Plain':757500,
    'Mission Hill':865000,
    'Allston':539000,
    'South Boston':825000,
    'Longwood Medical Area':1200000,
    'Charlestown':952500,
    'North End':898000,
    'West End':518375,
    'Back Bay':1100000,
    'Downtown':1125000,
    'South End':1100100,
    'Beacon Hill':1200000,
    'Chinatown':1310000,
    'South Boston Waterfront':1134000
    }

#Calculate ROI based off Rev Projection to Median House
for nb,group in df.groupby('neighbourhood_cleansed'):
    try:
        price = median_house_prices[nb]    
        median_rev = group['revenue_projection'].median()
        df.loc[group.index,'yrs_roi'] = price/median_rev
    except:
        pass

roi_df = df.groupby('neighbourhood_cleansed')['yrs_roi'].mean()

#Plot the top 10 in Horizontal Bar Chart
top_10_roi = roi_df.sort_values().iloc[0:10]

top_10_roi.plot(kind='barh',legend=None)
plt.xlabel('Years for ROI')
plt.ylabel('')
plt.title('Top 10 Boston Neighbourhoods with the Shortest Time for ROI')

#############################
### Who are these guests? ###
#############################

#guest_df = df.groupby('accommodates')['utilization_365'].agg(['mean','median','count']).sort_values(by='mean',ascending=False)



###################################################
### Plotting locations on Map with Long and Lat ###
###################################################

"""BBox = (df.longitude.min(),df.longitude.max(),df.latitude.min(), df.latitude.max())

mymap = plt.imread(r'C:/Users/e085865/Desktop/Python/Udacity/1. Introduction/Blog Project/map (4).png')

fig, ax = plt.subplots(figsize = (8,7))
ax.scatter(top_df.longitude, top_df.latitude, alpha= .9,c='b',edgecolors='black',
           s=(top_df['revenue_projection']/top_df['revenue_projection'].max()*1000))

ax.set_title('Plotting Spatial Data on Boston Map')
ax.set_xlim(BBox[0],BBox[1])
ax.set_ylim(BBox[2],BBox[3])
ax.axis('off')
ax.imshow(mymap, zorder=0, extent = BBox, aspect= 'equal')

for price in top_10_price:
    print(price/top_10_price.max())
    if price/top_10_price.max() >= .85:
        colors.append('blue')
    elif price/top_10_price.max() >= .7:
        colors.append('cornflowerblue')
    else:
        colors.append('lightsteelblue')"""


##########################################
### Incase we want to use the data set ###
##########################################


