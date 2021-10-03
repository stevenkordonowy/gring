# https://github.com/plamere/spotipy/blob/master/examples/change_playlist_details.py

import logging
import time
import base64

import spotipy
from spotipy import util
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials, SpotifyStateError
from flask import Flask, redirect, request, render_template
import requests as req
import threading

logger = logging.getLogger('green-ring-fix')
logging.basicConfig(level='DEBUG')

# scope = 'playlist-modify-public playlist-modify-private ugc-image-upload'
scope = 'playlist-modify-public playlist-modify-private user-library-read streaming'

app = Flask(__name__)

@app.route("/")
def hello():
    app_id = '68e489df7f1b4cef9d6a69cc8a0b649a'
    app_secret = 'b6407e24d4e343d189a9d61590226f2a'
    redirect_uri = 'http://www.example.com'

    client_auth = SpotifyClientCredentials(
            client_secret = app_secret,
            client_id = app_id
        )

    oauth = SpotifyOAuth(
            scope = scope,
            client_secret = app_secret,
            client_id = app_id,
            redirect_uri = redirect_uri,
            open_browser=False
        )

    auth_url = oauth.get_authorize_url()

    f = redirect(auth_url)

    return f

@app.route("/f")
def my_form():
    app_id = '68e489df7f1b4cef9d6a69cc8a0b649a'
    app_secret = 'b6407e24d4e343d189a9d61590226f2a'
    redirect_uri = 'http://www.example.com'

    oauth = SpotifyOAuth(
            scope = scope,
            client_secret = app_secret,
            client_id = app_id,
            redirect_uri = redirect_uri,
            open_browser=False
        )

    auth_url = oauth.get_authorize_url()

    t = render_template('my-form.html').replace('SHIT', auth_url)
    return t

@app.route('/f', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.upper()
    # auth = LazyAuth(processed_text,
    #     scope = scope,
    #     client_secret = app_secret,
    #     client_id = app_id,
    #     redirect_uri = redirect_uri,
    #     open_browser=False,
    #     cache_handler=cache)
    threading.Thread(target = kickoff_stuff, args = [text]).start()
    return processed_text

# @app.route('/')
# def user(name):
#     return f"Your name is {name}"

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

class LazyAuth(SpotifyOAuth):
    

    def __init__(self, code, client_id=None, client_secret=None, redirect_uri=None, state=None, scope=None, cache_path=None, username=None, proxies=None, show_dialog=False, requests_session=True, requests_timeout=None, open_browser=True, cache_handler=None
    ):
        print('Super cool auth')
        super().__init__(client_id,
        client_secret, redirect_uri, state, scope, cache_path, username, proxies, show_dialog, requests_session, requests_timeout, open_browser, cache_handler)

        self.code = code

    def get_auth_response(self, open_browser=None):
        # r = super().get_auth_response(open_browser)
        # return r

        return self.code
        

    def _get_auth_response_interactive(self, open_browser=False):
        # r = super()._get_auth_response_interactive(open_browser)
        # return r
        
        # url = self.get_authorize_url()
        # prompt = (
        #         "Go to the following URL: {}\n"
        #         "Enter the URL you were redirected to: ".format(url)
        #     )
        # response = self._get_user_input(prompt)
        # state, code = SpotifyOAuth.parse_auth_response_url(response)
        # if self.state is not None and self.state != state:
        #     raise SpotifyStateError(self.state, state)
        return self.code


def kickoff_stuff(text):
    print('Well looky here:{}'.format(text))
    # args = get_args()
    app_id = '68e489df7f1b4cef9d6a69cc8a0b649a'
    app_secret = 'b6407e24d4e343d189a9d61590226f2a'
    redirect_uri = 'http://www.example.com'

    cache = spotipy.cache_handler.MemoryCacheHandler('obvsnot')

    oauth = LazyAuth(
            code = text,
            scope = scope,
            client_secret = app_secret,
            client_id = app_id,
            redirect_uri = redirect_uri,
            open_browser=False,
            cache_handler=cache
        )

    sp = spotipy.Spotify(
        auth_manager = oauth

        # auth = token,
        # auth_manager = auth,
        # client_credentials_manager=auth
    )


    test_playlist_id = '4gcOpHvPb7lTATlQXOISHy'

    description = 'Let your mind wander with some Organic/Melodic House'

    c = 0
    while True:
        name = 'deployit{}'.format(c)
        try:
            sp.playlist_change_details(
                test_playlist_id,
                name = name,
                public = True,
                collaborative = False,
                description = description)

            # sp.playlist_upload_cover_image(
            #     test_playlist_id,
            #     get_base64_encoded_image('droff.jpg')
            # )
            print('done with {}'.format(c))
            c += 1
        except Exception as e:
            logger.error('RUH ROH\n{}'.format(e))

        time.sleep(60)


if __name__ == '__main__':
    logger.debug('HELLO!!!')
    # app.run(host='localhost', port=9874)
    app.run()
    # main('hi')