# tests/test_preprocess.py
import pytest

from app.constants.app_constants import MAX_QUESTION_LENGTH
from app.services.preprocess_service import preprocess_question


def test_collapses_internal_whitespace():
    assert preprocess_question("What   is  2 +   2?") == "What is 2 + 2?"


def test_strips_surrounding_whitespace():
    assert preprocess_question("  hello  ") == "hello"


def test_empty_after_cleaning_raises():
    with pytest.raises(ValueError):
        preprocess_question("     ")


def test_too_long_raises():
    with pytest.raises(ValueError):
        preprocess_question("a" * (MAX_QUESTION_LENGTH + 1))