import os
from calendar import timegm
from datetime import timedelta
from secrets import token_urlsafe
from time import gmtime
from typing import Any, Final, Sequence
from urllib.parse import urlencode

import dotenv
import tweepy
from flask import Flask, request, session, render_template
from werkzeug.middleware.proxy_fix import ProxyFix

from twofer import Database
from twofer.functools import time_limited_cache


# dotenv
dotenv.load_dotenv()
twofer_server_env = os.getenv('TWOFER_SERVER_ENV', 'twofer-server.env')
dotenv.load_dotenv(twofer_server_env)

# These environment values are requied and cannot be started without them.
TWITTER_CLIENT_ID = os.environ['TWOFER_TWITTER_CLIENT_ID']
TWITTER_CLIENT_SECRET = os.environ['TWOFER_TWITTER_CLIENT_SECRET']
TWITTER_BEARER_TOKEN = os.environ['TWOFER_TWITTER_BEARER_TOKEN']
FLASK_SECRET_KEY = os.environ['TWOFER_FLASK_SECRET_KEY']

# These values are set to its default when they are not explicitly set,
# you want to basically specify them though.
SERVER_HOST = os.getenv('TWOFER_SERVER_HOST', '127.0.0.1')
SERVER_PORT = int(os.getenv('TWOFER_SERVER_PORT', '8080'))
SERVER_GATEWAY_URL = os.getenv('TWOFER_SERVER_GATEWAY_URL', 'https://localhost')
SERVER_DATA_FILE = os.getenv('TWOFER_SERVER_DATA_FILE', 'twofer-server-data.json')
SERVER_OWNER = os.getenv('TWOFER_SERVER_OWNER', '_mshibata')
SERVER_MEMBERS = [x.strip() for x in os.getenv('TWOFER_SERVER_MEMBERS', '').split(',')]


# database
database: Final[Database] = Database(SERVER_DATA_FILE)
try:
    database.load()
except FileNotFoundError:
    pass


# Flask
app = Flask(__name__)
app.permanent_session_lifetime = timedelta(minutes=20)
app.secret_key = FLASK_SECRET_KEY
# Tell Flask it is Behind a Proxy — Flask Documentation (2.1.x)
# https://flask.palletsprojects.com/en/2.1.x/deploying/proxy_fix/
if SERVER_GATEWAY_URL:
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

_critical = app.logger.critical
_error = app.logger.error
_warning = app.logger.warning
_info = app.logger.info
_debug = app.logger.debug


# Tweepy
# OAuth 2.0 Authorization Code Flow with PKCE | Docs | Twitter Developer Platform
# https://developer.twitter.com/en/docs/authentication/oauth-2-0/authorization-code
oauth2_user_handler = tweepy.OAuth2UserHandler(
    client_id=TWITTER_CLIENT_ID,
    redirect_uri=f'{SERVER_GATEWAY_URL}/callback',
    scope=['tweet.read', 'tweet.write', 'users.read', 'follows.read', 'offline.access'],
    client_secret=TWITTER_CLIENT_SECRET
)


@time_limited_cache(7200)
def get_owner_user() -> tweepy.Response | None:

    if not SERVER_OWNER:
        return None

    app_client = tweepy.Client(TWITTER_BEARER_TOKEN)
    owner_res = app_client.get_user(username=SERVER_OWNER)
    return owner_res


@time_limited_cache(7200)
def owner_follwing_usernames() -> Sequence[str]:

    app_client = tweepy.Client(TWITTER_BEARER_TOKEN)
    owner = app_client.get_user(username=SERVER_OWNER)
    usernames = []
    next_token = None
    while True:
        res = app_client.get_users_following(owner.data['id'],
            max_results=1000, pagination_token=next_token)
        usernames.extend(u['username'] for u in res.data)
        next_token = res.meta.get('next_token')
        if not next_token:
            break
    return usernames


@time_limited_cache(300)
def get_user(user_token: str) -> tweepy.Response | None:

    if not user_token:
        return None

    try:
        client = ensure_unexpired_client(user_token)
        user_res = client.get_me(user_auth=False)
    except:
        return None
    return user_res


def validate_user(user_res: tweepy.Response, /) -> bool:

    username = user_res.data['username']
    valid = (
        (username == SERVER_OWNER)
        or (username in SERVER_MEMBERS)
        or (username in owner_follwing_usernames())
    )
    if not valid:
        _info(f'invalid user: {user_res}')

    return valid


def user_data_from_token_dict(token_dict: dict, /) -> dict[str, Any]:

    sec = timegm(gmtime())
    return {
        'access_token': token_dict['access_token'],
        'expires_at': sec + token_dict['expires_in'],
        'refresh_token': token_dict['refresh_token'],
    }


def ensure_unexpired_client(user_token: str, at_least_sec: int = 300, /) -> tweepy.Client | None:

    try:
        user_data: dict = database[user_token]
        access_token: str = user_data['access_token']
        expires_at: int = user_data['expires_at']
        refresh_token: str = user_data['refresh_token']
    except KeyError as e:
        _debug(f'KeyError: {e}')
        return None

    client = tweepy.Client(access_token)

    sec = timegm(gmtime())
    if expires_at - at_least_sec < sec:
        _debug(f'refresh token for {user_token}')
        query_str = urlencode({'grant_type': 'client_credentials'})
        refresh_url = f'https://api.twitter.com/2/oauth2/token?{query_str}'
        try:
            token_dict: dict = oauth2_user_handler.refresh_token(
                refresh_url, refresh_token, auth=oauth2_user_handler.auth)
            user_data = user_data_from_token_dict(token_dict)
        except:
            _info(f'refresh token for {user_token} failed')
            return None

        access_token: str = user_data['access_token']
        client = tweepy.Client(access_token)

        # check if the user is followed by the owner
        user_res = client.get_me(user_auth=False)
        if validate_user(user_res):
            database[user_token] = user_data
            database.save()
        else:
            _info('invalid user {user_res}')
            del database[user_token]
            database.save()
            return None

    return client


@app.route('/')
def index() -> Any:

    user_token = session.get('user_token')

    owner_res = get_owner_user()
    user_res = get_user(user_token)

    return render_template('index.html', owner=owner_res, user=user_res, user_token=user_token)


@app.route('/login')
def login() -> None:

    user_token = request.args.get('user_token')
    if user_token and (user_token in database):
        session['user_token'] = user_token
        session.permanent = True

    return app.redirect('/')


@app.route('/logout')
def logout() -> None:

    session.clear()

    return app.redirect('/')


@app.route('/authenticate')
def authenticate() -> Any:

    auth_url = oauth2_user_handler.get_authorization_url()
    return app.redirect(auth_url)


@app.route('/callback')
def callback() -> Any:

    user_token = session.get('user_token')
    if user_token in database:
        del database[user_token]
        database.save()
        session.clear()

    try:
        token_dict = oauth2_user_handler.fetch_token(request.url)
    except Exception as e:
        _info(f'callback() oauth2_user_handler.fetch_token failed: {e}')
        return ['Bad Request'], 400

    user_data = user_data_from_token_dict(token_dict)
    access_token: str = user_data['access_token']

    client = tweepy.Client(access_token)
    user_res = client.get_me(user_auth=False)
    if not validate_user(user_res):
        return ['Forbidden'], 403

    user_token = token_urlsafe()
    _debug(f'granted user_token {user_token} for {user_res}')
    database[user_token] = user_data
    database.save()

    session['user_token'] = user_token
    session.permanent = True

    return render_template('callback.html', user_token=user_token)


@app.route('/leave/<user_token>')
def leave(user_token: str) -> Any:

    try:
        user_data = database[user_token]
        access_token = user_data['access_token']
        query_str = urlencode({'access_token': access_token})
        url = f'https://api.twitter.com/2/oauth2/invalidate_token?{query_str}'
        oauth2_user_handler.post(url, auth=False)
    except:
        pass

    try:
        del database[user_token]
    except KeyError:
        pass
    database.save()

    session.clear()

    return app.redirect('/')


@app.route('/2/tweets/<tweet_id>', methods=['DELETE'])
def delete_tweet(tweet_id: str) -> Any:

    try:
        user_token = request.args['user_token']
    except KeyError as e:
        _debug(f'delete_tweet(): {e}')
        return ['Bad request'], 400

    client = ensure_unexpired_client(user_token)
    if client is None:
        return ['Bad request'], 400

    res = client.delete_tweet(tweet_id, user_auth=False)
    return {'data': res.data}


@app.route('/2/tweets', methods=['POST'])
def create_tweet() -> Any:

    try:
        user_token = request.args['user_token']
        data = request.get_json()
        text = data.get('text')
    except Exception as e:
        _debug(f'create_tweet(): {e}')
        return ['Bad request'], 400

    client = ensure_unexpired_client(user_token)
    if client is None:
        _debug('client is None')
        return ['Bad request'], 400

    res = client.create_tweet(text=text, user_auth=False)
    return {'data': res.data}


def main() -> None:
    app.run(SERVER_HOST, SERVER_PORT)


if __name__ == '__main__':
    main()
