import argparse
import os
from sys import stderr
from typing import TextIO
from urllib.parse import urlencode

import requests
from appdirs import user_config_dir, user_data_dir
from dotenv import load_dotenv

from . import VERSION, Database

USER_CONFIG_DIR = user_config_dir('twofer')
USER_DATA_DIR = user_data_dir('twofer')

# dotenv
load_dotenv()
CLIENT_ENV = os.getenv('TWOFER_CLIENT_ENV', 'twofer-client.env')
load_dotenv(CLIENT_ENV)
CLIENT_CONFIG_FILE = os.getenv(
    'TWOFER_CLIENT_CONFIG_FILE', os.path.join(USER_CONFIG_DIR, 'twofer-client-config.json'))
CLIENT_DATA_FILE = os.getenv(
    'TWOFER_CLIENT_DATA_FILE', os.path.join(USER_DATA_DIR, 'twofer-client-data.json'))
CLIENT_CA_FILE = os.getenv('TWOFER_CLIENT_CA_FILE')
CLIENT_TIMEOUT = int(os.getenv('TWOFER_CLIENT_TIMEOUT', 60))


database = Database(CLIENT_DATA_FILE)
database.load()


def _init(args: argparse.Namespace) -> None:

    server_name = database.get('server_name', 'twofer.example.com')
    server_name = input(f'1. Twofer server [{server_name}]: ') or server_name
    database['server_name'] = server_name.strip()
    database.save()

    user_token = input(f"""2. Open the link below, authenticate the app,

    https://{server_name}/authenticate

   and enter the user token shown: """)

    database['user_token'] = user_token.strip()
    database.save()

    print('completed.')


def _login(args: argparse.Namespace) -> None:

    try:
        user_token: str = database['user_token']
        server_name: str = database['server_name']
    except:
        print('You don\'t have valid login information. Try "tf init" to initialize the client.')
        exit(1)

    query_str = urlencode({'user_token': user_token})
    print(f"""Open the link below to login:

    https://{server_name}/login?{query_str}
    """)


def _version(args: argparse.Namespace) -> None:
    print(VERSION)


def _delete(args: argparse.Namespace) -> None:

    tweet_id: int = args.tweet_id

    user_token: str = database['user_token']
    server_name: str = database['server_name']

    query = urlencode({'user_token': user_token})
    url = f'https://{server_name}/2/tweets/{tweet_id}?{query}'
    res = requests.delete(url, verify=CLIENT_CA_FILE, timeout=CLIENT_TIMEOUT)
    if res.status_code == 200:
        print('successfully deleted:', tweet_id)
    else:
        print('returned', res.status_code, res.reason)



def _create(args: argparse.Namespace) -> None:

    text_io: TextIO | None = args.file
    silent_mode = bool(args.silent)

    if text_io:
        text = text_io.read()
    else:
        try:
            text = input("What's happening?: ").strip()
        except KeyboardInterrupt:
            print('\ncancelled: KeyboardInterrupt')
            exit(1)
        if not text:
            print('cancelled: text is empty')
            exit(1)

    user_token = database['user_token']
    server_name = database['server_name']
    data = {'text': text}

    query_str = urlencode({'user_token': user_token})
    url = f'https://{server_name}/2/tweets?{query_str}'
    try:
        res = requests.post(url, json=data, verify=CLIENT_CA_FILE, timeout=CLIENT_TIMEOUT)
    except requests.ReadTimeout:
        print('ReadTimeout: The server did not send any data in the allotted amount of time.',
              file=stderr)
        return

    if res.status_code == 200:
        if not silent_mode:
            print('successfully tweeted:', res.json()['data']['id'])
        return

    print('returned', res.status_code, res.reason, file=stderr)


def main() -> None:

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    _parser = subparsers.add_parser('init', help='initialize client')
    _parser.set_defaults(func=_init)

    _parser = subparsers.add_parser('login', help='show login url')
    _parser.set_defaults(func=_login)

    _parser = subparsers.add_parser('delete', help='delete tweet')
    _parser.add_argument('tweet_id', type=int, help='tweet ID')
    _parser.set_defaults(func=_delete)

    _parser = subparsers.add_parser('create', help='create tweet')
    _parser.add_argument('-s', '--silent', action='store_true',
        help='silent mode')
    _parser.add_argument('file', nargs='?', default=None, type=argparse.FileType('r'),
        help="file to tweet or '-' for stdin")
    _parser.set_defaults(func=_create)

    _parser = subparsers.add_parser('version', help='show version and exit')
    _parser.set_defaults(func=_version)

    args = parser.parse_args()
    if not hasattr(args, 'func'):
        parser.print_help()
        exit(1)
    args.func(args)


if __name__ == '__main__':
    main()
