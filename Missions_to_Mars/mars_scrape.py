

def scrape():
    # Dependencies
    from bs4 import BeautifulSoup as bs
    from splinter import Browser
    import requests
    import pymongo
    import time
    import os
    import pandas as pd

    # def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_dict = {}

    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)

    # Create a Beautiful Soup object
    news_html = browser.html
    soup = bs(news_html,'html.parser')

    try:
        # Identify and return title of news article
        news_title = soup.find('div', class_="content_title").text
        # Identify and return paragraph text
        news_p = soup.find('div', class_="article_teaser_body").text
    except:
        return None

    mars_dict['news_title'] = news_title
    mars_dict['news_p'] = news_p

    # JPL Mars Space Images - Featured Image
    jpl_nasa_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_nasa_url)

    html = browser.html
    soup = bs(html,"html.parser")

    # Featured Image
    starting_url = 'https://www.jpl.nasa.gov'
    featured_image_url = soup.find('div',class_='carousel_container').article.footer.a['data-fancybox-href']
    featured_image = starting_url + featured_image_url

    mars_dict['featured_image'] = featured_image

    # Weather
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    html = browser.html
    weather_soup = bs(html,"html.parser")

    mars_weather = weather_soup.find('span',class_= "css-901oao css-16my406 r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0")

    mars_dict['mars_weather'] = mars_weather

    # Facts
    mars_facts_url = "https://space-facts.com/mars/"

    table = pd.read_html(mars_facts_url)
    df= table[1]
    html_table = df.to_html()
    html_table.replace('\n', '')
    mars_facts = df.to_html('table.html')

    mars_dict['mars_facts'] = mars_facts

    # Hemispheres
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)

    hemisphere_img_urls=[]

    links = browser.find_by_css('a.product-item h3')
    for i in range(len(links)):
        hemisphere = {}
        browser.find_by_css('a.product-item h3')[i].click()
        sample = browser.links.find_by_text('Sample').first
        hemisphere['image_url'] = sample['href']
        hemisphere['title'] = browser.find_by_css('h2.title').text
        hemisphere_img_urls.append(hemisphere)
        browser.back()

    mars_dict['hemisphere_img_urls'] = hemisphere_img_urls

    return mars_dict

