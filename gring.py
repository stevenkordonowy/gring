# https://github.com/plamere/spotipy/blob/master/examples/change_playlist_details.py

import logging
import time

import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

logger = logging.getLogger('green-ring-fix')
logging.basicConfig(level='DEBUG')

scope = 'playlist-modify-public playlist-modify-private'

def main():
    # args = get_args()
    app_id = '68e489df7f1b4cef9d6a69cc8a0b649a'
    app_secret = 'b6407e24d4e343d189a9d61590226f2a'
    redirect_uri = 'http://127.0.0.1:9090'

    sp = spotipy.Spotify(
        # auth_manager = SpotifyOAuth(
        #     scope = scope,
        #     client_secret = app_secret,
        #     client_id = app_id,
        #     redirect_uri = redirect_uri
        # )

        auth_manager = SpotifyClientCredentials(
            # scope = scope,
            client_secret = app_secret,
            client_id = app_id
            # redirect_uri = redirect_uri
        )
    )

    test_playlist_id = '4gcOpHvPb7lTATlQXOISHy'

    c = 0
    while True:
        name = 'deployed-idiot{}'.format(c)
        try:
            sp.playlist_change_details(
                test_playlist_id,
                name = name,
                public = True,
                collaborative = False,
                description = 'Just playin')
            print('done with {}'.format(c))
            c += 1
        except Exception as e:
            logger.error('RUH ROH\n{}'.format(e))

        time.sleep(60)


if __name__ == '__main__':
    logger.debug('HELLO!!!')
    main()