import csv
from os.path import exists

from instagram import Instagram

USERNAME = 'kraisahossain@gmail.com'
PASSWORD = '#123456789'

POST_COUNT = 20
START_TIME = None       # 'YYYY-MM-DD'
END_TIME = None         # 'YYYY-MM-DD'
PROFILE_NAMES = ['cocacola', 'chanchal_chowdhury']
FILE_NAME = 'profile.csv'

try:
    insta = Instagram(USERNAME, PASSWORD)

    for profile_name in PROFILE_NAMES:
        profile_info = insta.get_profile_by_username(profile_name)

        if not exists(f'files/{FILE_NAME}'):
            with open(f'files/{FILE_NAME}', 'w', encoding='utf-8', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(list(profile_info.keys()))

        copy_dict = {}

        for header in list(profile_info.keys()):
            copy_dict[header] = profile_info[header]

        if exists(f'files/{FILE_NAME}'):
            with open(f'files/{FILE_NAME}', 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=copy_dict.keys())
                writer.writerow(copy_dict)
        else:
            with open(f'files/{FILE_NAME}', 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=copy_dict.keys())
                writer.writeheader()
                writer.writerow(copy_dict)

    print(profile_info)
except Exception as error:
    print(error)
