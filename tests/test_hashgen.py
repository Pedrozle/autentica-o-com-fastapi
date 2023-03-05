import pytest
from src.services.hashgen import HashGenerator


@pytest.fixture
def hashgen():
    return HashGenerator()


def test_hashgen(hashgen):
    data = "pytest".encode("utf-8")
    hash = hashgen.gen(data)
    assert (
        hash
        == "1f3f1ad131e3c1f89c3319207733bb233d537ba0cd9ab3791580f235340ca537bf6c6a9dedcfeb03e05b331f5d3ae7a8d141a8a31b221e520f00be50d25f00e5"
    )
