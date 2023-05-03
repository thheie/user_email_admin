import csv
import requests
import json
import os.path
from logger import logger


def load_csv_file():
    filename = 'managed_accounts.csv'
    logger.info(f'loading csv file: {filename}')
    value_list = []
    if os.path.isfile(filename):
        with open(filename, newline='') as csvfile:
            for row in csv.DictReader(csvfile):
                value_list.append(row)
            logger.debug('file loaded ok')
            return value_list
    else:
        logger.critical(f'CSV file: {filename} not found')


def set_url(item):
    url = f'https://api.atlassian.com/users/{item["Atlassian ID"]}/manage/email'
    # url = f'https://api.atlassian.com/users/{item["Atlassian ID"]}/manage/api-tokens'
    return url


def update_user_email(user_list):
    for user_id in user_list:
        url = set_url(user_id)
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer <bearer token>"
        }
        payload = json.dumps({'email': user_id['Email new']})
        response = requests.request(
            "GET",
            url,
            data=payload,
            headers=headers)
        if response.status_code == 200:
            logger.info(f'change email address for user {user_id["Name"]} to {user_id["Email new"]}')
        else:
            logger.info(
                f'Unable to change email address for user {user_id["Name"]}. Error code: {response.status_code}')


def main():
    user_list = load_csv_file()
    if len(user_list) > 0:
        update_user_email(user_list)


if __name__ == '__main__':
    main()
