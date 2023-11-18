from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

#service = Service(executable_path='D:/work/chromeDriver/chromedriver-win64/chromedriver.exe')
#options = webdriver.ChromeOptions()
#browser = webdriver.Chrome(service=service, options=options)

#browser = webdriver.Chrome(executable_path="D:\work\chromeDriver\chromedriver.exe")

browser = webdriver.Chrome()


LocationName = []
reviewers = []
ratings = []
reviewTitles = []
reviews = []



def scrapReview(url):

    while(url != False):

        browser.get(url)
        content = browser.page_source

        soup = BeautifulSoup(content, features='html.parser')

        place = soup.find("div", class_="mmBWG")
        reviewSection= soup.find("div", class_="LbPSX")

        name = place.find('h1').text

        print(name)

        #reviewer = reviewSection.find_all("span", class_="biGQs _P fiohW fOtGX")
        reviewer = reviewSection.find_all("div", class_= "mwPje f M k")
        rating = reviewSection.find_all("svg", class_="UctUV d H0")
        fullReview = reviewSection.find_all("span", class_="yCeTE")
        #review = reviewSection.find_all("div", class_="_T FKffI bmUTE")
        #review = reviewSection.find_all("div", class_="_T FKffI bmUTE")

        reviewTitle = []
        review = []


        for i in range(len(fullReview)):
            if i%2==0:
                reviewTitle.append(fullReview[i])
            else:
                review.append(fullReview[i])

        print(len(reviewer), len(rating), len(reviewTitle), len(review))

        for i in range(len(reviewer)):

            LocationName.append(name)
            reviewers.append(reviewer[i].find("span", class_="biGQs _P fiohW fOtGX").text)
            ratings.append(float(rating[i]['aria-label'].split(" ")[0].strip()))
            reviewTitles.append(reviewTitle[i].text)
            reviews.append(review[i].text)



        try:
            url = reviewSection.find("div", class_="xkSty")
            url = "https://www.tripadvisor.com"+url.find("a")['href']
        except:
            url = False

    #browser.quit()
    storeData(LocationName, reviewers, ratings, reviewTitles, reviews)



def storeData(LocationName, reviewers, ratings, reviewTitles, reviews):

    df = pd.DataFrame(
        {
            'Location': LocationName,
            'Reviewer': reviewers,
            'Rating': ratings,
            'Review Title': reviewTitles,
            'Review': reviews
        }
    )

    df.to_csv('attractions.csv', mode='a', index=False, header=False)


    #df.to_excel('attractions.xlsx', sheet_name="Sheet1")

    #df.to_csv('attractions.csv', mode='a', index=False, header=False)
    #browser.quit()



#urls = urlScraper.all_urls("https://www.tripadvisor.com/Attractions-g293935-Activities-a_allAttractions.true-Bangladesh.html")
urls= ['https://www.tripadvisor.com/Attraction_Review-g23978483-d8557766-Reviews-Fantasy_Kingdom-Jamgora_Dhaka_Division.html', 'https://www.tripadvisor.com/Attraction_Review-g667472-d12113853-Reviews-1971_Genocide_Torture_Archive_Museum-Khulna_City_Khulna_Division.html']#scrapReview(urls)

#for i in (urlScraper.all_urls("https://www.tripadvisor.com/Attractions-g293935-Activities-a_allAttractions.true-Bangladesh.html")):
for i in urls:

    scrapReview(i)


browser.quit()

