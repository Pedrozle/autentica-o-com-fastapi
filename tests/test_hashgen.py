import pytest
from src.services.hashgen import HashGenerator


@pytest.fixture
def hashgen():
    return HashGenerator()


def test_hashgen(hashgen):
    data = "pytest"
    hash = hashgen.gen(data)
    assert (
        hash
        == "$argon2id$v=19$m=65536,t=3,p=2$ceD06nAVfhMcTGwXkxXn9g$qn+4dwt+cMWB+XzFrJldXHBH+QVoVNOFJZKGmWtCw+g"
    )
