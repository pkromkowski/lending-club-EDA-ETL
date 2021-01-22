import sqlite3
import sys

import pandas as pd

"""
This project uses a sqlite database because it is easy to use and available. Though the dataset is nearly 2.5 million 
rows, sqlite is still able to handle it perfectly. 
"""


def open_conn(database_name, database_path):
    # connect to database, create one if it doesn't already exsist
    try:
        connection = sqlite3.connect(database_path + '%s.db' % database_name, uri=True)
        print("Connection with database established ..........")
    except Exception as e:
        print(sys.stderr, "Cannot connect or create database. Please check dependencies are installed")
        print(sys.stderr, "Exception: %s" % str(e))
        sys.exit(1)
    connection.cursor()
    return connection


# This table making function can be used with other RDB that require schema before data dump
# def make_table(table_dic, schema):
#     table_name = table_dic[schema]
#
#     sub_str = " "
#     for key, value in table_dic['fields'].items():
#         sub_str = sub_str + key + " " + value + ","
#     query = "CREATE TABLE IF NOT EXISTS " + table_name + " (" + sub_str + ", Timestamp TIMESTAMP))"
#     return query


def update_db(dtf, connection, table_dic, logic='append'):
    """
    Upload pandas dataframe to sql database
    """
    print("Updating Database...... ")
    table_name = table_dic['tablename']
    print("Processing database deployment for: ", table_name)
    # create a column of time stamp to know when that data was pulled
    dtf['Timestamp'] = pd.to_datetime("today")
    print(dtf.dtypes)
    # replace the current dataset if there is one
    if logic == 'replace':
        dtf.to_sql(table_name, connection, if_exists='replace')
    else:
        dtf.to_sql(table_name, connection, if_exists='append')
        if logic == 'append':  # append next runs results to the datatable
            pass
        elif logic == 'drop_dup':
            # this feature drops the duplicates by removing all except the first occurance
            fields = list(table_dic['fields'])
            sub_str = fields[0]
            for key in fields[1:]:
                sub_str = sub_str + ", " + key

            query = "DELETE FROM " + table_name + " WHERE ROWID NOT IN (select min(ROWID) from " + table_name + \
                    " GROUP BY " + sub_str + " );"
            print(query)
            connection.execute(query)


def close_conn(connection):
    # close connection to finalize data pushes and table creations
    connection.commit()
    connection.close()
    print("Connection Closed")
    return True
