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

scope = 'playlist-modify-public playlist-modify-private ugc-image-upload'

import typing as t
class Flasky(Flask):

    def __init__(
        self,
        import_name: str,
        static_url_path: t.Optional[str] = None,
        static_folder: t.Optional[str] = "static",
        static_host: t.Optional[str] = None,
        host_matching: bool = False,
        subdomain_matching: bool = False,
        template_folder: t.Optional[str] = "templates",
        instance_path: t.Optional[str] = None,
        instance_relative_config: bool = False,
        root_path: t.Optional[str] = None,
    ):
        super().__init__(import_name,
        static_url_path,
         static_folder,
         static_host,
         host_matching,
         subdomain_matching,
         template_folder,
        instance_path,
         instance_relative_config,
        root_path)

        self.sp = ''
        self.authd = False

# os.environ['SPOTIPY_CLIENT_SECRET'] = 'b6407e24d4e343d189a9d61590226f2a'
# os.environ['SPOTIPY_REDIRECT_URI'] = 'https://gring-fix.herokuapp.com/authd'
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://www.example.com'
# oauth = SpotifyOAuth(
#         scope = scope,
#         open_browser=False
#     )
# token = util.prompt_for_user_token(scope)
app = Flasky(__name__)

@app.route("/")
def get(stuff = None):
    if not app.authd:
        logging.warning('Need to auth')
        return redirect('/gen-token')

    # text = request.form['code']
    threading.Thread(target = wrapper, args=[]).start()
    return str(app.authd)

# @app.route("/authd")
# def getc(stuff = None):
#     if not app.authd:
#         logging.warning('Need to auth')
#         return redirect('/token')

#     text = request.form['code']
#     threading.Thread(target = wrapper, args=[]).start()
#     return str(app.authd)

# Raj:
# * Need a confirmed email, remove from PhD and put into masters, need SID
# * QCS: Ask about conflicting

@app.route("/gen-token")
def token():
    oauth = SpotifyOAuth(
            scope = scope,
            open_browser=False
        )

    auth_url = oauth.get_authorize_url()
    return render_template('my-form.html').replace('SHIT', auth_url)

@app.route('/gen-token', methods=['POST'])
def post():
    text = request.form['text']
    logging.warning('Ya hit the post!: {}'.format(text))
    
    # token = util.prompt_for_user_token(scope)
    # oauth = SpotifyOAuth(
    #         scope = scope,
    #         open_browser=False
    #     )
    # t = oauth.cache_handler.get_cached_token()

    oauth = LazyAuth(code = text)
    app.sp = spotipy.Spotify(oauth_manager=oauth)
    app.authd = True
    return redirect('/')
    # return '/'


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


import pathlib

def load_binary(filename):
    with open(next(pathlib.Path('.').glob('{}'.format(filename))), "rb") as img_file:
        return base64.b64encode(img_file.read())

def update():
    # username = 'stevenkordonowy1991@gmail.com'
    # test_playlist_id = '4gcOpHvPb7lTATlQXOISHy'
    test_playlist_id = '6IHTHqqxr7IOAfRkHIpFKd'
    test_name = 'Deployed practice!!!!!'

    # playlist_id = ''
    # name = 'Drifting Off'
    description = 'Let your mind wander with some Organic/Melodic House'

    try:
        app.sp.playlist_change_details(
            test_playlist_id,
            name = test_name,
            public = True,
            collaborative = False,
            description = description)

        logging.getLogger().setLevel('INFO')
        app.sp.playlist_upload_cover_image(
            playlist_id = test_playlist_id,
            image_b64 = load_binary('droff.jpg')
        )
        logging.getLogger().setLevel('DEBUG')
    except Exception as e:
        logger.error('RUH ROH\n{}'.format(e))


def wrapper():
    logging.warning('Lets kick this shit off')
    update()
    schedule.every(60).seconds.do(update)

    while True:
        schedule.run_pending()
        time.sleep(30)
        continue 

if __name__ == '__main__':
    logger.info('Trying for real!')

    app.run()

    