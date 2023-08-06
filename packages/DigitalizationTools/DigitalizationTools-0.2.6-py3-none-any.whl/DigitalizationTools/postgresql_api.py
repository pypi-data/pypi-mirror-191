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
        """
        keys: column names ["name1", "name2", ...]
        datatype: type of columns ["text", "float", ...]
        """
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
        """
        if with_id = True, 'id' should be the last element in 'insert_data'
        """
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
    
    @beartype
    def insert_multiple_rows(self, insert_df:pd.DataFrame): 
        """
        insert_data: list of lists, e.g.: [[1,2,3], [1,2,3]]
        """
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
            
            id                 = secrets.token_hex(16)
            date               = str(datetime.now())[0:19]
            len_of_df          = len(insert_df)
            insert_df["id"]    = [id for i in range(len_of_df)]
            insert_df["date"]  = [date for i in range(len_of_df)]

            sql_insert_data = []
            for i in range(len(insert_df)):
                sql_insert_data.append(tuple(insert_df.iloc[i].to_list()))

            cur.executemany(insert, sql_insert_data)
            conn.commit()
            conn.close()
            return True
        except psycopg2.Error as err:
            return err
    
    def get_all(self):
        """
        get all rows in table
        """
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
        """
        get one row based on id
        """
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
        """
        get all columns based on the given column names,
        columnNames = ["name1", "name2", ...]
        """
        if columnNames == []:
            return "No column specified"
        try:
            df = self.get_all()
            return df.loc[:, columnNames]
        except psycopg2.Error as err:
            return err
    
    @beartype
    def delete_one_row(self, id:str):
        """
        delete one row from table
        """
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
        """
        update the whole row in table
        """
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
    
    @beartype
    def update_elements(self, id:str, update_dict=dict):
        """
        update_dict = {"text": text, "list": [1,2,3] }
        """
        keys    = tuple(update_dict.keys())
        values  = tuple(update_dict.values()) 
        try:
            # get all ids in table
            df = self.get_columns(["id"])
            if id not in df["id"].to_list():
                return "id does not exist..."
            if len(values) > 1:
                keys_s  = f"{keys}".replace("'", '')
                sql = f"""UPDATE {self.tableName} SET {keys_s} = {values} WHERE id = '{id}';"""
            else:

                sql = f"""UPDATE {self.tableName} SET {keys[0]} = '{values[0]}' WHERE id = '{id}';"""

            conn = psycopg2.connect(host=self.hostName,database=self.databaseName,user=self.userName, password=self.sqlPasswords)
            cur = conn.cursor()
            
            cur.execute(sql)
            conn.commit()
            conn.close()
            return True
        except psycopg2.Error as err:
            return err
        

    def delete_all_rows(self):
        """
        delete all rows from table
        """
        try:
            conn = psycopg2.connect(host=self.hostName,database=self.databaseName,user=self.userName, password=self.sqlPasswords)
            cur = conn.cursor()
            sql_delete = 'DELETE FROM {};'.format(self.tableName)
            cur.execute(sql_delete)  
            conn.commit()
            conn.close()
            return True
        except psycopg2.Error as err:
            return err