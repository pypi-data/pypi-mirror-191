from ..himan.pandas.utils import file_ext
from pathlib import Path, PurePath



def get_path(filename):
    return PurePath(Path(__file__).parent, 'samples', 'csv', filename)


def test_should_extract_extension():
    filepath= get_path('sample.csv')
    ext = file_ext(filepath)

    assert 'csv' == ext