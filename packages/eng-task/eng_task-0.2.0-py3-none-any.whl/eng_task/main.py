import csv_utils
import additional_reports
import preprocess



import logging
from csv_utils import SpreadsheetDownloader, CsvLocation, DataFrameExporter, CSVFileHandler
from preprocess import Preprocessor
from additional_reports import DataFrameComparer, DataFrameSummary, DataFrameComparer
import os
import configparser
import os
import time
import pandas as pd


# Configure the logging system
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

def data_profile(df):
    profile = DataFrameSummary(df)
    result_df = profile.summarize()
    return result_df

def preprocess(df):
    preprocessor = Preprocessor(df)
    preprocessed_df = preprocessor.preprocess()
    return preprocessed_df

def consistency(df1,df2):
    comparer = DataFrameComparer(df1, df2)
    results_df = comparer.compare()
    return results_df

def validate_schema(df1, df2):
    logging.info('Checking schema now')
    df1.iloc[:, 1:] = df1.iloc[:, 1:].astype(float)
    if df1.columns.tolist() == df2.columns.tolist():
        if df1.dtypes.equals(df2.dtypes):
            return True
    return False

def get_latest_file():
    csv_handler = CSVFileHandler()
    df = csv_handler.get_last_uploaded()
    return df
    
def get_raw_csv_location_and_download (url):
    csv_location = CsvLocation()
    file_name, output_dir = csv_location.get_csv_location()
    local_file_path = os.path.join(output_dir,file_name)
    downloader = SpreadsheetDownloader(url, local_file_path=local_file_path)
    df, updated_or_not_decision = downloader.download_spreadsheet_to_df_if_updated()
    return df, updated_or_not_decision

def export_clean_data(df, clean_data):
    logging.info('Exporting clean data csv to local path')
    exporter = DataFrameExporter(df,clean_data)
    exporter.export()
    
def export_profile_data(df, data_profiling):
    logging.info('Exporting data profile csv to local path')
    exporter = DataFrameExporter(df, data_profiling)
    exporter.export()
    
def export_consistecy_data(df, data_consistency):
    logging.info('Exporting data consistency csv to local path')
    exporter = DataFrameExporter(df,data_consistency)
    exporter.export()


def main(url):
    df, updated = get_raw_csv_location_and_download(url)
    if updated == 2:
        df_preprocess = preprocess(df)
        df_summary = data_profile(df_preprocess)
        export_profile_data(df_summary,data_profiling='data_profiling')
        export_clean_data(df_preprocess,clean_data='clean_data')
        return df_preprocess, df_summary
    elif updated == 1: 
        df_preprocess = preprocess(df)
        logging.info('validate_schema using columns and data types')
        logging.info('getting the latest file from latest clean_data csv from local path')
        df_old=get_latest_file()
        decision=validate_schema(df_preprocess,df_old)
        logging.info(f'the decision is {decision}')
        if decision is True:
            logging.info('The schemas are valid')
            df_summary = data_profile(df_preprocess)
            df_consistency = consistency(df, df_old)
            export_consistecy_data(df_consistency, data_consistency='data_consistency')
            export_profile_data(df_summary,data_profiling='data_profiling')
            export_clean_data(df_preprocess,clean_data='clean_data')
            logging.info('Done, they are now saved to your local patht that was defined')
            return df_preprocess, df_summary, df_consistency
    elif updated==0:
        print("There is nothing to do")
        

if __name__ == "__main__":
    # logging.info("Starting")
    # df = pd.read_csv('/Users/jedmundson/clean_data_2023-02-12_08-46-44.csv')
    # logging.info(df)

    url = "https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1126335/ET_3.1_DEC_22.xlsx"
    main(url)
  



   
        
