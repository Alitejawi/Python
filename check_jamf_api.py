#!/usr/bin/env python3

__author__ = "Ali Al-Itejawi"
__version__ = "1.1"
__email__ = "ali@al-itejawi.com"

__description__ = "Check Jamf API"

import os
import jamf
import json
import credentials
import logging


def main():
    # Define paths and change the context to the repo
    base_path = os.path.dirname(os.path.abspath(__file__))
    api_url = '<your_jamf_url>'
    api_user = credentials.api_user
    api_pass = credentials.api_pass

    # Initalise a log for the email
    log_ext = 'txt'  # Use txt to view directly in your email client (if supported), use log to be read by a traditional log viewer
    log_file = os.path.join(base_path, '{}{}.{}'.format(os.path.basename(__file__).split('.')[0], os.getpid(), log_ext))
    logging.basicConfig(filename=log_file, format='[%(asctime)s] [%(levelname)-7s] %(message)s', level=logging.INFO)
    logging.info('Starting')

    api = jamf.JamfClassic(api_url, api_user, api_pass)
    data = api.get_data('scripts')
    if data.success:
        print(json.dumps(data.data))

        # failures.append('Invalid format of address {}, {}'.format(mac, serial))
    else:
        logging.critical('Failed to pull advanced search')


if __name__ == '__main__':
    main()

