# -*- coding: utf-8 -*-
"""
Created on Thu Oct 31 14:39:14 2019

@author: ASUS
"""


# coding: utf-8

# In[5]:


import requests
from bs4 import BeautifulSoup
import pandas
import csv
import re

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
page_no = 1
list_restaurants =[]

for page in range(2000):
    print(page_no)
    response = requests.get("https://www.zomato.com/jakarta/restaurants?page={0}".format(page_no), headers=headers)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    search_list = soup.find_all("div", {'id': 'orig-search-list'})
    list_content = search_list[0].find_all("div", {'class': 'content'})
    for i in range(0,15):
        res_name = list_content[i].find("a", {'data-result-type': 'ResCard_Name'})
        locality = list_content[i].find("b")
        ratings = list_content[i].find("div", {'data-variation': 'mini inverted'})
        if ratings is None:
            continue
        rest6 = list_content[i].find_all("div", {'class': 'search-page-text clearfix row'})
        rest7 = rest6[0].find_all("span", {'class': 'col-s-11 col-m-12 nowrap pl0'})
        rest8 = rest7[0].find_all("a")
        cuisines = [e.string for e in rest8]
        cost_for_two = rest6[0].find("span", {'class': 'col-s-11 col-m-12 pl0'})
        if cost_for_two is None:
            continue
        votes = list_content[i].find("span", {'class': re.compile(r'rating-votes-div*')})
        if votes is None:
            continue
        dataframe ={}
        dataframe["rest_name"] = res_name.string.replace('\n', ' ')
        dataframe["locality"] = locality.string.replace('\n', ' ')
        dataframe["rating"] = ratings.string.replace('\n', ' ')
        dataframe["cuisines"] = cuisines
        dataframe["cost_for_two"] = cost_for_two.string[1:]
        dataframe["votes"] = votes.string.split()[0]
        list_restaurants.append(dataframe)
    page_no+=1
    
df = pandas.DataFrame(list_restaurants)
df.to_csv("daftar_restoran_zomato.csv")


# In[5]:


import requests
from bs4 import BeautifulSoup
import re
import pandas
import csv

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
page_no = 1
restaurant_reviews =[]

for page in range(2000):
    print(page_no)
    response = requests.get("https://www.zomato.com/jakarta/restaurants?page={0}".format(page_no), headers=headers)
    content = response.content
    soup = BeautifulSoup(content, "html.parser")
    search_list = soup.find_all("div", {'id': 'orig-search-list'})
    list_content = search_list[0].find_all("div", {'class': 'content'})
    for i in range(0,15):
        res_name = list_content[i].find("a", {'data-result-type': 'ResCard_Name'})
        ratings = list_content[i].find("div", {'data-variation': 'mini inverted'})
        if ratings is None:
            continue
        res_url = res_name.get('href')
        response_url = requests.get(res_url, headers=headers)
        content_url = response_url.content
        soup_url = BeautifulSoup(content_url, "html.parser")
        merch_name = soup_url.find_all("div", {'class': 'header nowrap ui left'})
        merch_ratings = soup_url.find_all("div", {'class': re.compile(r'ttupper fs12px left bold zdhl2 tooltip*')})
        try:
            popular = soup_url.find_all("a", {'data-sort': 'reviews-top'})
            num_reviews = int(popular[0].find('span').string)
        except:
            continue
        if(num_reviews > 10):
            for j in range(0, 10):
                name = merch_name[j].find('a')
                ratings = merch_ratings[j].get('aria-label').split()[1]
                dataframe ={}
                dataframe["rest_name"] = res_name.string.replace('\n', ' ')
                dataframe["cust_name"] = name.string.replace('\n', ' ')
                dataframe["cust_rating"] = ratings
                restaurant_reviews.append(dataframe)
        else:
            for j in range(0, num_reviews):
                name = merch_name[j].find('a')
                ratings = merch_ratings[j].get('aria-label').split()[1]
                dataframe ={}
                dataframe["rest_name"] = res_name.string.replace('\n', ' ')
                dataframe["cust_name"] = name.string.replace('\n', ' ')
                dataframe["cust_rating"] = ratings
                restaurant_reviews.append(dataframe)
    page_no+=1
    
df = pandas.DataFrame(restaurant_reviews)
df.to_csv("pendapat_tentang_zomato.csv", index=False)