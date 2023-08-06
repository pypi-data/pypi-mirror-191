import re
import pandas as pd
import numpy as np

class Preprocessor:
    def __init__(self, df):
        self.df = df
    
    def clean_data(self):
        self.df.replace(to_replace=0, value=np.nan, inplace=True)
        return self.df

    def remove_brackets(self):
        for col in self.df.columns:
            self.df[col] = self.df[col].apply(lambda x: re.sub(r'[\{\}\[\]\(\)"]', '', str(x)))
        return self.df

    def to_datetime(self, string):
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

    def rename_columns(self):
        columns = self.df.columns[1:]
        rename_dict = {}
        for col in columns:
            if col != self.df.columns[0]:
                rename_dict[col] = self.to_datetime(col)
        self.df.rename(columns=rename_dict, inplace=True)
        return self.df
    
    def preprocess(self):
        # self.clean_data()
        self.remove_brackets()
        self.rename_columns()
        return self.df

