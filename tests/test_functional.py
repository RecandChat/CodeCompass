import pytest
from codecompasslib.API.get_bulk_data import get_users, get_followers, get_following, \
    get_user_repos, get_misc_data, get_bulk_data


def test_get_users(sample_size) -> None:
    """
    This function tests the get_users function.
    :param sample_size: How many users to get.
    :return: None
    """
    users_list: list
    users_flag: bool
    users_list, users_flag = get_users(sample_size)
    assert len(users_list) == 1
    assert users_flag


def test_get_followers(sample_user) -> None:
    """
    This function tests the get_followers function.
    :param sample_user: A sample user (Lukasaurus11)
    :return: None
    """
    followers_list: list
    followers_flag: bool
    followers_list, followers_flag = get_followers(sample_user)
    assert len(followers_list) > 0
    assert followers_flag


def test_get_followers_fail(non_existent_user) -> None:
    """
    This function tests the get_followers function with a non-existent user.
    :param non_existent_user: A non-existent user (ThisUserDoesNotExist1234567890)
    :return: None
    """
    followers_list: list
    followers_flag: bool
    followers_list, followers_flag = get_followers(non_existent_user)
    assert len(followers_list) == 0
    assert followers_flag is False


def test_get_following(sample_user) -> None:
    """
    This function tests the get_following function.
    :param sample_user: A sample user (Lukasaurus11)
    :return: None
    """
    following_list: list
    following_flag: bool
    following_list, following_flag = get_following(sample_user)
    assert len(following_list) > 0
    assert following_flag


def test_get_following_fail(non_existent_user) -> None:
    """
    This function tests the get_following function with a non-existent user.
    :param non_existent_user: A non-existent user (ThisUserDoesNotExist1234567890)
    :return: None
    """
    following_list: list
    following_flag: bool
    following_list, following_flag = get_following(non_existent_user)
    assert len(following_list) == 0
    assert following_flag is False


def test_get_user_repos(sample_user) -> None:
    """
    This function tests the get_user_repos function.
    :param sample_user: A sample user (Lukasaurus11)
    :return: None
    """
    user_repos: list
    user_repos_flag: bool
    user_repos, user_repos_flag = get_user_repos(sample_user)
    assert len(user_repos) > 0
    assert user_repos_flag


def test_get_user_repos_fail(non_existent_user) -> None:
    """
    This function tests the get_user_repos function with a non-existent user.
    :param non_existent_user: A non-existent user (ThisUserDoesNotExist1234567890)
    :return: None
    """
    user_repos: list
    user_repos_flag: bool
    user_repos, user_repos_flag = get_user_repos(non_existent_user)
    assert len(user_repos) == 0
    assert user_repos_flag is False


def test_get_misc_data() -> None:
    """
    This function tests the get_misc_data function, with an accepted field (language).
    :return: None
    """
    misc_data_flag: bool = get_misc_data(['language'])
    assert misc_data_flag


def test_get_misc_data_fail() -> None:
    """
    This function tests the get_misc_data function, with a non-accepted field (ThisFieldDoesNotExist).
    :return: None
    """
    misc_data_flag: bool = get_misc_data(['ThisFieldDoesNotExist'])
    assert misc_data_flag is False


def test_get_bulk_data(sample_size) -> None:
    """
    This function tests the get_bulk_data function.
    :param sample_size: How many users to get.
    :return: None
    """
    bulk_data_flag: bool = get_bulk_data(sample_size)
    assert bulk_data_flag
