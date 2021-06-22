from modules.dbfuncs import dml_create_alter_drop_tbl, dml_insert, ddl_fetch
create_table = ('''
                    CREATE IF NOT EXISTS category(
                        category_id  serial PRIMARY KEY,
                        category varchar(30) NOT NULL
                    );
                ''',
                '''
                    CREATE IF NOT EXISTS amazon_scrap_product(
                        ID serial PRIMARY KEY,
                        Product_id varchar(25) UNIQUE NOT NULL, 
                        Category_id INT,
                        name varchar(255) NOT NULL,
                        content_link varchar(255),
                        image_link varchar(255),
                        rating varchar(20),
                        rating_counts INTEGER,
                        original_price MONEY,
                        price MONEY,
                        coupon varchar(50),
                        txtdate TIMESTAMP DEFAULT NOW(),
                        FOREIGN KEY (Category_id) REFERENCES category(category_id) ON UPDATE CASCADE ON DELETE CASCADE
                );
                ''')

drop_table_product = '''
                DROP TABLE IF EXISTS product;
                '''
drop_table_category = '''DROP TABLE IF EXISTS category;'''


def create_amazon_table():
    dml_create_alter_drop_tbl(create_table)


def drop_amazon_table():
    pass