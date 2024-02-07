from insta_scraper.exceptions import InvalidCookies
from insta_scraper.instagram_request import InstagramRequest
from insta_scraper.utils import parse_cookie_file

_request = InstagramRequest()


def _set_cookies(filename: str):
    try:
        cookies = parse_cookie_file(filename)
    except ValueError as error:
        raise InvalidCookies(f'Cookies are in an invalid format: {error}') from error

    if cookies is not None:
        cookie_names = [c.name for c in cookies]

        missing_cookies = [c for c in ['sessionid'] if c not in cookie_names]

        if missing_cookies:
            raise InvalidCookies(f'Missing cookies with name(s): {missing_cookies}')

        _request.session.cookies.update(cookies)

        if not _request.is_logged_in():
            raise InvalidCookies('Cookies are not valid')

    print('ok')


def login_check(cookies: str):
    _set_cookies(cookies)
