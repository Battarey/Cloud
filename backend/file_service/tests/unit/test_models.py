import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../file-service')))
from models.file import File
import datetime
import uuid

def test_file_model_fields():
    file = File(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        filename='test.txt',
        size=123,
        content_type='text/plain',
        storage_key='key',
        created_at=datetime.datetime.now(datetime.timezone.utc)
    )
    assert file.filename == 'test.txt'
    assert file.size == 123
    assert file.content_type == 'text/plain'
    assert file.storage_key == 'key'
    assert isinstance(file.created_at, datetime.datetime)
