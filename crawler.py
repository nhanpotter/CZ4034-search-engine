import os
import time

from bs4 import BeautifulSoup
from selenium import webdriver


def init_driver():
    # path to local chromedriver
    chromeDriverPath = os.getenv('CHROME_DRIVER_PATH')
    print(chromeDriverPath)
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

    driver = init_driver()

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
                "review" : ....
            }
        ]
    }
    '''
    def scrapeReviews(self, url, maxNoReviews):
        reviewCount = 0
        # store restaurant info
        data = {}
        # store list of reviews
        data["reviews"] = []
        # in case no reviews could be retrieve from the restaurant
        data["success"] = False
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
            try:
                # Store name
                storeName = soup.find('h1', class_='_3a1XQ88S').text
                # Store location
                storeLoc = soup.find('div', class_='_2vbD36Hr _36TL14Jn').find('span', class_='_2saB_OSe').text.strip()
                # Reviews
                results = soup.find('div', class_='listContainer hide-more-mobile')
                # name and location of restaurant
                data["name"] = storeName
                data["location"] = storeLoc
                try:
                    reviews = results.find_all('div', class_='prw_rup prw_reviews_review_resp')
                    for review in reviews:
                        try:
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
                            data["reviews"].append({
                                "name": storeName,
                                "date inserted": ratingDate,
                                "location": storeLoc,
                                "username": reviewerUsername,
                                "review": reviewText,
                                "rating": rating
                            })
                            data["success"] = True # at least on review is crawled
                            reviewCount += 1
                            if reviewCount >= maxNoReviews:
                                break
                        except Exception:  # Just go with the next review
                            pass
                except Exception: # reviews section could not be found
                    pass
            except Exception: # the basic info of the restaurant could not be crawled
                pass
            # Go to next page if exists
            try:
                unModifiedUrl = str(soup.find('a', class_='nav next ui_button primary', href=True)['href'])
                url = 'https://www.tripadvisor.com' + unModifiedUrl
            except:
                reviewCount = maxNoReviews # terminate the loop

        return data

if __name__ == '__main__':
    crawler = TripAdvisorCrawler()
    start = time.time()
    data = crawler.scrapeReviews(
        'https://www.tripadvisor.com.sg/Restaurant_Review-g294265-d3916132-Reviews-Momma_Kong_s-Singapore.html', 10)
    print(data)
    assert(len(data["reviews"])==10)
    print(time.time() - start)
