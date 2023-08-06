from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def make_requests_with_retries():
    session = Session()
    retries = Retry(
        total=5, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    session.mount('http://', HTTPAdapter(max_retries=retries))
    return session
