import logging
import time
import base64
import requests
import pathlib

import spotipy
from spotipy import util
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials, SpotifyStateError
from flask import Flask, redirect, request, render_template
import requests as req
import threading


logger = logging.getLogger('green-ring-fix')
logging.basicConfig(level='DEBUG')

scope = 'playlist-modify-public playlist-modify-private ugc-image-upload'

app = Flask(__name__)

@app.route("/")
def get():
    # app_id = '68e489df7f1b4cef9d6a69cc8a0b649a'
    # app_secret = 'b6407e24d4e343d189a9d61590226f2a'
    # redirect_uri = 'http://www.example.com'

    oauth = SpotifyOAuth(
            scope = scope,
            # client_secret = app_secret,
            # client_id = app_id,
            # redirect_uri = redirect_uri,
            open_browser=False
        )

    auth_url = oauth.get_authorize_url()

    t = render_template('my-form.html').replace('SHIT', auth_url)
    return t

@app.route('/', methods=['POST'])
def post():
    print('Ya hit the post!')
    text = request.form['text']
    threading.Thread(target = kickoff_stuff, args = [text]).start()
    return 'All is well... for now....'


def load_binary(filename):
    return base64.b64encode(requests.get(filename).content).decode("utf-8")

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
    print('Well looky here:{}'.format(text))
    # args = get_args()
    app_id = '68e489df7f1b4cef9d6a69cc8a0b649a'
    app_secret = 'b6407e24d4e343d189a9d61590226f2a'
    redirect_uri = 'http://www.example.com'

    # cache = spotipy.cache_handler.MemoryCacheHandler('obvsnot')

    oauth = LazyAuth(
            code = text,
            scope = scope,
            client_secret = app_secret,
            client_id = app_id,
            redirect_uri = redirect_uri,
            open_browser=False
        )

    sp = spotipy.Spotify(
        auth_manager = oauth
    )

    test_playlist_id = '4gcOpHvPb7lTATlQXOISHy'

    description = 'Let your mind wander with some Organic/Melodic House'

    c = 0
    while True:
        name = 'newdeplo{}'.format(c)
        try:
            # sp.playlist_change_details(
            #     test_playlist_id,
            #     name = name,
            #     public = True,
            #     collaborative = False,
            #     description = description)

            sp.playlist_upload_cover_image(
                test_playlist_id,
                load_binary('file://ball.jpg')
            )
            print('done with {}'.format(c))
            c += 1
        except Exception as e:
            logger.error('RUH ROH\n{}'.format(e))

        time.sleep(60)


if __name__ == '__main__':
    logger.debug('HELLO!!!')
    f = '{}/{}'.format(pathlib.Path().resolve().as_uri(), 'ball.jpg')
    load_binary(f)
    app.run()