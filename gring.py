import logging
import time
import base64
import requests
import pathlib
import schedule

import spotipy
from spotipy import util
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials, SpotifyStateError
from flask import Flask, redirect, request, render_template
import requests as req
import threading
import os


logger = logging.getLogger('green-ring-fix')
logging.basicConfig(level='DEBUG')

scope = 'playlist-modify-public playlist-modify-private ugc-image-upload user-follow-read'

app = Flask(__name__)
# app.config['SECRET_KEY'] = os.urandom(64)
# app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SESSION_FILE_DIR'] = './.flask_session/'
# Session(app)

# caches_folder = './.spotify_caches/'
# if not os.path.exists(caches_folder):
#     os.makedirs(caches_folder)

# def session_cache_path():
#     return caches_folder + session.get('uuid')

@app.route("/")
def get():
    threading.Thread(target = wrapper).start()
    return 'Hello Clarice'
    # oauth = SpotifyOAuth(
    #         scope = scope,
    #         # client_secret = app_secret,
    #         # client_id = app_id,
    #         # redirect_uri = redirect_uri,
    #         open_browser=False
    #     )

    # auth_url = oauth.get_authorize_url()

    # # t = 
    # return render_template('my-form.html').replace('SHIT', auth_url)

@app.route('/', methods=['POST'])
def post():
    print('Ya hit the post!')
    text = request.form['text']
    threading.Thread(target = wrapper).start()
    return 'All is well... for now....'


class LazyAuth(SpotifyOAuth):
    def __init__(self, code, client_id=None, client_secret=None, redirect_uri=None, state=None, scope=None, cache_path=None, username=None, proxies=None, show_dialog=False, requests_session=True, requests_timeout=None, open_browser=True, cache_handler=None
    ):
        print('Super cool auth')
        super().__init__(
            client_id,
        client_secret, redirect_uri
        , state, scope, cache_path, username, proxies, show_dialog, requests_session, requests_timeout, open_browser, cache_handler)

        self.code = code

    def get_auth_response(self, open_browser=None):
        return self.code


def kickoff_stuff(text):
    oauth = LazyAuth(
            code = text,
            scope = scope,
            open_browser=False
        )

    sp = spotipy.Spotify(
        auth_manager = oauth
    )

    test_playlist_id = '4gcOpHvPb7lTATlQXOISHy'

    description = 'Let your mind wander with some Organic/Melodic House'

    c = 0
    while True:
        name = 'FUCKYOU{}'.format(c)
        try:
            sp.playlist_change_details(
                test_playlist_id,
                name = name,
                public = True,
                collaborative = False,
                description = description)

            sp.playlist_upload_cover_image(
                playlist_id = test_playlist_id,
                image_b64 = load_binary('droff.jpg')
            )
            print('done with {}'.format(c))
            c += 1
        except Exception as e:
            logger.error('RUH ROH\n{}'.format(e))

        time.sleep(30)


import pathlib

def load_binary(filename):
    with open(next(pathlib.Path('.').glob('{}'.format(filename))), "rb") as img_file:
        return base64.b64encode(img_file.read())

def update(duck):
    username = 'stevenkordonowy1991@gmail.com'
    test_playlist_id = '4gcOpHvPb7lTATlQXOISHy'
    description = 'Let your mind wander with some Organic/Melodic House'

    token = util.prompt_for_user_token(username, scope)
    sp = spotipy.Spotify(auth=token)

    name = 'Dawg{}'.format(duck + 1)
    try:
        sp.playlist_change_details(
            test_playlist_id,
            name = name,
            public = True,
            collaborative = False,
            description = description)

        logging.getLogger().setLevel('INFO')
        sp.playlist_upload_cover_image(
            playlist_id = test_playlist_id,
            image_b64 = load_binary('droff.jpg')
        )
        logging.getLogger().setLevel('DEBUG')
    except Exception as e:
        logger.error('RUH ROH\n{}'.format(e))

    duck += 1

def wrapper():
    duck = 1
    update(duck)
    schedule.every(60).seconds.do(update, duck)

    while True:
        schedule.run_pending()
        time.sleep(30)
        continue 

if __name__ == '__main__':
    logger.debug('HELLO!!!')    
    # f = '{}/{}'.format(pathlib.Path().resolve().as_uri(), 'ball.jpg')
    # load_binary(f)
    # app_id = '68e489df7f1b4cef9d6a69cc8a0b649a'
    # app_secret = 'b6407e24d4e343d189a9d61590226f2a'
    # redirect_uri = 'http://www.example.com'
    # os.environ['SPOTIPY_CLIENT_SECRET'] = 'b6407e24d4e343d189a9d61590226f2a'
    # os.environ['SPOTIPY_REDIRECT_URI'] = 'https://gring-fix.herokuapp.com'
    # app.run()
    p = pathlib.Path('.')
    print(list(p.glob('**/*.jpg')))
    wrapper()

    