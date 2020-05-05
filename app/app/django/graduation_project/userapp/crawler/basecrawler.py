import re
import requests
from typing import Dict, Optional
from bs4 import BeautifulSoup

url_pattern = re.compile(r"(https?|ftp)://(-\.)?([^\s/?\.#-]+\.?)+(/[^\s]*)?$")


def get_bs_from_url(url: str, rheader: Optional[Dict[str, str]] = None) -> BeautifulSoup:
    if url_pattern.match(url):
        try:
            res = requests.get(url, headers=rheader)

            if res.status_code == 200:
                return BeautifulSoup(res.text, "lxml")
            else:
                raise requests.exceptions.RequestException
        except requests.exceptions.RequestException:
            print(f"Cannot access '{url}'")
    else:
        raise ValueError(f"'{url}' is not url")
