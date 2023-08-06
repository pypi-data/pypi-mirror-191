import pandas as pd
from datetime import datetime
import logging
import os
import shutil
import urllib.request
from datetime import datetime
import configparser
import re
import requests
import hashlib
import os



def get_csv_location():
    config = configparser.ConfigParser()
    config.read('configure.ini')
    file_name = config.get('DEFAULT','filenamme')
    output_dir = config.get('DEFAULT','output_dir')
    return file_name, output_dir


def download_spreadsheet_to_df_if_updated(url, local_file_path):
    # Get the current version of the file from the URL
    response = requests.get(url)
    remote_file_contents = response.content
    logging.info('downloading dataset from gov website')
    # Calculate the hash of the remote file contents
    remote_file_hash = hashlib.sha256(remote_file_contents).hexdigest()
    logging.info('checking if local file exists')
    # Check if the local file exists
    if os.path.exists(local_file_path):
        # Calculate the hash of the local file contents
        with open(local_file_path, 'rb') as f:
            logging.info('local file exists')
            local_file_contents = f.read()
        local_file_hash = hashlib.sha256(local_file_contents).hexdigest()
        
        # Compare the hashes
        logging.info('checking to see if remote file has been updated')
        if remote_file_hash == local_file_hash:
            # The file has not been updated, load the local file into a dataframe
            logging.info('local file is the same as remote file')
            df = pd.read_excel(local_file_path)
            return df, False
        else:
            logging.info('remote file has been updated, initiate rest of workflow')
            # The file has been updated, download the updated version and load it into a dataframe
            with open(local_file_path, 'wb') as f:
                f.write(remote_file_contents)
            df = pd.read_excel(local_file_path)
            return df, True
    else:
        # The local file does not exist, download the remote file and load it into a dataframe
        logging.info('local file does not exists, it is probably the first time running this code, downloading raw data now')
        with open(local_file_path, 'wb') as f:
            f.write(remote_file_contents)
        df = pd.read_excel(local_file_path)
        return df, True


def check_for_updates():
  logging.info('Checking for any updated data')
  url = "https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1126335/ET_3.1_DEC_22.xlsx"
  file_name, output_dir = get_csv_location()
  # Read the spreadsheet using pandas
  downloaded_dataset = pd.read_excel(url, sheet_name="Quarter", skiprows = 4)
  try:
    existing_dataset = pd.read_csv(f'{output_dir}/{file_name}')
    if downloaded_dataset.equals(existing_dataset):
      logging.info('The dataset that we are interested in has not been changed')
      del downloaded_dataset
    else:
      print("The two Excel files do not contain the same data.")
      return downloaded_dataset
  except FileNotFoundError:
    logging.info('file not found, this must be the first run... moving on')
  return downloaded_dataset


def _clean_data(df):
  df.replace(to_replace = 0, value = '', inplace=True)
  return df

def _remove_brackets(df):
    for col in df.columns:
        df[col] = df[col].apply(lambda x: re.sub(r'[\{\}\[\]\(\)"]', '', str(x)))
    return df

def _to_datetime(string):
    parts = string.split("\n")
    if len(parts) == 1:
        parts = string.split()
    year = int(parts[0])
    quarter = parts[1].split()[0].rstrip("stndrdth")
    quarter = int(quarter)
    quarter_map = {
        1: 1,
        2: 4,
        3: 7,
        4: 10
    }
    month = quarter_map[quarter]
    return "{}-{:02d}-01".format(year, month)

def _rename_columns(df):
    columns = df.columns[1:]
    rename_dict = {}
    for col in columns:
        if col != df.columns[0]:
            rename_dict[col] = _to_datetime(col)
    df.rename(columns=rename_dict, inplace=True)
    return df
    
def preprocess_df(df):
    removed_0 = _clean_data(df)
    removed_brackets = _remove_brackets(removed_0)
    change_date_format = _rename_columns(removed_brackets)
    return change_date_format

def summarize_data(data):
    df = data
    row_count = df.shape[0]
    col_count = df.shape[1]
    num_cols = df._get_numeric_data().columns
    statistics = []
    for col in num_cols:
        statistics.append([col, df[col].min(), df[col].max(), df[col].median(), df[col].mean()])
    missing_values = df.isnull().sum().sum()
    result_df = pd.DataFrame({"Row Count": [row_count], 
                             "Column Count": [col_count], 
                             "Missing Values": [missing_values]})
    statistics_df = pd.DataFrame(statistics, columns=["Column", "Min", "Max", "Median", "Mean"])
    combined_df = pd.concat([result_df, statistics_df], axis=0)
    file_name, output_dir = get_csv_location()
    save_df_as_csv(combined_df,folder_path=output_dir, file_name='clean_data_data_profiling')
    return combined_df

def save_df_as_csv(df, folder_path, file_name):
    file_path = folder_path + '/' + file_name
    df.to_csv(file_path, index=False)

def main(url, local_path):
    logging.info('started')
    data, decision= download_spreadsheet_to_df_if_updated(url, local_path)
    if decision is True:
        data = preprocess_df(data)
        now = datetime.now() # current date and time
        date_time = now.strftime("%m_%d_%Y")
        file_name, output_dir=get_csv_location()
        save_df_as_csv(data, folder_path=output_dir,file_name=f'{file_name}_{date_time}.csv')
        summarize_data(data)
    return data



