#!/usr/bin/env python3
import sys
import os
import re
from camera import Camera
from flask import Flask, render_template, Response

home=os.getenv('HOME')

MY_INDEX=3
pattern=r"WEB_SHOW3_PORT=(.*)"

f=open(home + '/lib/CONFIG', 'r');
str = f.read()
f.close()

matchs = re.finditer(pattern, str)
for match in matchs:
    MY_PORT=match.groups()[0]

app = Flask(__name__)

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera(MY_INDEX)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    args = sys.argv
    app.run(host='0.0.0.0', debug=False, threaded=True, port=int(MY_PORT))
