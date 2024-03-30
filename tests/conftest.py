import pytest
from google.oauth2.credentials import Credentials
from codecompasslib.API.drive_operations import get_creds_drive
from pandas import DataFrame


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


@pytest.fixture
def creds() -> Credentials:
    """
    Returns a Google Drive API credentials object
    :return: A Google Drive API credentials object
    """
    return get_creds_drive()


@pytest.fixture
def folder_id() -> str:
    """
    Returns a folder ID to be used in tests
    :return: A string representing a folder ID
    """
    return '13JitBJQLNgMvFwx4QJcvrmDwKOYAShVx'


@pytest.fixture
def drive_id() -> str:
    """
    Returns a drive ID to be used in tests
    :return: A string representing a drive ID
    """
    return '0AL1DtB4TdEWdUk9PVA'


@pytest.fixture
def file_id() -> str:
    """
    Returns a file ID to be used in tests
    :return: A string representing a file ID
    """
    return '1hAP9CD6iP4FSZP4RSRm2CYUrS2KF_Lhf'


@pytest.fixture
def df() -> DataFrame:
    """
    Returns a pandas DataFrame to be used in tests
    :return: A pandas DataFrame
    """
    return DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})


@pytest.fixture
def filename() -> str:
    """
    Returns a filename to be used in tests
    :return: A string representing a filename
    """
    return 'test.csv'
