"""
Utilities for making external web requests.
"""
import os
from typing import Optional
import tempfile


import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from selenium import webdriver

DEFAULT_TIMEOUT = 20  # seconds


def screenshot(url: str, width: int=768, height: int=768) -> str:
    """
    Take a screenshot of a url and save to a tempfile.
    """
    driver = webdriver.Chrome()
    driver.set_window_size(width, height)
    driver.get(url)
    _, fn = tempfile.mkstemp(suffix=".png")
    driver.save_screenshot(fn)
    driver.quit()
    return fn


class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)


def get_session(**kwargs):
    """
    Get an http session with retry/timeout logic.
    """
    retries = Retry(
        total=kwargs.pop("max_retries", 3),
        backoff_factor=kwargs.pop("backoff", 1.2),
        status_forcelist=kwargs.pop("retry_on", [429, 500, 502, 503, 504]),
    )
    http = requests.Session(**kwargs)
    http.mount("https://", TimeoutHTTPAdapter(max_retries=retries))
    http.mount("https://", TimeoutHTTPAdapter(max_retries=retries))
    return http


def download_file(
    url, local_path: Optional[str] = None, chunk_size: int = 8192, **kwargs
) -> str:
    """download a public url locally"""
    session = get_session(**kwargs)

    # create a temp path
    if not local_path:
        # create output path
        ext = url.split(".")[-1].lower()
        name = url.split("/")[-1].split(".")[0].lower()
        tempdir = tempfile.mkdtemp(prefix="byb-")
        local_path = os.path.join(tempdir, f"{name}.{ext}")

    with session.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
    return local_path


def exists(url) -> bool:
    """
    Check if a URL exists via HEAD request
    """
    r = requests.head(url)
    return int(r.status_code) < 400
