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

def ddl_create_stored_procedure(sql):
    pass



