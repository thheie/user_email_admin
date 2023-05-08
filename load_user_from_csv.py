"""
Loads and iterates though a list  of Atlassian user ids and a new email address for that specific user.
The emails are updated using the Atlassian user api for email updates
see https://developer.atlassian.com/cloud/admin/user-management/rest/api-group-email/#api-users-account-id-manage-email-put for details
"""
import csv
import requests
import json
import os.path
from logger import logger


def load_csv_file(filename):
    """
    Loads user identifier and new email address from a csv file
    :param filename: The name of the file that is to be loaded
    :return: A list of dicts. The identifier of the dicts is the same as the column headers in the CSV file
    """
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
    """
    Creates the urs that is cals the api
    :param item: a dict that contains the user id
    :return: the complete URL for the api
    """
    url = f'https://api.atlassian.com/users/{item["User id"]}/manage/email'
    # url = f'https://api.atlassian.com/users/{item["Atlassian ID"]}/manage/api-tokens'
    return url


def update_user_email(user_list):
    """
    updates user emails using the Atlassian rest api for email updates.
    :param user_list: A list of dicts that must contain a value for user_id and a value for the new email address.
    :return: Nothing
    """
    for user_id in user_list:
        url = set_url(user_id)
        headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer <api token>"
        }
        payload = json.dumps({"email": user_id["email - new"]})
        response = requests.request(
            "PUT",
            url,
            data=payload,
            headers=headers)
        if response.status_code == 204:
            logger.info(f'change email address for user {user_id["email"]} to {user_id["email - new"]}')
        else:
            logger.info(f'Unable to change email address for user {user_id["email"]} to {user_id["email - new"]}. Error code: {response.status_code}')
            logger.info(f'{response.text}')


def main():
    filename = 'userlist.csv'
    user_list = load_csv_file(filename)
    if len(user_list) > 0:
        update_user_email(user_list)


if __name__ == '__main__':
    main()
