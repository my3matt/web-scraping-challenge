#!/usr/bin/env python
# coding: utf-8

# In[6]:


from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pandas as pd
import time


# In[10]:


#Site Navigation
executable_path = {"executable_path": '/usr/local/bin/chromedriver'}
browser = Browser("chrome", **executable_path, headless=False)


# In[12]:
#define scrape
def scrape():
		mars_data = {}
		mars_data = marsNews()
		mars_data["mars_news"] = output[0]
		mars_data["mars_paragraph"] = output[1]
		mars_data["mars_image"] = marsImage()
		mars_data["mars_weather"] = marsWeather()
		mars_data["mars_facts"] = marsFacts()
		mars_data["mars_hemisphere"]= marsHemisphere()

		return mars_data	

#NASA Mars News URL 

def marsNews():
		news_url = "https://mars.nasa.gov/news/"
		browser.visit(news_url)
		html = browser.html
		soup = bs (html, "html.parser")
		article = soup.find("div", class_='list_text')
		news_title = article.find("div", class_="content_title").text
		news_p = article.find("div", class_ ="article_teaser_body").text
		printtext = [news_title, news_p]

		return printtext


# In[14]:


#JLP Mars Space Images URL 
def marsImage():
	image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser.visit(image_url)
	html = browser.html
	soup = bs(html, "html.parser")
	image = soup.find("img", class_="thumb")["src"]
	featured_image_url= "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars" + image
	return featured_image_url


# In[22]:

def marsWeather():
	import GetOldTweets3 as got
	#Mars weather tweet attempt using API 
	#username = 'MarsWxReport'
	#count= 1
	# Creation of query object
	tweetCriteria = got.manager.TweetCriteria().setUsername("MarsWxReport").setSince("2020-05-20").setUntil("2020-05-23").setMaxTweets(1).setEmoji("unicode")
	tweet = got.manager.TweetManager.getTweets(tweetCriteria)[0]
	return tweet.text


# In[23]:


#Mars Facts
def marsFacts():

	facts_url = "https://space-facts.com/mars/"
	browser.visit(facts_url)
	mars_data = pd.read_html(facts_url)
	mars_data = pd.DataFrame(mars_data[0])
	mars_data.columns= ["Description", "Value"]
	mars_facts = mars_data.to_html(header = True, index = True)
	return mars_facts


# In[24]:


#Mars Hemispheres
def marsHemisphere():
	import time 
	hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	browser.visit(hemispheres_url)
	html = browser.html
	soup = bs(html, "html.parser")
	mars_hemisphere = []

	products = soup.find("div", class_ = "result-list" )
	hemispheres = products.find_all("div", class_="item")

	for hemisphere in hemispheres:
		title = hemisphere.find("h3")[".text"]
		title = title.replace("Enhanced", "")
		end_link = hemisphere.find("a")["href"]
		image_link = "https://astrogeology.usgs.gov/" + end_link
		browser.visit(image_link)
		html = browser.html
		soup=bs(html, "html.parser")
		downloads = soup.find("div", class_="downloads")
		image_url = downloads.find("a")["href"]
		mars_hemisphere.append({"title": title, "img_url": image_url})
	return mars_hemisphere

if __name__ == "__main__":
    print(scrape())


