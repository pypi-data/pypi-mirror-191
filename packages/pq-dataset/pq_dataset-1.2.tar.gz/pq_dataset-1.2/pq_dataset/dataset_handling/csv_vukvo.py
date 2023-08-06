from dataclasses import dataclass
import re
import pandas as pd
from typing import List

from pq_dataset.utils.InputFile import InputFile
from pq_dataset.dataset_handling.pd_clean_up_columns import pd_clean_up_columns

@dataclass
class CsvVukvoDataset:
    input_file: str
    json_file: str
    
    def __post_init__(self):

        if not InputFile(self.input_file).valid():
            raise OSError(f'{self.input_file} not found')
        
    def load(self):
        raise NotImplementedError
    
    def load_as_pandas_df(self, columns_subset: List[str] = [], root_var: str = '') -> pd.DataFrame:
        
        def clean_root_data(df: pd.DataFrame, root_var: str) -> pd.DataFrame:
            query_string = f'{root_var}`.notnull()'
            try:
                df2 = self.data.query(query_string)
            except KeyError: 
                # self.logger.debug('clean_root_data tried to filter df, but variable does not exist')
                return self.data
            # self.logger.debug(f'clean_root_data removed {self.data.shape[0] - df2.shape[0]} cases from dataframe')
            return df2
        
        if columns_subset:
            df = pd.read_csv(self.input_file, use_cols=columns_subset, encoding='utf-8-sig', sep=';', decimal=',', low_memory=False)
        else:
            df = pd.read_csv(self.input_file, encoding='utf-8-sig', sep=';', decimal=',', low_memory=False)
        
        df = df.rename(columns=lambda x: re.sub('(\/)','__',x)) # Replacing / with __
        df = clean_root_data(df, root_var)
        df = pd_clean_up_columns(df)
        
        return df