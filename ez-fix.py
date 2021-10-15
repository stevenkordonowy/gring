import pathlib
import base64
import spotipy
from spotipy import util
import time
import datetime
import os
from flask import Flask, jsonify, request
# from flask_executor import Executor
import logging
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import sys

app = Flask(__name__)
# executor = Executor(app)
executor = ThreadPoolExecutor(2)

logger = logging.getLogger('green-ring-fix')
logging.basicConfig(level='INFO')

def pprint(t):
    logger.info('{}: {}'.format(datetime.datetime.now(), t))

def load_binary(filename):
    with open(next(pathlib.Path('.').glob('{}'.format(filename))), "rb") as img_file:
        return base64.b64encode(img_file.read())

@app.route('/')
def index():
    return 'Well hello!'

@app.route('/start')
def kickoff():
    # executor.submit(mainy)
    # thing = executor.submit(mainy)
    # thing.result()
    # return 'Scheduled a job'

    thread = Thread(target=mainy)
    thread.daemon = True
    thread.start()
    return jsonify({'thread_name': str(thread.name), 'started': True})

@app.route('/kill')
def kill():
    pprint('You want to kill me eh?')
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Et tu, Brute?'

def update(spotty, playlist_id, name, description, img):
    pprint('Updating playlist \'{}\''.format(name))
    spotty.playlist_change_details(
        playlist_id,
        name = name,
        public = True,
        collaborative = False,
        description = description)

    spotty.playlist_upload_cover_image(
        playlist_id = playlist_id,
        image_b64 = img
    )

def mainy():
    email = 'rwelch1919@gmail.com'

    # Spotify API
    scope = 'playlist-modify-public playlist-modify-private ugc-image-upload'
    token = util.prompt_for_user_token(scope=scope, username=email)
    sp = spotipy.Spotify(auth=token)
    
    # Playlist Args
    playlist_id = '7KikO7RiLTvBn3L5scILhO'
    name = 'Drifting Off'
    description = 'Let your mind wander with some Organic & Melodic House'
    img = load_binary('droff.jpg')

    while True:
        try:
            update(
            spotty=sp,
            playlist_id=playlist_id,
            name=name,
            description=description,
            img=img
        )
        except Exception as e:
            pprint('Error updating\n{}'.format(e))
            pprint('Attempting to regenerate token')
            token = util.prompt_for_user_token(scope=scope, username=email)
            sp = spotipy.Spotify(auth=token)

        time.sleep(60)
        continue 



def mainy2(email):
    # Spotify API
    scope = 'playlist-modify-public playlist-modify-private ugc-image-upload'
    token = util.prompt_for_user_token(scope=scope, username=email)
    sp = spotipy.Spotify(auth=token)
    
    # Playlist Args
    playlist_id = '7KikO7RiLTvBn3L5scILhO'
    name = 'Drifting Off'
    description = 'Let your mind wander with some Organic & Melodic House'
    img = load_binary('droff.jpg')

    update(
        spotty=sp,
        playlist_id=playlist_id,
        name=name,
        description=description,
        img=img
    )


if __name__ == '__main__':
    # import sys
    # if len(sys.argv) != 2:
    #     raise ValueError('Please provide email')

    # email = sys.argv[1]

    os.environ['SPOTIPY_CLIENT_SECRET'] = 'b6407e24d4e343d189a9d61590226f2a'
    os.environ['SPOTIPY_REDIRECT_URI'] = 'http://www.example.com'
 
    pprint('Running gring-fix')
    # executor.submit(mainy, email)
    # print('Past submit')
    # thing.result()
    
    app.run()

    # mainy2(email)

    

    