from ..himan.pandas.utils import load_file
from pandas import DataFrame
from pathlib import Path, PurePath



def get_path(filename):
    return PurePath(Path(__file__).parent, 'samples', 'csv', filename)


filepath = get_path('sample.csv')

def test_should_read_csv_file():
    item = load_file(filepath)

    keys = item.keys()
    assert len(keys) == 2
    assert 'name' in item.keys()

def test_should_accept_no_header_parameter():
    item = load_file(filepath, header=None)

    keys = item.keys()
    assert len(keys) == 2
    assert 'name' not in item.keys()
    assert item[0][1:] == ['John', 'Peter']

def test_should_read_as_dataframe():
    item = load_file(filepath, as_dataframe=True)

    assert isinstance(item, DataFrame)
