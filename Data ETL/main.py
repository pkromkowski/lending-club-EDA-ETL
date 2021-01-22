#import packages
import argparse
import os
import time
import schedule
import yaml

#import modules
from data_extraction import get_raw_data
from data_transformation import format_columns, create_columns, save_split_data
from manage_db import open_conn, update_db, close_conn

# accept configurations specifics on pipeline start up
parser = argparse.ArgumentParser()
parser.add_argument("--yamlpath", default='config.yaml',
                    help="Location for yaml file if not in current working directory")
parser.add_argument("--kaggleuser", default=None, help="Username for kaggle access")
parser.add_argument("--kagglepw", default=None, help="kagglepw")
parser.add_argument("--demo", default="ON", help="If pipeline is in demo mode, the scheduler will not kick off")
args = parser.parse_args()

#read in full config file
with open(os.path.join(args.yamlpath)) as file:
    pipe_info = yaml.full_load(file)


#start the data pipeline process
def start_etl():
    #Export
    returned_connection = open_conn(database_name=pipe_info['database']['name'],
                                    database_path=pipe_info['dataload']['databasepath'])
    dt = get_raw_data(call_type='local', api_path=pipe_info['datapull']['source']['local']['apipath'],
                      source_path=pipe_info['datapull']['general']['sourcepath'],
                      kaggle_dataset_name=pipe_info['datapull']['general']['rawname'],
                      save_bool=pipe_info['datapull']['general']['save_raw'])
    #Transform
    dt = format_columns(dt)
    dt = create_columns(dt)
    df_1, df_2 = save_split_data(dt, pipe_info['datatransform']['cleanname'], pipe_info['datatransform']['cleanpath'])

    #Load
    update_db(df_1, connection=returned_connection, table_dic=pipe_info['database']['schemas']['lc_main_20'],
              logic=pipe_info['dataload']['logic'])

    update_db(df_2, connection=returned_connection, table_dic=pipe_info['database']['schemas']['lc_sec_20'],
              logic=pipe_info['dataload']['logic'])

    print("Uploading Complete")
    close_conn(returned_connection)


if args.demo == "OFF":
    # schedule new data pulls ever sunday at 11pm to be ready before Monday morning.
    schedule.every().sunday.at("23:00").do(start_etl)
    schedule.run_pending()
    time.sleep(60)
elif args.demo == "ON":
    start_etl()
