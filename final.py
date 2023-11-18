from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import urlScraper


browser = webdriver.Chrome()

LocationName = []
reviewers = []
ratings = []
review_titles = []
reviews = []


def scrap_review(url):

    while url:

        browser.get(url)
        content = browser.page_source

        soup = BeautifulSoup(content, features='html.parser')

        place = soup.find("div", class_="mmBWG")
        review_section= soup.find("div", class_="LbPSX")

        name = place.find('h1').text

        reviewer = review_section.find_all("div", class_= "mwPje f M k")
        rating = review_section.find_all("svg", class_="UctUV d H0")
        review_box = review_section.find_all("span", class_="yCeTE")

        review_title = []
        review = []

        for i in range(len(review_box)):
            if i % 2 == 0:
                review_title.append(review_box[i])
            else:
                review.append(review_box[i])


        for i in range(len(reviewer)):

            LocationName.append(name)
            reviewers.append(reviewer[i].find("span", class_="biGQs _P fiohW fOtGX").text)
            ratings.append(float(rating[i]['aria-label'].split(" ")[0].strip()))
            review_titles.append(review_title[i].text)
            reviews.append(review[i].text)


        try:
            url = review_section.find("div", class_="xkSty")
            url = "https://www.tripadvisor.com"+url.find("a")['href']
        except:
            url = False

    store_data(LocationName, reviewers, ratings, review_titles, reviews)



def store_data(LocationName, reviewers, ratings, review_titles, reviews):

    df = pd.DataFrame(
        {
            'Location': LocationName,
            'Reviewer': reviewers,
            'Rating': ratings,
            'Review Title': review_titles,
            'Review': reviews
        }
    )

    df.to_csv('reviews.csv', mode='a', index=False, header=False)



urls = urlScraper.all_urls('https://www.tripadvisor.com/Attractions-g293935-Activities-oa0-Bangladesh.html')

for i in urls:
    scrap_review(i)

browser.quit()

