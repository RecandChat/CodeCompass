from monkelib.API.get_data import get_user_repo, get_most_starred_repos
import pytest


def test_get_user_repo():
    assert get_user_repo('octocat') is True
    assert get_user_repo('gfdhgfdhgfdhgfd') is False


def test_get_most_starred_repos():
    assert get_most_starred_repos() is True

