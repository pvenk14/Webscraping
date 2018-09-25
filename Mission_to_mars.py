
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import pymongo
from splinter import Browser
import requests
import time
import pandas as pd




# # News from NASA Website
# Initialize browser
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


# In[10]:
def scrape():

   # executable_path = {'executable_path': 'chromedriver.exe'}
    #browser = Browser('chrome', **executable_path, headless=False)


    # In[3]:


    #website to scrape
    mars_url = 'https://mars.nasa.gov/news/'
    browser.visit(mars_url)


    # In[4]:


    # Get HTML page with the browser; create BeautifulSoup object; parse with 'html.parser'
    mars_html = browser.html
    soup = BeautifulSoup(mars_html, 'html.parser')

    try:
    #mars_news_data
        news_title = soup.find('ul', class_="item_list").find('li',class_="slide").find('div',class_="content_title").text
        print(f"The news_title is: {news_title}") 
        news_body = soup.find('ul',class_="item_list").find('li',class_="slide").find('div',class_="article_teaser_body").text
        print(f"The News Body is: {news_body}") 


    except AttributeError as e:
        print(e)


    # # JPL Mars Space Images - Featured Image

    # In[11]:


    # URL of NASA site, JPL Featured Space Images to be scraped
    mar_space_images_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(mar_space_images_url)


    # In[12]:


    #find the full image URL
    full_image = browser.find_by_id('full_image')
    full_image.click()


    # In[13]:


    #navigate to link more info
    time.sleep(10)
    more_info = browser.find_link_by_partial_text('more info')
    more_info.click()

    #get html code once at page
    image_html = browser.html


    #parse
    soup = BeautifulSoup(image_html, "html.parser")

    #find path and make full path
    image_path = soup.find('figure', class_='lede').a['href']
    featured_image_url = "https://www.jpl.nasa.gov/" + image_path


    # # ### Mars Weather

    # In[16]:


    # mars weather URL from twitter
    mars_weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(mars_weather_url)

    weather_html = browser.html

    soup = BeautifulSoup(weather_html, 'html.parser')

    mars_weather = soup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    mars_weather


    # # Mars Facts

    # In[21]:


    #get the facts url
    facts_url ='http://space-facts.com/mars/'
    fact_tables = pd.read_html(facts_url)
    mars_fact_df = fact_tables[0]
    mars_fact_df.cloumns = ['Fact','value']
    mars_fact_df


    # In[27]:


    # Use Pandas to convert the data to a HTML table string and save to a file# 
    mars_fact_html = mars_fact_df.to_html()

    mars_fact_df.to_html('MarsFactsTable.html', index=False )

    mars_fact_html


    # # Mars Hemispheres

    # In[29]:


    #Go to astrogeology page and parse the URL 
    hemis_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemis_url)

    hemis_html = browser.html

    soup = BeautifulSoup(hemis_html, "html.parser")



    # In[49]:


    # gets class holding hemisphere images
    hemis_img = soup.find('div', class_="collapsible results")
    hemispheres = hemis_img.find_all('div',class_='item')


    # In[50]:


    #setup list to hold dictionaries
    hemisphere_image_urls =[]


    # In[55]:


    # add values to the list with title and URL dictionary 

    for x in hemispheres:
        #get title and link from main page
        title = x.h3.text
        link = "https://astrogeology.usgs.gov" + x.find('a',class_='itemLink product-item')['href']
        
        #follow link from each page
        browser.visit(link)
        time.sleep(5)
        
        #get image links
        image_page = browser.html
        hem_img = BeautifulSoup(image_page, 'html.parser')
        img_url = hem_img.find('div', class_='downloads').find('li').a['href']
        
        # create image dictionary for each image and title
        image_dict = {}
        image_dict['title'] = title
        image_dict['img_url'] = img_url
        
        hemisphere_image_urls.append(image_dict)
        
    mars_dict = {
        "id": 1,
        "news_title": news_title,
        "news_p": news_body,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "fact_table": mars_fact_df,
        "hemisphere_images": hemisphere_image_urls
    }

    return mars_dict
        

