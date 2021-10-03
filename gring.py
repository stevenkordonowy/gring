# https://github.com/plamere/spotipy/blob/master/examples/change_playlist_details.py

import logging
import time
import base64

import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

logger = logging.getLogger('green-ring-fix')
logging.basicConfig(level='DEBUG')

scope = 'playlist-modify-public playlist-modify-private'

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

def main():
    # args = get_args()
    app_id = '68e489df7f1b4cef9d6a69cc8a0b649a'
    app_secret = 'b6407e24d4e343d189a9d61590226f2a'
    # redirect_uri = 'http://localhost:8000'

    auth = SpotifyClientCredentials(
            client_secret = app_secret,
            client_id = app_id
        )

    token = auth.get_access_token()

    sp = spotipy.Spotify(
        # auth_manager = SpotifyOAuth(
        #     scope = scope,
        #     client_secret = app_secret,
        #     client_id = app_id,
        #     redirect_uri = redirect_uri
        # )

        auth = token['access_token'],
        auth_manager = auth,
        client_credentials_manager=auth
    )

    test_playlist_id = '4gcOpHvPb7lTATlQXOISHy'

    description = 'Let your mind wander with some Organic/Melodic House'

    c = 0
    while True:
        name = 'wellwtf{}'.format(c)
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
    main()