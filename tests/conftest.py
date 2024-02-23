import pytest


@pytest.fixture
def sample_user() -> str:
    """
    Returns a sample user to be used in tests
    :return: A string representing a sample user
    """
    return 'Lukasaurus11'


@pytest.fixture
def non_existent_user() -> str:
    """
    Returns a non-existent user to be used in tests
    :return: A string representing a non-existent user
    """
    return 'ThisUserDoesNotExist1234567890'


@pytest.fixture
def sample_size() -> int:
    """
    Returns a sample size to be used in tests
    :return: 1
    """
    return 1
