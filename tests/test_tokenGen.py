import pytest
from src.services.tokengen import TokenGenerator


@pytest.fixture
def tokengen():
    return TokenGenerator()


def test_tokengen(tokengen):
    token = tokengen.gen()
    assert token > 10000
