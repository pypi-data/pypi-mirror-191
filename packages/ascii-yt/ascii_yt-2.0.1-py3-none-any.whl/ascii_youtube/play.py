import os, sys
from time import sleep
from . import ascii_frames as af
from pkg_resources import require

# get the package requirements
require("opencv-python==4.7.0.68")
import cv2

require("pafy-tmsl>=0.5.6")
import pafy


YT_HOSTNAME = 'https://www.youtube.com'

def play(url, size=None, replay=False, chars="", colors=False):
    print('Loading..')

    # check if it's a youtube URL
    if url.startswith(YT_HOSTNAME):
        try: 
            url = pafy.new(url).getbest(preftype="mp4").url
        except OSError:
            # handle the connection error
            af.raise_error((f"check your connection.. ⚠️"))
    else:
        af.raise_error((f"this URL is not a youtube video like \"{YT_HOSTNAME}..\""))
    
    vidcap = cv2.VideoCapture(url)
    os.system("clear")
    DELAY = 0.01

    while True:
        success, frame = vidcap.read()
        if success:
            print("\x1b[H" + af.image2ascii(frame, size, chars, colors))
            sleep(DELAY)
        elif replay: 
            vidcap = cv2.VideoCapture(url)
        else: 
            return

