import pandas as pd
from typing import List



def load_file(filepath, header=0, as_dataframe=False):
    '''It should load any kind of file formats'''

    ext = file_ext(filepath)

    if ext == 'csv':
        df = pd.read_csv(filepath, header=header)
    elif ext in ['xlsx', 'xls']:
        df = pd.read_excel(filepath, header=header)
    else:
        print("Invalid file format")
        return None
    
    if as_dataframe:
        return df

    return df.to_dict('list')

def write(filepath, items: List[dict], mode='w'):
    header = True
    if mode == 'a':
        header = False

    ext = file_ext(filepath)

    if ext == 'csv':
        df = pd.DataFrame(items) 
        df.to_csv(filepath, index=False, mode=mode, header=header)


def file_ext(filepath):
    filename = filepath.name
    return filename.split('.')[-1]