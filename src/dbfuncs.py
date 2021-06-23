from modules.dbconnection import db_connection


def dml_create_tables():
    with db_connection.cursor() as curs:
        curs.execute('''CREATE TABLE IF NOT EXISTS category(
                        category_id  serial PRIMARY KEY,
                        category varchar(30) NOT NULL
                    );
               
                    CREATE TABLE IF NOT EXISTS amazon_scrap_product(
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
                        txtdate TIMESTAMP DEFAULT NOW()
                        
                );
                ALTER TABLE amazon_scrap_product ADD FOREIGN KEY (Category_id) REFERENCES category(category_id) ON UPDATE CASCADE ON DELETE CASCADE;
                ''')
        db_connection.commit()


def dml_create_sp_insert_product():
    with db_connection.cursor() as curs:
        curs.execute(''' 
                    CREATE OR REPLACE PROCEDURE add_product(
                        p_category_name  varchar(30),
                        p_productid   varchar(25),
                        p_name  varchar(255),
                        p_link  varchar(255),
                        p_image  varchar(255),
                        p_ratings  varchar(20),
                        p_rating_count  integer,
                        p_original_price  money,
                        p_price  money,
                        p_coupon varchar(50)
            )
                LANGUAGE 'plpgsql'
            AS $BODY$
                    DECLARE 
                        _cat_id integer;
                    
                    BEGIN
                        _cat_id := (select category_id from category where category = category_name);
                                            
                        insert into amazon_scrap_product (product_id, name, content_link, image_link, rating, rating_counts, original_price, price, coupon)
                        VALUES(p_productid,  p_name, p_link, p_image, p_ratings, p_rating_count, p_original_price, p_price, p_coupon );
                    end;
            
            $BODY$;
            
             ''')
        db_connection.commit()


def ddl_drop_tbl_category_product():
    with db_connection.cursor() as curs:
        curs.execute('''
                    DROP TABLE IF EXISTS amazon_scrap_product;
                    DROP TABLE IF EXISTS category;
                    DROP PROCEDURE IF EXISTS add_product
                    ''')
        db_connection.commit()


def dml_insert(sql):
    with db_connection.cursor() as curs:
        curs.execute(sql)
        db_connection.commit()
        return curs.statusmessage


def ddl_fetch(sql):
    with db_connection.cursor() as curs:
        curs.execute(sql)
        return curs.fetchall()


ddl_drop_tbl_category_product()
dml_create_tables()
dml_create_sp_insert_product()