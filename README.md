# Web Scraping of Ecommerce Sites - Amazon
This project is to scrap ecommerce site and use the information to populate database.
case study - Amazon.com

## Background Issues
1. Amazon Scraping Blockage: Due to cross-site origin, scraping amazon site might return empty page. To resolve this, user agent needs to be inputted. 
Even with user agent, some pages might not return result
```python
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
```
You can get your user-agent from [here][https://www.whatismybrowser.com/detect/what-is-my-user-agent]

2. Amazon several design template: Amazon has designs per search product category and localized country. For this reason, the search site with grid 4 x 12 is used for scraping.
The template url is `f"https://www.amazon.com/s?k={x}&page={num}"`

3. For security reasons, postgres database information is saved in `.env` file.
```python
 db_connection = psycopg2.connect(
        database=os.getenv("DATABASE"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        host=os.getenv("HOST"),
        port=os.getenv("PORT")
    )
```
#Usage
1. Table Creation
Tables can be created for storage of scraped data by calling function `ddl_create_tables()` in `dbfuncs`
   
2. Site Scraping
Multiple keywords can be scraped using `scrap_ecommerce_amazon` or a single search item `get_page_content`
   
#Sample Code
```python
from modules.web_scrap import scrap_ecommerce_amazon, write_to_csv
#Scrap site for keyword
data = scrap_ecommerce_amazon(3000, 65, 'dress', 'bracelet','boot')
#insert data into created database
dml_insert_into_data(data)
#Write product to csv file
write_to_csv('amazon_products', dml_fetch_products())
```