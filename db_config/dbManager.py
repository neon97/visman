# -*- coding: utf-8 -*-
"""

"""
import psycopg2
import pandas as pd
import db_config.config as config
import logging

import os
import psycopg2



logging.basicConfig(level=logging.INFO)

#DATABASE_URL = os.environ['DATABASE_URL']


class dbManager:
    def __init__(self):
        logging.info("Initialing dbManager")
        self._user = config.DATABASE_CONFIG['user']
        self._host = config.DATABASE_CONFIG['host']

        self._nameOfDB = config.DATABASE_CONFIG['database']
        self._port = config.DATABASE_CONFIG['port']
        self._url = config.DATABASE_CONFIG['url']

        self._connection = None
        self._DFSQLmap = {}
        self._DFSQLmap['object'] = 'varchar(Max)'
        self._DFSQLmap['int64'] = 'integer'
        self._DFSQLmap['float64'] = 'float'
        self._DFSQLmap['datetime64[ns]'] = 'varchar(Max)'
        self._DFSQLmap['bool'] = 'BIT'
        self._connect()

    def getDBName(self):
        self._nameOfDB = config.DATABASE_CONFIG['database']
        return self._nameOfDB

    def getDataFrame(self, query):
        logging.info('Running query : %s ', query)
        df = pd.read_sql(query, self._connection)
        return df

    def callprocedure(self, func, args):
        logging.info('Running function : %s with args - %s', func, args)
        cur = self._connection.cursor()
        cur.callproc(func, args)

        colnames = [desc[0] for desc in cur.description]
        logging.info(' Columns on Function %s returned %s ', func, colnames)
        value = cur.fetchall()
        logging.info(' Columns on Function %s returned %s ', func, value)
        self._connection.commit()

        return value

    def updateDB(self, query):
        cur = self._connection.cursor()
        logging.info('Connection to database established')
        logging.info('Executing query %s', query)
        cur.execute(query)
        self._connection.commit()
        return True
        logging.info('Update Commit done')
    
    def runSQL(self, query):
        cur = self._connection.cursor()
        logging.info('Connection to database established')
        logging.info('Executing query %s', query)
        cur.execute(query)
        self._connection.commit()
        return True
        logging.info('Query ran Successfully')

    def truncateDB(self, tableName):
        print('Dropping table: ' + tableName)
        if self.__isTableExists(tableName):
            delQuery = "DROP TABLE " + tableName
            cur = self._connection.cursor()
            cur.execute(delQuery)
            cur.commit()

    def commit(self, df, tableName):
        tableNames = self.__columnNamesOfSQLTable(tableName)
        csr = self._connection.cursor()
        for rw in df.iterrows():
            cols, vals = self.__getinsertValues(rw, df.columns)

            iquery = "insert into {}{} values {}".format(tableName, cols, vals.replace("Primary's", "Primary''s"))
            logging.info('Running query : %s ', iquery)
            try:
                csr.execute(iquery)
                self._connection.commit()
                logging.info('Query ran successfully ')
            except psycopg2.Error as error:
                print(error)
                continue

        return tableNames

    def _connect(self):
        logging.info('Running _connect')
        logging.info('Initailizing db connection')
        if (self._connection != None):
            return

        # connect to the PostgreSQL server
        #self._nameOfDB = config.DATABASE_CONFIG['database']
        try:


            self._connection = psycopg2.connect(user=self._user,
                                                host=self._host,
                                                database=self._nameOfDB,
                                                password=config.DATABASE_CONFIG['password'],
                                                port=self._port)
            # self._connection = psycopg2.connect(self._url, sslmode='require')

            logging.info('Connection to Database %s : %s : %s  Successfull', self._user, self._nameOfDB, self._port)

        except psycopg2.DatabaseError as error:
            errors = {'visitor_entry': False,
                      'error': (error)
                      }
            logging.debug(errors)

    def _disconnect(self):
        # print("Disconnect to DB")
        if (self._connection == None):
            return

        self._connection.close()
        self._connection = None

    def __isTableExists(self, tableName):
        cursor = self._connection.cursor()
        if cursor.tables(table=tableName, tableType='TABLE').fetchone():
            return True
        return False

    def isTableExists(self, tableName):
        cursor = self._connection.cursor()
        if cursor.tables(table=tableName, tableType='TABLE').fetchone():
            return True
        return False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._disconnect()
        print('connection closed')

    def __columnNamesOfSQLTable(self, tableName):
        cur = self._connection.cursor()
        query = "SELECT COLUMN_NAME from INFORMATION_SCHEMA.COLUMNS where TABLE_NAME = N'{}'".format(tableName)
        cur.execute(query)
        rows = cur.fetchall()
        lstRowsInDbTable = []
        for r in rows:
            lstRowsInDbTable.append(r[0])
        return lstRowsInDbTable

    def __getSQLTableNameFromDF(self, tableName, df):

        params = ""
        for col, dtype in zip(df.columns, df.dtypes):
            print(col, dtype)
            params = params + col + " " + self._DFSQLmap[str(dtype)] + ","
        params = params[:-1]
        # tbname = tableName + "(" + "ID INT IDENTITY(1,1) PRIMARY KEY," + params + ")"
        tbname = tableName + "(" + params + ")"

        return tbname

    def __getinsertValues(self, row, columns):
        colnStr = ""
        rowstr = ""
        for coln in columns:
            colnStr = colnStr + coln + ","
            strData = str(row[1][coln])
            rowstr = rowstr + "'" + strData + "'" + ","

        colnStr = "(" + colnStr[:-1] + ")"
        rowstr = "(" + rowstr[:-1] + ")"
        return colnStr, rowstr

