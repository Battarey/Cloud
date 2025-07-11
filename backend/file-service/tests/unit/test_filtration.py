import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../file-service')))
from filtration.service import filter_files
from filtration.schemas import FileFilterParams
from types import SimpleNamespace
import datetime

def make_file(filename, created_at, size, content_type):
    return SimpleNamespace(filename=filename, created_at=created_at, size=size, content_type=content_type)

def test_filter_files_by_name():
    files = [make_file('abc.txt', datetime.datetime.now(), 10, 'txt'), make_file('def.txt', datetime.datetime.now(), 20, 'txt')]
    params = FileFilterParams(name='abc')
    result = filter_files(files, params)
    assert len(result) == 1
    assert result[0].filename == 'abc.txt'

def test_filter_files_by_size():
    files = [make_file('a', datetime.datetime.now(), 10, 'txt'), make_file('b', datetime.datetime.now(), 20, 'txt')]
    params = FileFilterParams(size_min=15)
    result = filter_files(files, params)
    assert len(result) == 1
    assert result[0].filename == 'b'

def test_filter_files_by_type():
    files = [make_file('a', datetime.datetime.now(), 10, 'txt'), make_file('b', datetime.datetime.now(), 20, 'folder')]
    params = FileFilterParams(file_type='folder')
    result = filter_files(files, params)
    assert len(result) == 1
    assert result[0].content_type == 'folder'
