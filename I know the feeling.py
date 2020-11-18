# -*- coding: utf-8 -*-
"""
Created on Wed May 20 12:17:36 2020

@author: ralls
"""
'''
Challenge:
   Work on the next function (step 2)



1. Initialize K random centroids
2. Identify the closest Centroid for each data point
3. Move each centroid to the center of the points
    a. Repeat from step 2 until centroids no longer move
'''
from scipy.spatial import distance
from random import randrange
import pandas as pd
from collections import defaultdict 


# load emoji
Emoji_file = pd.read_csv('Emoji.txt', sep=" ")
# load emoji_lookup
Emoji_lookup = pd.read_csv('emoji_lookup.tsv', sep="\t", header=None)
emojis = Emoji_lookup.to_dict('records')

emoji_look = {}
for row in Emoji_lookup.iterrows():
    emoji_look[row[1][0]] = row[1][1]


def cal_average(num):
    avgs = {}
    new_cents = {}
    p = 0
    for c in num:
        d = num[c]
        v = len(d.columns)
        for l in range(v):
            sum_num = 0
            x = d.iloc[:, l]
            num_list = x.tolist()
            for t in num_list:
                sum_num = sum_num + t
                p +=1
            avg = sum_num / p
            p = 0
            avgs[l] = avg
            new_cent = pd.Series(avgs)
            new_cents[c] = new_cent
    return new_cents


# Create a function for determining where the centriods will be
# The input the number of centroids and list of locations (The emoji file)
# The function will assign X random points for the centriods
# The output would be the centroid location (probably using a dict)
# Num = user_response, data = Emoji_file
def cent_loc(num, data):
    # Figure out how many lines of data you have
    data_num = len(data)
    centroids = {}
    org_centroids = {}
    for i in range(num):
        # Create a random number for each centroid
        cent_num = randrange(data_num)
        # Create the centroid there
        centroid = data.iloc[cent_num, 1:]
        # Store centroid in dictionary
        centroids[str(i)] = centroid
        org_centroids[str(i)] = centroid
    return centroids, org_centroids



# Create a function that will determine the centriod it is closest to for each emoji
# Input the emoji's and the centroids 
# The function will asign a centroid for each emoji
# The output will be the centroid for each emoji (probably using a dict)
# Data = Emoji_file, cent = Centroids
def emoji_cent(data, cent):
    # Call each datapoint to find the distance between all the centroids
    least_emoji_dist = {}
    for i in range(len(data)):
        emoji_dist = {}
        for cent_key in cent:
            centroid = cent[cent_key]
            emoji = data.iloc[i]
            # Find the distance
            cent_dist = distance.euclidean(centroid, emoji[1:])
            emoji_dist[cent_key] = cent_dist
    # Find the least one
            closest_cent = min(emoji_dist, key=emoji_dist.get) 
    # Store the least one in a dict
        least_emoji_dist[emoji[0]] = closest_cent
        res = defaultdict(list)
    for key, val in sorted(least_emoji_dist.items()): 
        res[val].append(key)
    return least_emoji_dist, res
    # Figure out the distance between the emoji and each centroid
# It will look through all 300 coordinates for each emoji (856)



# Create a function for moving the centriods after all the emojis are located
# Input the centroids and the emoji centroids
# The function will create seperate dictionaries for each of the centroids and thier emoji's
# The output will be the new centroid locations using a NEW dictionary
# Emoji_cents = emoji_centroids, data = Emoji_file, num = user_response
def new_cent_loc(emoji_cents, data, num):
    # Call all the emojis and assign them into seperate dictionaries
    coord = {}
    res = defaultdict(list) 
    for key, val in sorted(emoji_cents.items()): 
        res[val].append(key)
    # Find the vectors for all the emojis per dictionaries
    for key in res:
        val = res[key]
        dims = data.loc[data['emojiCode'].isin(val)]
        dims = dims.drop('emojiCode', axis=1)
        coord[key] = dims
    # Find the average
    new_cents = cal_average(coord)
    # Store the new centroids in a new dict
    return new_cents
# This function will move the centriod to the center of the points until they are the center for good

def new_emoji_cent(data, cent, new_cents):
    # Call each datapoint to find the distance between all the centroids
    cent = new_cents
    least_emoji_dist = {}
    for i in range(len(data)):
        emoji_dist = {}
        for cent_key in cent:
            centroid = cent[cent_key]
            emoji = data.iloc[i]
            # Find the distance
            cent_dist = distance.euclidean(centroid, emoji[1:])
            emoji_dist[cent_key] = cent_dist
    # Find the least one
            closest_cent = min(emoji_dist, key=emoji_dist.get) 
    # Store the least one in a dict
        least_emoji_dist[emoji[0]] = closest_cent
    return least_emoji_dist, cent


##############################
# Time to do the hard coding



# Use user input to find the centriod number 
user_response = int(input("How many clusters do you want? "))
# First call the functions to get variables
centroids, org_cents = cent_loc(user_response, Emoji_file)

emoji_centroids, res = emoji_cent(Emoji_file, centroids)

new_cents = new_cent_loc(emoji_centroids, Emoji_file, user_response)

for key in centroids:
    val = centroids[key]
    val = val.reset_index()
    val = val.drop('index', axis=1)
    cols = []
    for col in val:
        cols.append(col)
    val = val.rename(columns={col: '0'})
    centroids[key] = val
    
for i in centroids:
    s = centroids[i]
    n = s['0']
    centroids[str(i)] = n
    
cent_bools = []

for i in range(user_response):
    i = str(i)
    x = all(centroids[i] == new_cents[i])
    cent_bools.append(x)

y = all(cent_bools)

t = 0
while y == False:
    t += 1
    cent_bools = []
    
    for i in range(user_response):
        i = str(i)
        
        x = all(centroids[i] == new_cents[i])
        cent_bools.append(x)
    y = all(cent_bools)

    new_emoji_centroids, centroids = new_emoji_cent(Emoji_file, centroids, new_cents)
    
    new_cents = new_cent_loc(emoji_centroids, Emoji_file, user_response)
    print(t)    
if y == True:
    data  = pd.DataFrame(columns=['Emoji', 'Centroid'])
    pic = {}
    for a in res:
        b = res[a]
        for c in b:
            d = c.split('eoji')[1]
                    # Create a df to store the emoji and the centroid
            data = data.append({'Emoji' : emoji_look[d], 'Centroid' : a}, ignore_index=True)

    for roe in data.iterrows():
        pic[roe[1][0]] = roe[1][1]
    
    result = defaultdict(list)
    for key, val in sorted(pic.items()):
        result[val].append(key)
                    
    for m in range(user_response):
        print('Cluster {}:{}'.format(str(m), result[str(m)]))