import psycopg2
from datetime import datetime
import secrets
import pandas as pd
from beartype import beartype
from typing import Optional, Union


# sql_pass = "g5XSmIEJesgmR9uKvhdD"


class database:
    @beartype
    def __init__(self, hostName:str, databaseName:str, userName:str, sqlPasswords:str):
        self.hostName     = hostName
        self.databaseName = databaseName
        self.userName     = userName
        self.sqlPasswords = sqlPasswords
    
    def get_table(self):
        try:
            conn = psycopg2.connect(host=self.hostName,database=self.databaseName,user=self.userName, password=self.sqlPasswords)
            cur = conn.cursor()
            cur.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';")
            tables = cur.fetchall()
            columnsName = [i[0] for i in cur.description]
            conn.commit()
            conn.close()
            df_tables = pd.DataFrame(tables, columns=columnsName)
            return df_tables
        except psycopg2.Error as err:
            return err


class databaseTable(database):
    
    @beartype
    def __init__(self, hostName:str, databaseName:str, userName:str, sqlPasswords:str, tableName:str):
        super().__init__(hostName, databaseName, userName, sqlPasswords)
        self.tableName  = tableName
    
    @beartype
    def create_table(self, keys:list, datatype:list):
        try:
            conn = psycopg2.connect(host=self.hostName,database=self.databaseName,user=self.userName, password=self.sqlPasswords)
            cur = conn.cursor()
            # create table
            create_table_sql = "CREATE TABLE IF NOT EXISTS {} ".format(self.tableName)
            keys_datatype = [f"{keys[i]} {datatype[i]}," for i in range(len(keys))]
            create_table_sql = create_table_sql + \
                                "({} id text, date text);".format("".join(keys_datatype))
            cur.execute(create_table_sql)
            conn.commit()
            conn.close()
            self.keys = keys
            self.datatype = datatype
            return True
        except psycopg2.Error as err:
            return err
    
    @beartype
    def insert_one_row(self, insert_data:list, with_id:Optional[bool]=False):
        try:
            conn = psycopg2.connect(host=self.hostName,database=self.databaseName,user=self.userName, password=self.sqlPasswords)
            cur  = conn.cursor()        
            sql = "SELECT * FROM {};".format(self.tableName)
            cur.execute(sql)
            keys = [i[0] for i in cur.description][0:-2]
            # insert data
            qs = ",".join(["%s" for _ in range(len(keys)+2)])
            insert = """INSERT INTO {} ({},id,date) 
                    VALUES ({})""".format(self.tableName, ",".join(keys), qs)
            # check if id is specified
            if with_id: # true
                insert_data.append(str(datetime.now())[0:19])
            else: # false, no id specified
                insert_data.append(secrets.token_hex(16))
                insert_data.append(str(datetime.now())[0:19])
            cur.execute(insert, tuple(insert_data))
            conn.commit()
            conn.close()
            return True
        except psycopg2.Error as err:
            return err
    
    def get_all(self):
        try:
            conn = psycopg2.connect(host=self.hostName,database=self.databaseName,user=self.userName, password=self.sqlPasswords)
            cur = conn.cursor()
            sql = "SELECT * FROM {};".format(self.tableName)
            cur.execute(sql)
            # get all rows
            rows = cur.fetchall()
            # keys
            columnsName = [i[0] for i in cur.description]
            conn.commit()
            conn.close()
            return pd.DataFrame(rows, columns=columnsName)
        except psycopg2.Error as err:
            return err
    
    @beartype
    def get_one_row(self, id:str):
        try:
            conn = psycopg2.connect(host=self.hostName,database=self.databaseName,user=self.userName, password=self.sqlPasswords)
            cur = conn.cursor()
            sql_select = "SELECT * FROM {} WHERE id=%s".format(self.tableName)
            cur.execute(sql_select, (id,))
            rows = cur.fetchone()
            columnsName = [i[0] for i in cur.description]
            conn.commit()
            conn.close()
            return pd.DataFrame([rows], columns=columnsName)
        except psycopg2.Error as err:
            return err

    @beartype
    def get_columns(self, columnNames:list):
        if columnNames == []:
            return "No column specified"
        try:
            df = self.get_all()
            return df.loc[:, columnNames]
        except psycopg2.Error as err:
            return err
    
    @beartype
    def delete_one_row(self, id:str):
        try:
            conn = psycopg2.connect(host=self.hostName,database=self.databaseName,user=self.userName, password=self.sqlPasswords)
            cur = conn.cursor()
            sql_delete = 'DELETE FROM {} WHERE id=%s'.format(self.tableName)
            cur.execute(sql_delete, (id,))  
            conn.commit()
            conn.close()
            return True
        except psycopg2.Error as err:
            return err
    
    @beartype
    def update_one_row(self, id:str, update_data:list):
        try:
            df = self.get_columns(["id"])
            if id in df["id"].to_list():
                # delete
                self.delete_one_row(id)
                # insert
                update_data.append(id)
                self.insert_one_row(insert_data=update_data, with_id=True)
                return True
            else:
                return "no id matching."
        except psycopg2.Error as err:
            return err