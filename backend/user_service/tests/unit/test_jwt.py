import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from security.tokens.jwt import create_access_token
from datetime import timedelta

def test_create_access_token_default():
    token = create_access_token({"sub": "user_id"})
    assert isinstance(token, str)
    assert len(token) > 0

def test_create_access_token_with_expiry():
    token = create_access_token({"sub": "user_id"}, expires_delta=timedelta(minutes=1))
    assert isinstance(token, str)
    assert len(token) > 0
