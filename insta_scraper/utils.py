from requests.cookies import RequestsCookieJar

from insta_scraper.exceptions import InvalidCookies


def parse_cookie_file(filename: str) -> RequestsCookieJar:
    jar = RequestsCookieJar()

    with open(filename, mode='rt', encoding='utf-8') as file:
        data = file.read()

    # only netscape format
    for i, line in enumerate(data.splitlines()):
        line = line.strip()

        if line == '' or line.startswith('#'):
            continue

        try:
            domain, _, path, secure, expires, name, value = line.split('\t')
        except Exception as error:
            raise InvalidCookies(f"Can't parse line {i + 1}: '{line}'") from error

        secure = secure.lower() == 'true'
        expires = None if expires == '0' else int(expires)

        jar.set(name, value, domain=domain, path=path, secure=secure, expires=expires)

    return jar
