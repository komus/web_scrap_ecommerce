from dbconnection import db_connection

def dml_create_alter_tbl(sql):
    with db_connection.cursor() as curs:
        curs.execute(sql)
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


rows = ddl_fetch("SELECT username FROM account_user LIMIT 10")
for row in rows:
    print(f"user => {row[0]} ")

SQL = """CREATE TABLE IF NOT EXISTS Models (
            id serial PRIMARY KEY, 
            modelname varchar(255) NOT NULL, 
            range int NOT NULL, 
            created_at TIMESTAMP DEFAULT NOW()
);"""
dml_create_alter_tbl(SQL)

SQL = """
        CREATE TABLE IF NOT EXISTS cars(
            id serial PRIMARY KEY,
            ModelId int, 
            PlateNo varchar(15) NOT NULL
        );
        ALTER TABLE cars ADD FOREIGN KEY (ModelId) REFERENCES Models(id);
"""
dml_create_alter_tbl(SQL)

