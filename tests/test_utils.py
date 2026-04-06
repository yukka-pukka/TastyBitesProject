import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import normalize, compute_score, is_minority_owned

def test_normalize_ampersand():
    assert normalize("Chicken & Waffles") == "chicken and waffles"

def test_normalize_whitespace():
    assert normalize("  Cafe Selam  ") == "cafe selam"

def test_normalize_lowercase():
    assert normalize("CAFE SELAM") == "cafe selam"

def test_normalize_combined():
    assert normalize("  Fat's Chicken & Waffles  ") == "fat's chicken and waffles"

def test_compute_score_range():
    score = compute_score(0.5, 4.5)
    assert 0 < score <= 5

def test_compute_score_closer_is_better():
    close = compute_score(0.1, 4.0)
    far = compute_score(5.0, 4.0)
    assert close > far

def test_compute_score_higher_rating_is_better():
    high = compute_score(1.0, 5.0)
    low = compute_score(1.0, 2.0)
    assert high > low

def test_compute_score_zero_distance():
    score = compute_score(0, 5.0)
    assert score > 0

def test_compute_score_zero_rating():
    score = compute_score(1.0, 0)
    assert score >= 0

def test_is_minority_owned_known():
    assert is_minority_owned("Cafe Selam") == True

def test_is_minority_owned_unknown():
    assert is_minority_owned("McDonald's") == False

def test_is_minority_owned_case_insensitive():
    assert is_minority_owned("cafe selam") == True

def test_is_minority_owned_ampersand():
    assert is_minority_owned("Fat's Chicken & Waffles") == True