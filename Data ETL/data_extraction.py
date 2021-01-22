try:
    from kaggle.api.kaggle_api_extended import KaggleApi
except Exception as error:
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
    except ImportError:
        raise ImportError('Kaggle API not properly set up')
        pass
import datetime
import glob
import os
import sys

import pandas as pd

"""
Extracts data from three possible sources:
    1) Lending club API (not in production)
    2) Kaggle API (is very slow)
    3) As a proxy for the other two, a local directory of the data from kaggle
"""


def get_raw_data(call_type='local', source_path="./Data/source/", save_bool=False, raw_path="./Data/raw/",
                 username=None, key=None, api_path=None, kaggle_dataset_name='accepted'):
    if call_type == 'api':
        """ Production implementation should connect to Lending Club API
            # https://www.lendingclub.com/developers/versioning
        """

        print('Starting LC API connection')
        data = pd.DataFrame()
        if data.empty:
            print('DataFrame is empty from LC API!')
        else:
            print(data.head())
            if save_bool:
                save_raw(data, kaggle_dataset_name, raw_path)
            return data

    #   Kaggle data
    elif call_type == 'kaggle':
        print('Starting Kaggle Scraping')
        try:
            if (username is not None) & (key is not None):
                os.environ['KAGGLE_USERNAME'] = username  # assign environment username
                os.environ['KAGGLE_KEY'] = key  # assign environment key from kaggle.com
                api = KaggleApi()  # connect to api
                api.authenticate()  # authenticate
                # get list of files that are in dataset and return the newest "accepted" dataset
                file = get_kaggle_file(api_path, api, kaggle_dataset_name)
                # download accepted dataset VERY SLOW
                api.dataset_download_file(dataset=api_path, file_name=file, path=source_path, force=True)
                # unzip and convert data to pandas
                data = pd.read_csv(source_path + "/" + file, compression='gzip', error_bad_lines=False)
                if data.empty:
                    print("DataFrame is empty!")
                else:
                    print(data.head())
                    if save_bool:
                        # save the untouched raw data in flat file warehouse (currently local directory but could be S3
                        save_raw(data, kaggle_dataset_name, raw_path)
                    return data
            else:
                print("No credentials provided, will try to retrieve from local source")

        except Exception as exe:
            print(sys.stderr, "Unable to access kaggle data")
            print(sys.stderr, "Exception: %s" % str(exe))
            sys.exit(1)

    try:
        print("Retrieving data from Local CSV")
        # access source data from local directory
        list_of_files = glob.glob('./Data/source/*%s*.csv' % kaggle_dataset_name)
        # get newest accepted dataset
        file = max(list_of_files, key=os.path.getctime)
        data = pd.read_csv(file)
        if data.empty:
            print("DataFrame is empty, cannot find any data source")
            sys.exit(1)
        else:
            print(data.head())
            if save_bool:
                save_raw(data, kaggle_dataset_name, raw_path)
            return data
    except Exception as exe:
        print(sys.stderr, "Cannot access raw data. Please check dependencies are installed")
        print(sys.stderr, "Exception: %s" % str(exe))
        sys.exit(1)


def get_kaggle_file(path, a, name):
    # kaggle api returns a list of data objects, each containing the metadata for every dataset on the page
    dataset_info = a.dataset_list_files(path)
    # get the file objects
    dataset_obs = dataset_info.__getattribute__('files')
    file_string = ''
    max_date = datetime.datetime(1900, 1, 1)
    for file in dataset_obs:
        if name in file.__str__():
            # find files with 'accepted' string in name and track the one that was created the most recently
            if file.creationDate > max_date:
                max_date = file.creationDate
                assert isinstance(file.__str__(), object)
                file_string = file.__str__()
    return file_string


def save_raw(data, name, raw_path):
    print("Raw Data Successfully Retrieved")
    print("Saving Raw CSV file in Simple Storage Bucket Warehouse..........")
    data.to_csv(raw_path + '{}_{}.csv'.format(name, datetime.datetime.today().strftime('%y_%m_%d')), index=False)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
