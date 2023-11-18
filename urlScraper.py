from selenium import webdriver
from bs4 import BeautifulSoup
import time


def all_urls(url):

    browser = webdriver.Chrome()

    urls = []

    while url:
        browser.get(url)
        time.sleep(4)
        content = browser.page_source

        soup = BeautifulSoup(content, features='html.parser')

        places = soup.find_all("div", class_ = "hZuqH")


        for place in places:

            try:
                r = place.find("div", class_="jVDab o W f u w JqMhy")
                r = int(r.find("span", class_="biGQs _P pZUbB osNWb").text)
            except:
                r = False


            if r != False and r > 5:
                urls.append("https://www.tripadvisor.com" + place.find("a")['href'])

        try:
            url = soup.find("div", class_="xkSty")
            url = "https://www.tripadvisor.com" + url.find("a")['href']
        except:
            url = False

    browser.quit()
    return urls




