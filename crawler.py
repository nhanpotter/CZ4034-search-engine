import csv
import os
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver


def init_driver():
    # path to local chromedriver
    chromeDriverPath = os.getenv('CHROME_DRIVER_PATH')
    if not chromeDriverPath:
        chromeDriverPath = '/usr/local/bin/chromedriver'

    # set options for chrome driver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(chromeDriverPath, options=chrome_options)
    return driver


class TripAdvisorCrawler:
    # file to store restaurants information and their corresponding reviews
    pathToReviews = "./data/RestaurantReviews.csv"
    pathToStoreInfo = "./data/RestaurantInfos.csv"
    driver = init_driver()

    # restaurant information crawling
    def scrapeRestaurantInfo(self, url):
        print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        # find all details
        ct = soup.findAll("div", {"class": "_2170bBgV"})
        if not ct:
            ct = soup.findAll("div", {"class": "_1XLfiSsv"})
        print(ct)
        # Store name h1 (div = _1hkogt_o)
        storeName = soup.find('h1', class_='_3a1XQ88S').text
        # Averagage rating span (div = Ct2OcWS4)
        avgRating = soup.find('span', class_='r2Cf69qf').text.strip()
        # Store address (within div = _2vbD36Hr _36TL14Jn)
        storeAddress = soup.find('div', class_='_2vbD36Hr _36TL14Jn').find('span', class_='_2saB_OSe').text.strip()
        # No of reviews (within div = Ct2OcWS4)
        noReviews = soup.find('a', class_='_10Iv7dOs').text.strip().split()[0]
        # Cuisines (within div = _1XLfiSsv)
        cuisineType = ct[1].string
        # Price Range (within div = _1XLfiSsv)
        priceRange = ct[0].string
        # Special diet (within div = _1XLfiSsv)
        specialDiet = ct[2].string
        # District (within div = _2vbD36Hr _36TL14Jn)
        district = soup.find('span', class_='_2saB_OSe _1OBMr94N').text.strip()
        # Scrape ratings for other values
        resultsTab = soup.find('div', class_='ppr_rup ppr_priv_detail_overview_cards').find('div', class_='ui_columns')
        rateReview = resultsTab.find_all('div', class_='jT_QMHn2')

        ratings = []

        for rate in rateReview:
            bars = rate.find('span', class_='_377onWB-').findChildren('span')
            barval = str(bars[0]).split('_')[3]
            print("barval value " + barval[0] + "." + barval[1])
            barnew = barval[0] + "." + barval[1]
            ratings.append(barnew)

        # Write data to csv and export to file
        with open(self.pathToStoreInfo, mode='a', encoding="utf-8") as trip:
            data_writer = csv.writer(trip, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, lineterminator="\n")
            print(ratings)
            if len(ratings) == 3:
                data_writer.writerow(
                    [storeName, storeAddress, avgRating, noReviews, cuisineType, priceRange, specialDiet, district,
                     ratings[0], ratings[1], ratings[2], "0"])
            else:
                data_writer.writerow(
                    [storeName, storeAddress, avgRating, noReviews, cuisineType, priceRange, specialDiet, district,
                     ratings[0], ratings[1], ratings[2], ratings[3]])
            print(url, " written to csv")

    def scrapeReviews(self, url, maxNoReviews):
        reviewCount = 0
        '''
        form: 
        {
            "success": bool,
            "name" : ...,
            "location" : ...., 
            "reviews" : [
                {
                    "name" : ...., 
                    "location" : ...., 
                    "reviewer" : ...., 
                    "rating" : ...., 
                    "reviewText" : ....
                }
            ]
        }
        '''
        data = {}  # TODO: store all the information related to a restaurant;
        data["reviews"] = []
        while reviewCount != maxNoReviews:
            # Requests
            self.driver.get(url)
            time.sleep(1)
            # Click More button
            more = self.driver.find_elements_by_xpath("//span[contains(text(),'More')]")
            for x in range(0, len(more)):
                try:
                    self.driver.execute_script("arguments[0].click();", more[x])
                    time.sleep(3)
                except:
                    pass
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            # Store name
            storeName = soup.find('h1', class_='_3a1XQ88S').text
            # Store location
            storeLoc = soup.find('div', class_='_2vbD36Hr _36TL14Jn').find('span', class_='_2saB_OSe').text.strip()
            # Reviews
            results = soup.find('div', class_='listContainer hide-more-mobile')
            try:
                reviews = results.find_all('div', class_='prw_rup prw_reviews_review_resp')
            except Exception:
                continue
            data["name"] = storeName
            data["location"] = storeLoc
            data["success"] = True
            # Export to csv
            try:
                with open(self.pathToReviews, mode='a', encoding="utf-8") as trip_data:
                    data_writer = csv.writer(trip_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL,
                                             lineterminator="\n")
                    for review in reviews:
                        ratingDate = review.find('span', class_='ratingDate').get('title')
                        text_review = review.find('p', class_='partial_entry')
                        if len(text_review.contents) > 2:
                            reviewText = str(text_review.contents[0][:-3]) + ' ' + str(text_review.contents[1].text)
                        else:
                            reviewText = text_review.text
                        reviewerUsername = review.find('div', class_='info_text pointer_cursor')
                        reviewerUsername = reviewerUsername.select('div > div')[0].get_text(strip=True)
                        rating = review.find('div', class_='ui_column is-9').findChildren('span')
                        rating = str(rating[0]).split('_')[3].split('0')[0]
                        # data_writer.writerow([storeName, storeLoc, reviewerUsername, ratingDate, reviewText, rating])
                        reviewCount += 1
                        print("Comment #", reviewCount, " for ", url)
                        data["reviews"].append({
                            "name": storeName,
                            "date inserted": ratingDate,
                            "location": storeLoc,
                            "username": reviewerUsername,
                            "review": reviewText,
                            "rating": rating
                        })
                        if reviewCount >= maxNoReviews:
                            break
            except:  # in case error in crawling the data
                data["success"] = False
                data["reviews"] = []
                return data
            # Go to next page if exists
            try:
                unModifiedUrl = str(soup.find('a', class_='nav next ui_button primary', href=True)['href'])
                url = 'https://www.tripadvisor.com' + unModifiedUrl
            except:
                reviewCount = maxNoReviews

        return data


if __name__ == '__main__':
    crawler = TripAdvisorCrawler()
    start = time.time()
    data = crawler.scrapeReviews(
        'https://www.tripadvisor.com.sg/Restaurant_Review-g294265-d3916132-Reviews-Momma_Kong_s-Singapore.html', 10)
    print(data)
    print(time.time() - start)
