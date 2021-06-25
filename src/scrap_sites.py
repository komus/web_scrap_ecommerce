from modules.web_scrap import scrap_ecommerce_amazon, write_to_csv
from dbfuncs import dml_insert_into_data,dml_fetch_products

data = scrap_ecommerce_amazon(3000, 65, 'dress', 'bracelet','boot')
print(data.shape)
dml_insert_into_data(data)
write_to_csv('amazon_products', dml_fetch_products())