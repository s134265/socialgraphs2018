
# coding: utf-8

# # Motivation

# # What is our data set?

# For this project it was decided to work with IMDB data. 
# IMDB provides a subset of their data to everyone who might be interesting in analyzing it. The data provided by IMDB are split into multiple files, not all of these files are used for this project.
# The files used for this project is:
# name.basics.tsv.gz
# title.akas.tsv.gz
# title.basics.tsv.gz
# title.crew.tsv.gz
# title.episode.tsv.gz
# title.principals.tsv.gz
# title.ratings.tsv.gz
# The file "title.principals" is the main datafile, which orignally consists of 1.3 Gb of data with 30.674.812 rows and 6 columns.
# These datafiles contains information about movies, actors in those movies, when they movies were made, what the different peoples roles were in the movies, ID of movies and actors, type of movie such as tv show or movie and ratings of these movies.
# 
# Besides these data files, some files containing reviews of movies were also used. These reviews were downloaded from the website Kaggle.com and consists of 100.000 reviews on 14.127 movies.
# The reviews from Kaggle are divided into two folders, each containing 50.000 reviews. Sentiment analysis has already been conducted on some of the reviews, however this was ignored for this project. 
# Besides the moview reviews the data also contains URLS describing which movie the different reviews come from, this is the part linking the movies with the reviews.

# # Why did you chose this/ these particular datasets

# The datasets chosen for this project provides with a way to link actors to each other through their movies. Besides this it also provides reviews for the movies, such that sentiment analysis can be done on these in order to link the sentiment score of the movies actors has been in, to the actors. 
# 
# Some of the data files are also used when cleaning the data and making it more suitable for the project, this was especially important since the data set was very large initially.
# 
# All of these data files therefore provides everything needed in order to make this project, which is why they were chosen.

# # What was your goal for the end user's experience?

# The goal of this project is to find communities of actors/actresses which are enjoyable together. The project is therefore not about find good movies, but instead finding out which actors/actresses make good movies when working together.
# 
# It is therefore possible for an actor to have bad reviews in general, but still being enjoyable to watch when paired up with certain actors/actresses.

# # Data preparation

# We have two type of data:
# * reviews
# * IMBD databases containing actors, movies and rating <br>
# 
# The databases contains alot of irrelevant information such as games and movies with no reviews in the review data set. Therefore we first have to clean our databases in order to keep only the relevant information.
# 
# In this we also comment the different methods and tools used for data cleaning.

# # Preparation for data cleaning

# ### Execution style

# In[1]:


startFromCleanData = True #Start with the raw data imported or the cleaned files
fastExecution = False     #Use the stored graph, position and DF of rebuild them
savingFigures = True      #Whether to save or not the figures produced


# ### Libraries

# In[2]:


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

# In[25]:


def cleanLoadData():
    
    #build the Dataframes
    mDF = pd.read_pickle("obj/moviesDF.pkl")
    aDF = pd.read_pickle("obj/actorsDF.pkl")
    aLL = []
    files = io.open("obj/actorsLinksList.txt", mode="r", encoding="utf-8")
    for row in files:
        split = row.split("\t")
        aLL.append(split)
    files.close()
    
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
    return movieAgeDict,ratingDict,actorName,movieName,mDF,aDF,aLL
    


# Once the data has been cleaned and saved into files, all there is left to do is load the data and use it in the rest of the project. 

# # Cleaned data stats

# As mentioned in the "What is our data set" chapter the original data consists of over 30 million rows and 1.3 Gb of data.
# The cleaned data ends up being around 44.000 rows with a size of 2.1Mb. which is approximately 0,15% of the original data.
