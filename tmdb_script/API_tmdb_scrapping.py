#!/usr/bin/env python
# coding: utf-8

# In[2]:


#get info from tmdb api
import tmdbsimple as tmdb
import pandas as pd
import numpy as np
import re
tmdb.API_KEY = '38d152a903074622d32b3cd9efc51c0d'


# In[3]:


#read links file (on the same directory as this script)
df = pd.read_csv("links.csv")
df.head()


# In[4]:


df.info()


# In[5]:


#remove tmdbId nulls
df = df.dropna()
df.info()


# In[6]:


columns = ["tmdbId","poster_path","release_date", "runtime", "adult", "popularity","budget","revenue", "production_companies", "production_countries"]
df_tmdb = pd.DataFrame(columns=columns)


# In[8]:


pd.options.display.float_format = '{:.0f}'.format
movie_list=df['tmdbId']
movie_list


# In[9]:


movie = tmdb.Movies(862)
response = movie.info()
print(response)
#print(movie.poster_path)
#print(movie.release_date)
#print(movie.overview)
#print(movie.production_countries)


# In[10]:


i=0
lenght = len(movie_list)

for movieid in movie_list:
    i+=1
    print(str(i)+"/"+str(lenght))  #print logs
    try:
        movie = tmdb.Movies(movieid)
        response = movie.info()
        companies = movie.production_companies
        countries = movie.production_countries
        companies_list = [company['name'] for company in companies]
        countries_list = [country['name'] for country in countries]    
        df_tmdb = df_tmdb.append({"tmdbId":movieid, "poster_path":"http://image.tmdb.org/t/p/original" +str(movie.poster_path), "release_date":movie.release_date,                                  "popularity":movie.popularity, "runtime":movie.runtime, "adult":movie.adult,
                                  "budget":movie.budget, "revenue":movie.revenue, "production_companies": '|'.join(companies_list),\
                                  "production_countries": '|'.join(countries_list)}, ignore_index=True)
    
    except:
        print("ERROR ON " + str(movieid))    #can give error on request
        continue


# In[11]:


df_tmdb.shape


# In[12]:


df_tmdb.head()


# In[13]:


df_final = df.join(df_tmdb.set_index('tmdbId'), on='tmdbId')
df_final.head()


# In[14]:


df_final.describe()


# In[15]:


df_final.info()


# In[20]:


df_final.to_csv('tmdb.csv', encoding='utf-8-sig')

