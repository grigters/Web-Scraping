# import dependencies
import pandas as pd
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import time
import re
# importing ssl and changing to an unsecured connection
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():

    ## NASA Mars News ##
    # url to be scraped
    url = 'https://mars.nasa.gov/news/'
    # get page with request module
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find(class_="content_title")
    title = title.text.strip()

    article = soup.find(class_="rollover_description_inner")
    article = article.text.strip()

    print(title, article)

    ## JPL Mars Space Images ##
    # Visit the url for JPL Featured Space Image
    browser = init_browser()
    time.sleep(1)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    base_url = 'https://www.jpl.nasa.gov'
    browser.visit(url)

    # Navigate to the page with the full image
    time.sleep(5)
    browser.click_link_by_partial_text('FULL IMAGE')

    time.sleep(3)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Save the image in a variable
    try:
        time.sleep(5)
        image = soup.find(class_="fancybox-image")["src"]
        featured_image_url = f"{base_url}{image}"
        print(featured_image_url)
    except:
        print('You ran the code too fast!')

    ## Mars Weather ##
    # url to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'
    # get page with request module
    response = requests.get(url)

    # create beautiful soup object and pretty print
    soup = BeautifulSoup(response.text, 'html.parser')

    # scrape the latest Mars weather tweet from the page
    mars_weather = soup.find(class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    # remove the image from the tweet
    mars_weather.find(['a']).decompose()
    # remove any line break code
    mars_weather = mars_weather.text.replace("\n", " ").strip()
    print(mars_weather)

    # remove image URL (if there is one) at the end of the tweet
    patterns = ['r"http\S+"', 'r"\xa0pic\S+"', 'r"pic\S+"', 'r"pbs\S+"']
    for pattern in patterns:
        mars_weather = re.sub(pattern, "", mars_weather).strip()
    
    print(mars_weather)

    ## Mars Facts ##
    # Visit the Mars Facts webpage and use Pandas to scrape the table
    url = "https://space-facts.com/mars/"

    # Use Pandas to convert read data in the table
    tables = pd.read_html(url)

    # add column names to the table and set index
    df = tables[0]
    df.columns = ['Description', 'Value']
    df.set_index('Description', inplace=True)

    # Use Pandas to convert the data to a HTML table string
    html_table = df.to_html()
    html_table = html_table.replace('\n', '')
    print(html_table)

    ## Mars Hemisphere ##
    # url to be scraped
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    base_url = 'https://astrogeology.usgs.gov'
    # get page with request module
    response = requests.get(url)

    # create beautiful soup object and pretty print
    soup = BeautifulSoup(response.text, 'html.parser')

    # scrape all the urls needed from the home page using list comprehension
    links = soup.find_all(class_="item")
    urls = [f'{base_url}'+link.a['href'] for link in links]
    print(urls)

    hemisphere_image_urls = []
    for url in urls:
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        time.sleep(2)
        title = soup.find(class_="title").text
        image = soup.find(class_="downloads").a['href']
        hem_dict = {'title': title, 'img_url': image}
        hemisphere_image_urls.append(hem_dict)
    
    browser.quit()

    print(hemisphere_image_urls)


    mars_data = {
	"title": title,
	"article": article,
	"featured_image_url": featured_image_url,
	"mars_weather": mars_weather,
	"html_table": html_table,
	"hemisphere_image_urls": hemisphere_image_urls
    }

    return mars_data