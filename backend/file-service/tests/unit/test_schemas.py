import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../file-service')))
from schemas.file import FileCreate, FileRead, FolderCreate
import uuid
import datetime
import pytest

def test_file_create_valid():
    obj = FileCreate(filename='abc.txt', size=1, content_type='txt')
    assert obj.filename == 'abc.txt'
    assert obj.size == 1
    assert obj.content_type == 'txt'

def test_file_create_invalid():
    with pytest.raises(ValueError):
        FileCreate(filename='a/b.txt', size=1, content_type='txt')

def test_file_read():
    obj = FileRead(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        filename='abc.txt',
        size=1,
        content_type='txt',
        created_at=datetime.datetime.now(datetime.timezone.utc)
    )
    assert obj.filename == 'abc.txt'

def test_folder_create_valid():
    obj = FolderCreate(folder_name='folder')
    assert obj.folder_name == 'folder'

def test_folder_create_invalid():
    with pytest.raises(ValueError):
        FolderCreate(folder_name='bad/folder')
