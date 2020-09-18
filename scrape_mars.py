# Dependencies and Setup
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import datetime as dt

# # Set Executable Path & Initialize Chrome Browser
# executable_path = {"executable_path": "/Users/prim/Downloads/chromedriver"}
# browser = Browser("chrome", **executable_path, headless=False)

# #Creating a dictionary
# def scrape():
#     executable_path = {"executable_path": "/Users/prim/Downloads/chromedriver"}
#     browser = Browser("chrome", **executable_path, headless=False)
#     news_title, news_paragraph = mars_news(browser)
#     dictionary_mars = {
#         "news_title":  news_title,
#         "news_paragraph" : news_paragraph(),
#         "img_url": featured_image(browser),
#         "mars_fact": mars_fact(),
#         "mars_hemisphere": hemisphere(browser)
#     }
#     return dictionary_mars


# NASA Mars News Site Web Scraper
def mars_news(browser):
    # Visit the NASA Mars News Site
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)
    
    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")

    # Parse Results HTML with BeautifulSoup
    try:
        slide_element = news_soup.select_one("ul.item_list li.slide")
        slide_element.find("div", class_="content_title")

        # Scrape the Latest News Title
        news_title = slide_element.find("div", class_="content_title").get_text()

        news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_paragraph


# JPL Mars Space Images

def featured_image(browser):
    # Visit the NASA JPL
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    # Ask Splinter to Go to Site 
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()

    # Find "More Info" Button and Click It
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()

    # Parse Results HTML with BeautifulSoup
    html = browser.html
    image_soup = BeautifulSoup(html, "html.parser")

    img = image_soup.select_one("figure.lede a img")
    try:
        img_url = img.get("src")
    except AttributeError:
        return None 
   # Use Base URL to create URL
    img_url = f"https://www.jpl.nasa.gov{img_url}"
    return img_url

# Mars Facts
def mars_fact():
    try:
# Visit the Mars Facts Site Using Pandas to Read
        mars_facts = pd.read_html("https://space-facts.com/mars/")[1]
        print(mars_facts)
    except:
        return None
    mars_facts.reset_index(inplace=True)
    mars_facts.columns=["ID", "Properties", "Mars", "Earth"]
    return mars_facts.to_html

# Mars Hemispheres
def hemisphere(browser):
    # Visit the  Site
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    hemisphere_image_urls = []

    # Get a List of All the Hemisphere
    links = browser.find_by_css("a.product-item h3")
    for item in range(len(links)):
        hemisphere = {}
        
        browser.find_by_css("a.product-item h3")[item].click()
        
        sample_element = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample_element["href"]
        
        # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        # Append Hemisphere 
        hemisphere_image_urls.append(hemisphere)
        
        # Navigate Backwards
        browser.back()
    return hemisphere_image_urls

# Helper Function
def scrape_hemisphere(html_text):
    hemisphere_soup = BeautifulSoup(html_text, "html.parser")
    try: 
        title_element = hemisphere_soup.find("h2", class_="title").get_text()
        sample_element = hemisphere_soup.find("a", text="Sample").get("href")
    except AttributeError:
        title_element = None
        sample_element = None 
    hemisphere = {
        "title": title_element,
        "img_url": sample_element
    }
    return hemisphere



# Main Web Scraping

def scrape_all():
    executable_path = {"executable_path": "/Users/prim/Downloads/chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)
    news_title, news_paragraph = mars_news(browser)
    img_url = featured_image(browser)
    fact = mars_fact
    hemisphere_image_urls = hemisphere(browser)
    timestamp = dt.datetime.now()

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": img_url,
        "fact": fact,
        "hemispheres": hemisphere_image_urls,
        "last_modified": timestamp
    }
    browser.quit()
    return data 

if __name__ == "__main__":
    print(scrape_all())