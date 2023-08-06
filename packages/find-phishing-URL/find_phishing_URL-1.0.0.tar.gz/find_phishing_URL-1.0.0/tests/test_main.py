import pytest
import requests_mock
from src.package.main import phishing_or_not


@pytest.mark.parametrize(
    "url, is_valid", [("https://google.com", "yes"),
                      ("https://dummy.com", "no"),
                      ("https://nodummy.com", "unknown")]
)
def test_phishing_or_not(url, is_valid):
    try:
        m = requests_mock.Mocker()
        m.post(
            "https://checkurl.phishtank.com/checkurl/index.php",
            data={"url": url, "format": "json"},
            verify=False)
    except Exception as e:
        print("\nError Occurred !!!\nDisplaying Error : ")
        print(e)
    assert phishing_or_not(url) == is_valid
