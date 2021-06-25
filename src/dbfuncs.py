import pandas as pd
import psycopg2
from modules.dbconnection import db_connection
import psycopg2.extras as extras


def ddl_create_tables():
    with db_connection.cursor() as curs:
        curs.execute('''CREATE TABLE IF NOT EXISTS category(
                        category_id  serial PRIMARY KEY,
                        category varchar(30) NOT NULL
                    );
               
                    CREATE TABLE IF NOT EXISTS amazon_scrap_product(
                        ID serial PRIMARY KEY,
                        Product_id varchar(25) NOT NULL, 
                        Category_id INT,
                        name varchar(255) NOT NULL,
                        content_link varchar(255),
                        image_link varchar(255),
                        rating varchar(20),
                        rating_counts varchar(20),
                        original_price varchar(25),
                        price varchar(25),
                        coupon varchar(50),
                        txtdate TIMESTAMP DEFAULT NOW()
                        
                );
                ALTER TABLE amazon_scrap_product ADD FOREIGN KEY (Category_id) REFERENCES category(category_id) ON UPDATE CASCADE ON DELETE CASCADE;
                ''')
        db_connection.commit()
        db_connection.close()


def ddl_create_sp_insert_product():
    with db_connection.cursor() as curs:
        curs.execute(''' 
                    CREATE OR REPLACE PROCEDURE add_product(
                        p_category_name  varchar(30),
                        p_productid   varchar(25),
                        p_name  varchar(255),
                        p_link  varchar(255),
                        p_image  varchar(255),
                        p_ratings  varchar(20),
                        p_rating_count  varchar(20),
                        p_original_price  varchar(25),
                        p_price  varchar(25),
                        p_coupon varchar(50)
            )
                LANGUAGE 'plpgsql'
            AS $BODY$
                    DECLARE 
                        _cat_id integer;
                    
                    BEGIN
                        _cat_id := (select category_id from category where category = p_category_name);
                                            
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


def dml_insert_into_data(data: pd.DataFrame) -> None:
    print(len(data))
    query = '''INSERT INTO amazon_scrap_product (product_id, category_id, name, content_link, image_link, rating, rating_counts, original_price, price, coupon) VALUES %s'''
    tuples = [tuple(x) for x in data.to_numpy()]
    with db_connection.cursor() as curs:
        try:
            extras.execute_values(curs, query, tuples)
            db_connection.commit()
        except (Exception,  psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            db_connection.rollback()
            curs.close()
    print("insertion done")


def dml_insert_category(category: str) -> None:
    query = f'''INSERT INTO category(category) VALUES('{category}') RETURNING category_id;'''
    with db_connection.cursor() as curs:
        curs.execute(query)
        db_connection.commit()
        val = curs.fetchone()[0]
    return val


def dml_fetch_products() -> pd.DataFrame:
    query = '''select asp.product_id, c.category, asp."name", asp.content_link, asp.image_link, asp.rating, asp.rating_counts, asp.original_price, asp.price, asp.coupon
                from amazon_scrap_product asp
                join category c on asp.category_id = c.category_id '''
    with db_connection.cursor() as curs:
        curs.execute(query)
        values = curs.fetchall()
    return pd.DataFrame(values)


