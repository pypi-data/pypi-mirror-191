import logging
import pandas as pd
import requests
import os
import hashlib
import configparser
import pandas as pd
import os
import datetime



class CSVFileHandler:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('configure.ini')
        self.directory = self.config['DEFAULT']['output_dir']

    def get_last_uploaded(self):
        csv_files = [f for f in os.listdir(self.directory) if f.endswith('.csv')]
        if csv_files:
            csv_files.sort(key=lambda x: os.path.getmtime(os.path.join(self.directory, x)))
            last_uploaded = csv_files[-1]
            file_path = os.path.join(self.directory, last_uploaded)
            logging.info(f'this is the file path {file_path}')
            df = pd.read_csv('/Users/jedmundson/clean_data_2023-02-12_09-21-43.csv')
            return df
        else:
            raise FileNotFoundError(f"No CSV files found in directory '{self.directory}'")

class CsvLocation:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('configure.ini')
        self.file_name = self.config.get('DEFAULT','filenamme')
        self.output_dir = self.config.get('DEFAULT','output_dir')
        
    
    def get_csv_location(self):
        return self.file_name, self.output_dir

class SpreadsheetDownloader:
    def __init__(self, url, local_file_path):
        self.url = url
        self.local_file_path = local_file_path

    def download_spreadsheet_to_df_if_updated(self):
        response = requests.get(self.url)
        remote_file_contents = response.content
        logging.info('downloading dataset from gov website')
        remote_file_hash = hashlib.sha256(remote_file_contents).hexdigest()
        logging.info('checking if local file exists')
        if os.path.exists(self.local_file_path):
            with open(self.local_file_path, 'rb') as f:
                logging.info('local file exists')
                local_file_contents = f.read()
            local_file_hash = hashlib.sha256(local_file_contents).hexdigest()
            logging.info('checking to see if remote file has been updated')
            if remote_file_hash == local_file_hash:
                logging.info('local file is the same as remote file')
                df = pd.read_excel(self.local_file_path, sheet_name='Quarter', skiprows=4)
                return df, 0
            else:
                logging.info('remote file has been updated, initiate rest of workflow')
                with open(self.local_file_path, 'wb') as f:
                    f.write(remote_file_contents)
                df = pd.read_excel(self.local_file_path, sheet_name='Quarter', skiprows=4)
                return df, 1
        else:
            logging.info('local file does not exists, it is probably the first time running this code, downloading raw data now')
            with open(self.local_file_path, 'wb') as f:
                f.write(remote_file_contents)
            df = pd.read_excel(self.local_file_path, sheet_name='Quarter', skiprows=4)
            return df, 2



class DataFrameExporter:
    def __init__(self, df, export_type):
        self.df = df
        self.export_type = export_type
        self.config = configparser.ConfigParser()
        self.config.read('configure.ini')
        self.output_dir = self.config.get('DEFAULT', 'output_dir')
        self.file_name = self.config.get('DEFAULT', self.export_type)

    def export(self):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        file_path = os.path.join(self.output_dir, self.file_name + "_" + timestamp + ".csv")
        self.df.to_csv(file_path, index=False)



