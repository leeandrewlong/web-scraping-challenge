# --- dependencies and setup ---
from dataclasses import dataclass
from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime as dt
import requests

def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    news_title, news_p = mars_news(browser)
    data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image":featured_image(browser),
        "mars_facts": mars_facts(browser),
        "mars_hemisphere": mars_hemisphere(browser),
        "last modified" : dt.datetime.now()
    }

    browser.quit()
    return 
def mars_news(browser):

    #Navigate Url to scrape
    Nasa_News_Url = "https://redplanetscience.com"
    browser.visit(Nasa_News_Url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    results = soup.find("div", class_ = "list_text")
    news_title = results.find("div", class_ = "content_title").text
    news_p = results.find("div", class_ = "article_teaser_body").text
    return (news_title, news_p)



def featured_image(browser):
    #Navigate Url to scrape
    Space_Images_Url = "https://spaceimages-mars.com"
    browser.visit(Space_Images_Url)
    time.sleep(1)

    # Scrape image into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    results = soup.find("div", class_ = "list_text")
    featured_image_url = "https://spaceimages-mars.com/image/featured/mars1.jpg"
    return featured_image_url

def Mars_Facts(browser):
    #Navigate Url to scrape
    Mars_Facts = "https://galaxyfacts-mars.com"
    browser.visit(Mars_Facts)
    time.sleep(1)

# Scrape image into Soup

    Mars = pd.read_html(Mars_Facts)

    df = Mars[0]
    df.columns=["Description", "Mars Value", "Earth Value"]
    return df.to_html("marstable.html",index = False)

def mars_hemisphere(browser):
    #Navigate to url for scraping
    base_url  = "https://marshemispheres.com/"
    browser.visit(base_url)
    #Container to hold  our loop iterations
    all_urls = []
    #Iterate through the 4 different links to get the images needed
    for x in range(4):
        html = browser.html
        soup = bs(html, "html.parser")
    
        title = soup.find_all("h3")[x].get_text()
        browser.find_by_tag("h3")[x].click()
    
        html = browser.html
        soup = bs(html, "html.parser")
    
        img_url = soup.find("img", class_="wide-image")["src"]
        all_urls.append({
            "title":title,
            "img_url": base_url+img_url
        })
        browser.back()
    return all_urls
if __name__ == "__main__":
    print(scrape())
