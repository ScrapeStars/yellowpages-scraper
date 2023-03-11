import requests
from parsel import Selector
import time
import random
import csv
from slugify import slugify


class ScrapeYellowPages(object):
    """
    Scrape yellow pages listings
    """
    def __init__(self, keyword, place):
        """
        Object to scrape yellow pages listings using search query and place name
        : param keyword: search query
        : param place : place name
        """
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.yellowpages.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
        }
        self.url = f"https://www.yellowpages.com/search?search_terms={keyword}&geo_location_terms={place}"
        self.XPATH_LISTINGS = "//div[contains(@class, 'search-results organic')]/div[contains(@class, 'result')]"
        self.base_url = "https://www.yellowpages.com"
        print("retrieving ", self.url)

    # Parsing yellow page listings
    def parse_listings(self):
        try:
            print("Started Scraping")
            time.sleep(random.randint(2, 5))
            response = requests.get(url=self.url, headers=self.headers)
            if response.status_code == 200:
                selector = Selector(text=response.text)
                listings = selector.xpath(self.XPATH_LISTINGS)
                scraped_results = []
                for result in listings:
                    XPATH_BUSINESS_RANK = ".//h2[contains(@class, 'n')]/text()"
                    XPATH_BUSINESS_NAME = ".//a[contains(@class, 'business-name')]/span//text()"
                    XPATH_BUSINESS_TELEPHONE = ".//div[@class='phones phone primary']//text()"
                    XPATH_BUSINESS_PAGE = ".//a[@class='business-name']//@href"
                    XPATH_BUSINESS_CATEGORIES = ".//div[contains(@class, 'categories')]/a//text()"
                    XPATH_BUSINESS_WEBSITE = ".//a[contains(@class, 'track-visit-website')]//@href"
                    XPATH_STREET_ADDRESS = ".//div[contains(@class, 'street-address')]//text()"
                    XPATH_BUSINESS_LOCALITY = ".//div[contains(@class, 'locality')]//text()"

                    raw_business_rank = result.xpath(XPATH_BUSINESS_RANK)
                    raw_business_name = result.xpath(XPATH_BUSINESS_NAME)
                    raw_business_telephone = result.xpath(XPATH_BUSINESS_TELEPHONE)
                    raw_business_page = result.xpath(XPATH_BUSINESS_PAGE)
                    raw_business_categories = result.xpath(XPATH_BUSINESS_CATEGORIES).getall()
                    raw_business_website = result.xpath(XPATH_BUSINESS_WEBSITE)
                    raw_street_address = result.xpath(XPATH_STREET_ADDRESS)
                    raw_business_locality = result.xpath(XPATH_BUSINESS_LOCALITY)

                    business_rank = str(raw_business_rank.get()).strip() if raw_business_rank else None
                    business_name = str(raw_business_name.get()).strip() if raw_business_name else None
                    business_phone = str(raw_business_telephone.get()).strip() if raw_business_telephone else None
                    business_page = str(raw_business_page.get()).strip() if raw_business_page else None
                    business_page = self.base_url + business_page
                    business_website = str(raw_business_website.get()).strip() if raw_business_website else None
                    business_categories = ", ".join(raw_business_categories)
                    street_address = str(raw_street_address.get()).strip() if raw_street_address else None
                    locality = str(raw_business_locality.get()).strip() if raw_business_locality else None
                    locality, locality_list = locality.split(',')
                    _, region, zipcode = locality_list.split(' ')

                    business_details = {
                        "rank": business_rank,
                        "business_name": business_name,
                        "telephone": business_phone,
                        "business_page": business_page,
                        "category": business_categories,
                        "website": business_website,
                        "street_address": street_address,
                        "region": region,
                        "zipcode": zipcode,
                        "listing_url": response.url
                    }
                    scraped_results.append(business_details)
                return scraped_results
            else:
                pass
        except Exception as e:
            print("Failed to process page", e)
            return []

    def __str__(self):
        return self.url


if __name__ == '__main__':
    keyword = 'restaurants'
    place = 'Boston%2C+MA'
    scrape_yellow_pages = ScrapeYellowPages(keyword=keyword, place=place)
    scraped_data = scrape_yellow_pages.parse_listings()
    if scraped_data:
        print("Writing scraped data to %s-%s-yellowpages-scraped-data.csv" % (slugify(keyword), slugify(place)))
        with open('%s-%s-yellowpages-scraped-data.csv' % (slugify(keyword), slugify(place)), 'w') as csvfile:
            fieldnames = [
                'rank',
                'business_name',
                'telephone',
                'business_page',
                'category',
                'website',
                'street_address',
                'region',
                'zipcode',
                'listing_url',
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for data in scraped_data:
                writer.writerow(data)
        print("Finish writing!")
    else:
        print("No data scraped!")
