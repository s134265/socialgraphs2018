# Import Libraries
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import fa2
import math
import community
import matplotlib.cm as cm
import matplotlib.image as mpimg
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import io
from collections import Counter
from wordcloud import WordCloud
from scipy.special import zeta
import pickle
# Rendering Parameters
title_font = {'family': 'sans-serif',
        'color':  '#000000',
        'weight': 'normal',
        'size': 16,
        }
#COLORS
mBlue = "#55638A"     # For actor
fRed = "#9E1030"    # For actress




# ## LOAD & CLEAN DATA FUNCTION 


def cleanLoadData():
    
    #build the Dataframes
    mDF = pd.read_pickle("obj/moviesDF.pkl")
    aDF = pd.read_pickle("obj/actorsDF.pkl")
    
    
    #rebuild the Dictionnary
    movieAgeDict = {}
    ratingDict = {}
    actorName = {}
    movieName = {}
    #movies
    for i in mDF.index:
        iD = mDF.loc[i].at["iD"]
        rating = mDF.loc[i].at["Rating"]
        title = mDF.loc[i].at["Title"]
        year = mDF.loc[i].at["Year"]
        movieAgeDict[iD] = year
        ratingDict[iD] = rating
        movieName[iD] = title
    #actors
    for i in aDF.index:
        iD = aDF.loc[i].at["iD"]
        name = aDF.loc[i].at["Name"]
        actorName[iD]= name
    
    #Actors in list
    aLL = []
    files = io.open("obj/actorsLinksList.txt", mode="r", encoding="utf-8")
    for row in files:
        split = row.replace("\n","").split("\t")
        if split[2] in ratingDict.keys():
            aLL.append(split)
    files.close()
    return movieAgeDict,ratingDict,actorName,movieName,mDF,aDF,aLL
    

# GRAPH LOAD
def graphBuild():
    
    # Get the graphs:
    full = nx.read_gpickle('obj/full.gpickle')
    g1970 = nx.read_gpickle('obj/graph_1970.gpickle')
    g1980 = nx.read_gpickle('obj/graph_1980.gpickle')
    g1990 = nx.read_gpickle('obj/graph_1990.gpickle')
    g2000 = nx.read_gpickle('obj/graph_2000.gpickle')
    gNow = nx.read_gpickle('obj/graph_now.gpickle')
    
    # Graph Dictionnaries
    gPeriod = {}
    gPeriod['1970']=g1970
    gPeriod['1980']=g1980
    gPeriod['1990']=g1990
    gPeriod['2000']=g2000
    gPeriod['now']=gNow
    
    # Graph Titles
    ttl = {}
    ttl["1970"] = "1900-1970"
    ttl["1980"] = "1970-1980"
    ttl["1990"] = "1980-1990"
    ttl["2000"] = "1990-2000"
    ttl["now"] = "2000+"
    
    # Positions
    periods = [1900,1970,1980,1990,2000]
    #fullgraph
    full_positions = {}
    path = "DATA/forceAtlasPositions.txt"
    files = io.open(path, mode="r", encoding="utf-8")
    for row in files:
        split = row.split("\t")
        full_positions[split[0]] = (float(split[1]),float(split[2]))
    files.close()
    #period graphs
    posPeriod = {}
    for key in gPeriod:
        posit={}
        path = "DATA/forceAtlasPositions_"+key+".txt"
        files = io.open(path, mode="r", encoding="utf-8")
        for row in files:
            split = row.split("\t")
            posit[split[0]] = (float(split[1]),float(split[2]))
        files.close()
        posPeriod[key] = posit
        
    return full,gPeriod,ttl,full_positions,posPeriod