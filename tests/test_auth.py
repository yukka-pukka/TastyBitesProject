import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from auth import hash_password, verify_password

def test_password_hashing():
    hashed = hash_password("mypassword")
    assert verify_password("mypassword", hashed) == True

def test_wrong_password():
    hashed = hash_password("mypassword")
    assert verify_password("wrongpassword", hashed) == False

def test_empty_password():
    hashed = hash_password("")
    assert verify_password("", hashed) == True

def test_hashes_are_unique():
    # same password should produce different hashes each time
    hash1 = hash_password("mypassword")
    hash2 = hash_password("mypassword")
    assert hash1 != hash2

def test_hash_is_string():
    hashed = hash_password("mypassword")
    assert isinstance(hashed, str)