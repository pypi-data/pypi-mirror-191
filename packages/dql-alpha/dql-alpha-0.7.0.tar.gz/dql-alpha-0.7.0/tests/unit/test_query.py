import pytest

from dql.data_storage.query import _escape_like


@pytest.mark.parametrize(
    "text,expected",
    (
        ("test like", "test like"),
        ("Can%t \\escape_this", "Can\\%t \\\\escape\\_this"),
    ),
)
def test_escape_like(text, expected):
    assert _escape_like(text) == expected
