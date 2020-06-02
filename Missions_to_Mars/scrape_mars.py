from splinter import Browser
from bs4 import BeautifulSoup as BS
import pandas as pd
import requests
import re

def scrape():
    
    #make a dict to store everything
    mars_dict = {}

    # URL of pages to be scraped
    news_url = 'https://mars.nasa.gov/news'
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    facts_url = "https://space-facts.com/mars/"
    hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    
    #browser setup
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome')
    

    '''NASA Mars News'''
    #create BeautifulSoup object and parse
    browser.visit(news_url)
    news_html = browser.html
    news_soup = BS(news_html,"html.parser")

    #find the latest news title and paragraph
    news_title = news_soup.find("div",class_="content_title").text
    news_para = news_soup.find("div", class_="article_teaser_body").text

    #add to dict
    mars_dict['news_title'] = news_title
    mars_dict['news_para'] = news_para


    '''JPL Mars Space Images - Featured Image'''

    # Visit & Scrape featured image with Beautiful Soup
    browser.visit(image_url)
    image_html = browser.html
    image_soup = BS(image_html, 'html.parser')

    # Retrieve featured image
    feature_img = image_soup.find('article',attrs={'class':'carousel_item'})
    feature_img_url_string = feature_img['style']
    featured_image_link = re.findall(r"'(.*?)'",feature_img_url_string)

    #combine the base url with the first img url
    featured_image_url = 'https://www.jpl.nasa.gov'+ featured_image_link[0]

    #add to dict
    mars_dict['featured_image_url'] = featured_image_url

    '''Mars Weather'''
    
    # Visit & Scrape weather data with Beautiful Soup
    result = requests.get(weather_url)
    weather_html = result.text
    weather_soup = BS(weather_html,'html.parser')

    #Retrieve the weather from the newest tweet
    mars_weather = weather_soup.find(class_='tweet-text').get_text()
    
    #add to dict
    mars_dict['mars_weather'] = mars_weather

    '''Mars Facts'''

    #Visit the Mars Facts Site Using Pandas to Read
    mars_data = pd.read_html(facts_url)
    mars_df = pd.DataFrame(mars_data[0])
    
    #convert the data to a HTML table string
    html_table = mars_df.to_html(header = False, index = False)
    html_table = html_table.replace('\n', '')

    #add to dict
    mars_dict['html_table'] = html_table

    '''Mars Hemispheres'''

    # Visit & Scrape images of Mars Hemispheres with Beautiful Soup
    browser.visit(hemi_url)
    hemi_soup = BS(browser.html, "html.parser")

    #get the 4 hemispheres (class of 'item')
    hemispheres = hemi_soup.select('div.item')

    #create dictionary to store titles & links to images
    hemisphere_image_urls = []

    #Iterate through each hemisphere
    for hemi in hemispheres:
        img_title = (hemi.find('h3').text).replace(' Enhanced', '') 
        browser.click_link_by_partial_text(img_title)
        soup = BS(browser.html, "html.parser")
        full = soup.find('a', text='Sample')
        img_url = full['href']
        hemisphere_image_urls.append({"title": img_title, "img_url": img_url})
        browser.back()

    #close browser
    browser.quit()    

    #add to dict
    mars_dict['hemisphere_image_urls'] = hemisphere_image_urls

    return mars_dict