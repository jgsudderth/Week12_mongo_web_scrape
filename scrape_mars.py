from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import requests
import time



def scrape_all():

    # Initiate headless driver for deployment
    browser = Browser("chrome", executable_path="chromedriver", headless=True)
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store in dictionary.
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "hemispheres": hemispheres(browser),
        "weather": twitter_weather(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

def mars_news(browser):
    #Visiting mars url
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    List_text = news_soup.find("div",class_="content_title")
    news_title = List_text.find("a").get_text()
    P_text = news_soup.find("div", class_="article_teaser_body").get_text()

    return news_title, P_text

def featured_image(browser):

    # Find and click the full image button

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    # Setting up splinter

    # Moving through the pages
    time.sleep(5)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    time.sleep(5)

    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup)

    # Get featured image
    results = soup.find('article')
    extension = results.find('figure', 'lede').a['href']
    link = "https://www.jpl.nasa.gov"
    featured_image_url = link + extension

    return featured_image_url

    # Use the base url to create an absolute url
   

    # return img_url


def hemispheres(browser):

    hemisphere_image_urls = []

    # First, get a list of all of the hemispheres
    links = browser.find_by_css("a.product-item h3")

    # Next, loop through those links, click the link, find the sample anchor, return the href
    for i in range(len(links)):
        hemisphere = {}
        
        # We have to find the elements on each loop to avoid a stale element exception
        browser.find_by_css("a.product-item h3")[i].click()
        
        # Next, we find the Sample image anchor tag and extract the href
        sample_elem = browser.find_link_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
        
        # Get Hemisphere title
        hemisphere['title'] = browser.find_by_css("h2.title").text
        
        # Append hemisphere object to list
        hemisphere_image_urls.append(hemisphere)
        
        # Finally, we navigate backwards
        browser.back()
    return hemisphere_image_urls

def twitter_weather(browser):
    
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    html = browser.html
    weather_soup = BeautifulSoup(html, 'html.parser')
    print(weather_soup)

    twit_text = weather_soup.find("div",class_="js-tweet-text-container")
    twitter_news_title = twit_text.find("p").get_text()
    return twitter_news_title
        
    # return mars_weather


def scrape_hemisphere(html_text):

    # Soupify the html text
    
    # Try to get href and text except if error.
    try:
        pass

    except AttributeError:
        pass


    # return hemisphere


def mars_facts():

   
    # Mars Facts URL
    url = "https://space-facts.com/mars/"

    # Retrieve page with the requests module
    html = requests.get(url)

    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(html.text, 'html.parser')

    # Empty dictionary for info
    mars_profile = {}

    # Get info
    results = soup.find('tbody').find_all('tr')

    # Storing profile information
    for result in results:
        key = result.find('td', 'column-1').text.split(":")[0]
        value = result.find('td', 'column-2').text
        
        mars_profile[key] = value
        
    # Creating a DataFrame
    profile_df = pd.DataFrame([mars_profile]).T.rename(columns = {0: "Value"})
    profile_df.index.rename("Description", inplace=True)
    print(profile_df)

    # Converting to html
    profile_html = "".join(profile_df.to_html().split("\n"))
    # Add some bootstrap styling to <table>
    # return df
    return profile_html

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())