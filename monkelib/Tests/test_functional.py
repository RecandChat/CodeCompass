import pytest
from monkelib.API.get_bulk_data import *


def test_get_users(sample_size):
    users_list, users_flag = get_users(sample_size)
    assert users_flag
    assert len(users_list) == 1


def test_get_followers(sample_user):
    followers_list, followers_flag = get_followers(sample_user)
    assert followers_flag
    assert len(followers_list) > 0


def test_get_followers_fail(non_existent_user):
    followers_list, followers_flag = get_followers(non_existent_user)
    assert followers_flag is False
    assert len(followers_list) == 0


def test_get_following(sample_user):
    following_list, following_flag = get_following(sample_user)
    assert following_flag
    assert len(following_list) > 0


def test_get_following_fail(non_existent_user):
    following_list, following_flag = get_following(non_existent_user)
    assert following_flag is False
    assert len(following_list) == 0


def test_get_user_repos(sample_user):
    user_repos, user_repos_flag = get_user_repos(sample_user)
    assert user_repos_flag
    assert len(user_repos) > 0


def test_get_user_repos_fail(non_existent_user):
    user_repos, user_repos_flag = get_user_repos(non_existent_user)
    assert user_repos_flag is False
    assert len(user_repos) == 0


def test_get_misc_data():
    misc_data_flag = get_misc_data(['language'])
    assert misc_data_flag


def test_get_misc_data_fail():
    misc_data_flag = get_misc_data(['ThisFieldDoesNotExist'])
    assert misc_data_flag is False


def test_get_bulk_data(sample_size):
    bulk_data_flag = get_bulk_data(sample_size)
    assert bulk_data_flag
