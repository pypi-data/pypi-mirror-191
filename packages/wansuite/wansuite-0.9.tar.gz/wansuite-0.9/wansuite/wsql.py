
import numpy as np
import pandas as pd
import sqlite3

def newTable(sql,new_table,struct):
    """
    -------------
    Example : struct: "(
       country TEXT,
       indicator TEXT,
       link TEXT,
       netdate TEXT
    )"
    """
    #Connecting to sqlite
    conn = sqlite3.connect(sql)

    cursor = conn.cursor()
   
    sql ='''CREATE TABLE {new_table}'''+struct
    cursor.execute(sql)
    print("Table created successfully........")

    # Commit your changes in the database
    conn.commit()

    #Closing the connection
    conn.close()


def fetchallTables(sql):
    conn = sqlite3.connect(sql)
    # Get all table names
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = cursor.fetchall()
    return table_names

#Print columns names and types of each column for one of sql
def table_col(sql,table):
    conn = sqlite3.connect(sql)
    cursor = conn.cursor()

# Get the names of all columns in the data table
    cursor.execute("PRAGMA table_info("+table+")")
    columns = [row[1] for row in cursor.fetchall()]
    cursor.execute("PRAGMA table_info("+table+")")
    types = [row[2] for row in cursor.fetchall()]
    #print(columns)
    #print(types)

# Close the connection
    conn.close()
    return columns, types

def deleteData(sql,table,condition):
    """
    Parameters
    -------------
    - condition: i.e. "indicator='RetailSalesMoMForecast' and country='us'"
    
    Examples
    -----------------------------
    deleteData(sql,table,c "indicator='RetailSalesMoMForecast' and country='us'"):
    """
    conn = sqlite3.connect(sql)
    cursor = conn.cursor()
    statement="DELETE FROM "+table+" WHERE "+condition

# delete rows where the value in column 'other_column' is less than 10
    cursor.execute(statement)

    conn.commit()
    conn.close()
    
    
def replaceValue(sql, table,col_name,old,new):
    conn = sqlite3.connect(sql)
    cursor = conn.cursor()
    statement="UPDATE "+table+" SET "+col_name+"="+str(new)+" WHERE "+col_name+"="+str(old)
    # Replace the value of column "column_name" in the table "table_name" where the value of column "condition_column" is "condition_value" with "new_value"
    cursor.execute(statement)

    conn.commit()
    conn.close()
    
def readSql(sql,table):
    conn = sqlite3.connect("Forex.db")
    return pd.read_sql_query("SELECT * from %s" % table, conn)
    
def getPossibleValue(sql,table,col):
    conn = sqlite3.connect(sql)
    cursor = conn.cursor()

    cursor.execute(f"SELECT DISTINCT {col} FROM {table}")
    values = cursor.fetchall()
    namelist=[]
    for value in values:
        namelist.append(value[0])
    
    conn.close()
    return namelist

def batchInsert(sql,table,df,col):
    conn=sqlite3.connect(sql)
    cursor=conn.cursor()
    for l in series.index:
        t=str(ppi.loc[l,"Time"])
        d=str(l.date())
        v=ppi.loc[l,"Forecast"]
        cursor.execute(""" 
            INSERT INTO indicators (date, time, country, indicator, value) 
            VALUES(?, ? ,"us","CPICoreYoYForecast",?)""",(d,t,v))
    conn.commit()
    conn.close()