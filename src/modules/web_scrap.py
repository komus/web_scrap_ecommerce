import requests
from bs4 import BeautifulSoup
import pandas as pd
from typing import List
from dbfuncs import dml_insert_category

def scrap_ecommerce_amazon(samples_num: int = 10,  max_pagination: int = 20,  *args) -> pd.DataFrame:
    """
     A function that scrap ecommerce web and stores information 
     like name, price, image etc. This function is for multiple keywords scraping

     parameter: function accepts:
        number of samples: number of samples to get for each keyword. default is 10

        max_pagination: maximum number of pagination of the site

        keywords: items to search for
    """
    items = []
    total_count = len(args)*samples_num
    for x in args:
        val = dml_insert_category(x)
        for num in range(0, max_pagination):
            url = f"https://www.amazon.com/s?k={x}&page={num}"
            page_content = get_page_content(url, samples_num, val)
            for y in range(len(page_content)):
                items.append(page_content[y])
            if len(items) >= total_count:
                break

    return pd.DataFrame(items)


def get_page_content(url: str, samples_num: int, category: int) -> List:
    """
         A function that scrap ecommerce web and stores information
         like name, price, image etc. This function is for multiple keywords scraping

         parameter: function accepts:
            url: The url of amazon search page to be scraped

            number of samples: number of samples to get from the url

            category: the category of the searched product

        """
    data = []
    headers = {
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.54',
        'accept': 't	text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-US,en;q=0.9',
    }
    read_site = requests.get(url, headers=headers)
    if read_site.status_code == 200:
        soup = BeautifulSoup(read_site.content, "html.parser")
        for info in soup.find_all(class_="sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col sg-col-4-of-20"):
            rating = info.find_all("span", "a-icon-alt")
            if len(rating) == 1:
                ratings = rating[0].text
            else:
                ratings = None
            review_counts = info.find_all("span", "a-size-base")
            if len(review_counts) == 1:
                review_count = review_counts[0].text
            else:
                review_count = None
            coupons = info.find_all("span", "a-size-base s-highlighted-text-padding aok-inline-block s-coupon-highlight-color")
            if len(coupons) == 1:
                coupon = coupons[0].text
            else:
                coupon = None
            all_price = info.find_all("span", "a-offscreen")
            original_price = 0
            if len(all_price) == 2:
                price = all_price[0].text
                original_price = all_price[1].text

            elif len(all_price) == 1:
                price = all_price[0].text
            else:
                price = 0

            image_link = info.find("img", "s-image").attrs['src']
            data.append(
                {
                    'product_id': info['data-asin'],
                    'category': category,
                    'name': info.find("span", "a-size-base-plus a-color-base a-text-normal").text,
                    'content_link': info.a['href'],
                    'image_link': image_link,
                    'rating': ratings,
                    'review_counts': review_count,
                    'original_price': original_price,
                    'price': price,
                    'coupon': coupon,
                })

            if len(data) >= samples_num:
                break
    return data


def write_to_csv(filename: str, data: pd.DataFrame) -> None:
    filename = filename + '.csv'
    data.to_csv(filename)
