from requests import RequestException
from requests_html import HTMLSession

from insta_scraper.constants import (
    DEFAULT_HEADERS,
    DEFAULT_REQUESTS_TIMEOUT,
    INSTA_BASE_URL,
)
from insta_scraper.exceptions import LoginRequired


class InstagramRequest:
    base_url = INSTA_BASE_URL
    default_headers = DEFAULT_HEADERS

    have_checked_locale = False

    def __init__(self, session=None, requests_kwargs=None) -> None:
        if session is None:
            session = HTMLSession()
            session.headers.update(self.default_headers)

        if requests_kwargs is None:
            requests_kwargs = {
                'timeout': DEFAULT_REQUESTS_TIMEOUT
            }

        self.session = session
        self.requests_kwargs = requests_kwargs
        self.request_count = 0

    def set_user_agent(self, user_agent):
        self.session.headers['User-Agent'] = user_agent

    def is_logged_in(self) -> bool:
        try:
            self.get(self.base_url + '/accounts/edit/')
            return True
        except LoginRequired:
            return False

    def get(self, url, **kwargs):
        try:
            self.request_count += 1

            url = str(url)

            response = self.session.get(url=url, **self.requests_kwargs, **kwargs)

            response.html.html = response.html.html.replace('<!--', '').replace('-->', '')
            response.raise_for_status()

            title = response.html.find('title', first=True)

            if title:
                print(title.text)
                if (title.text == "Login • Instagram" or response.url.startswith(self.base_url + '/accounts/login')):
                    raise LoginRequired("A login (cookies) is required to see this page")

            return response.html.html
        except RequestException as error:
            print('Exception while requesting URL: %s\nException: %r', url, error)
            raise
