from modules.web_scrap import scrap_ecommerce_amazon, write_to_csv


data = scrap_ecommerce_amazon(10, 1, 'shoe', 'sandal')

write_to_csv('test_data', data)