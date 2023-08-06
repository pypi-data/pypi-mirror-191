import os
from pathlib import Path, PurePath
from ..himan.pandas.utils import load_file, write



def get_path(filename):
    return PurePath(Path(__file__).parent, 'samples', 'csv', filename)



def test_should_write_csv_file():
    filename = get_path('sample_01.csv')

    items = [
        {'name': 'John', 'surname': 'Smith', 'age': 18},
        {'name': 'Peter', 'surname': 'Adams', 'age': 30}
    ]

    write(filename, items)

    item = load_file(filename)

    keys = item.keys()
    assert len(keys) == 3
    assert 'age' in item.keys()

    os.remove(filename)


def test_should_append_csv_file():
    filename = get_path('sample_01.csv')

    items = [
        {'name': 'John', 'surname': 'Smith', 'age': 18},
        {'name': 'Peter', 'surname': 'Adams', 'age': 30}
    ]

    write(filename, items)

    item = load_file(filename)

    keys = item.keys()
    assert len(keys) == 3
    assert 'age' in item.keys()

    new_item = [
        {'name': 'Paul', 'surname': 'Sanders', 'age': 21},
    ]

    write(filename, new_item, 'a')

    item = load_file(filename)
    assert len(item['name']) == 3

    os.remove(filename)

