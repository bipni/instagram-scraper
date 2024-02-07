from datetime import datetime
from itertools import dropwhile, takewhile

from instaloader import Instaloader, Profile


class Instagram:
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.L = Instaloader()
        self._login()

    def _login(self):
        self.L.login(self.username, self.password)

    def get_profile_by_username(self, username, post_count: int = None, start_date: str = None, end_date: str = None):
        try:
            profile = Profile.from_username(self.L.context, username)

            profile_info = profile._asdict()

            profile_info['mediacount'] = profile.mediacount
            profile_info['posts'] = []

            posts = profile.get_posts()

            if start_date and end_date:
                since = datetime.strptime(end_date, '%Y-%m-%d')
                until = end_date.strptime(start_date, '%Y-%m-%d')

                for post in takewhile(lambda p: p.date > until, dropwhile(lambda p: p.date > since, posts)):
                    profile_info['posts'].append(post._asdict())

                    if post_count and len(profile_info['posts']) >= post_count:
                        break
            else:
                for post in profile.get_posts():
                    post_info = post._asdict()

                    post_info['comments'] = []

                    for comment in post.get_comments():
                        post_info['comments'].append(comment._asdict())

                    profile_info['posts'].append(post_info)

                    if post_count and len(profile_info['posts']) >= post_count:
                        break

            return profile_info
        except Exception as error:
            print(error)
