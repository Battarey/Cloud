import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from security.password.password import get_password_hash, verify_password
import pytest

def test_password_hash_and_verify():
    password = "TestPassword123!"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("WrongPassword", hashed)

@pytest.mark.parametrize("password", [
    "short",
    "nouppercase1!",
    "NOLOWERCASE1!",
    "NoNumber!",
    "NoNumber1"
])
def test_password_hash_invalid(password):
    # Проверка, что хеширование не падает на невалидных паролях (валидация вне схемы)
    hashed = get_password_hash(password)
    assert isinstance(hashed, str)
