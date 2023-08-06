
import pandas as pd
import numpy as np
class DataFrameComparer:
    def __init__(self, df1, df2):
        self.df1 = df1
        self.df2 = df2

    def compare(self):
        # Check the number of missing values
        missing_values_df1 = self.df1.isnull().sum().sum()
        missing_values_df2 = self.df2.isnull().sum().sum()
        
        # Check for differences in columns
        different_columns = list(set(self.df1.columns) ^ set(self.df2.columns))
        
        return pd.DataFrame({
            'missing_values_df1': [missing_values_df1],
            'missing_values_df2': [missing_values_df2],
            'different_columns': [different_columns]
        })


class DataFrameSummary:
    def __init__(self, data):
        self.data = data

    def summarize(self):
        df = self.data
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
        combined_df.replace(to_replace=np.nan, value='', inplace=True)
        return combined_df

