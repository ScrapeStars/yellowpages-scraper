# Yellow Pages Business Details Scraper

This yellowpages.com Web Scraper written in Python and Parsel to scrape business details available based on a particular topic, category and location.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Fields to Extract

This yellow pages scraper can extract the fields below:

1. Rank
2. Business Name
3. Phone Number
4. Business Page
5. Category
6. Website
7. Street name
8. Locality 
9. Region 
10. Zipcode 
11. Listing URL

### Prerequisites

For this web scraping tutorial using Python 3, we will need some packages for downloading and parsing the HTML. 
Below are the package requirements:

 - parsel (installation: pip install parsel)
 - requests (installation: pip install requests)

### Installation

PIP to install the following packages in Python (https://pip.pypa.io/en/stable/installation/) 

Python Requests, to make requests and download the HTML content of the pages (http://docs.python-requests.org/en/master/user/install/)

Python Parsel, for parsing the HTML Tree Structure using XPaths (Learn how to install that here – https://pypi.org/project/parsel/)

All packages can be installed using below command:

```
pip install -r requirements.txt
```

## Running the scraper
We would execute the code with the script name followed by the positional arguments **keyword** and **place**. Here is an example
to find the business details for restaurants in Boston. MA.

```
python3 scrape_yellow_pages.py restaurants Boston,MA
```
## Sample Output

This will create a csv file:

[Sample Output](https://raw.githubusercontent.com/ScrapeStars/yellowpages-scraper/main/restaurants-boston-ma-yellowpages-scraped-data.csv)