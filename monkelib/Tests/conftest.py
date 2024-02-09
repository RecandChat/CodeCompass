import pytest
from monkelib.API.get_data import get_user_repo, get_most_starred_repos


@pytest.mark.parametrize('username, expected', [
    ('octocat', True),
    ('gfdhgfdhgfdhgfd', False)
])
def test_get_user_repo(username, expected):
    assert get_user_repo(username) == expected


def test_get_most_starred_repos():
    assert get_most_starred_repos() is True
