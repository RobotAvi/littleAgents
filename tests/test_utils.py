import pytest
from shared import utils
from datetime import datetime

def test_format_datetime():
    dt = datetime(2024, 1, 1, 12, 0)
    formatted = utils.format_datetime(dt)
    assert isinstance(formatted, str)
    assert "2024" in formatted

def test_truncate_text():
    text = "a" * 200
    truncated = utils.truncate_text(text, max_length=50)
    assert len(truncated) <= 50