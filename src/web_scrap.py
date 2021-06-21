import requests
from bs4 import BeautifulSoup
import pandas as pd
import itertools


def scrap_ecommerce(samples_num: int = 10, max_pagination: int = 20,  *args) -> pd.DataFrame:
    """
     A function that scrap ecommerce web and stores information 
     like name, description, images, price, seller etc

     parameter: function accepts:
        number of samples: number of samples to get. default is 10
        
        max_pagination: maximum number of pagination

        keywords: items to search for
    """
    items = []
    for x in args:
        for num in range(1, max_pagination):
            url = f"https://www.amazon.com/s?k={x}&page={num}"
            page_content = get_page_content(url)
            items = itertools.chain(items, page_content)
            if items.count() >= samples_num:
                break


def get_page_content(url):
    data = []
    headers = {
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36 Edg/91.0.864.48',
        'accept': 't	text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-US,en;q=0.9',
    }
    read_site = requests.get(url, headers=headers)
    print(read_site.status_code)
    if read_site.status_code == 200:
        soup = BeautifulSoup(read_site.content, "html.parser")
        for info in soup.find_all(class_="sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col sg-col-4-of-20"):
            ratings = info.find("span", "a-icon-alt")
            review_count = info.find("span", "a-size-base")
            image_link = info.find("img", "s-image").attrs['src']
            data.append(
                {
                    'product_id': info['data-asin'],
                    'name': '',
                    'content_link': info.a['href'],
                    'image_link': image_link,
                    'rating': ratings,
                    'review_counts': review_count
                    # 'Passer Rating':  p.passer_rating()
                })

    print(pd.DataFrame(data).head(1))


get_page_content("https://www.amazon.com/s?k=shoe")