#!/usr/bin/env python
from __future__ import division

"""
Simple module face detect
"""

__version__ = '0.0.1'
__copyright__ = "Copyright 2015, Marc Cobos"
__author__  = 'coboshernandez@gmail.com'


import cv2
import sys
import math
import os
import configparser
import json
import datetime
import uuid
import urllib2

config = configparser.ConfigParser();
config_aux = configparser.ConfigParser();

config.read(os.path.abspath(os.path.join(os.path.dirname(__file__),'config.ini')));

class RingBuffer:
    def __init__(self, size):
        self.data = [None for i in xrange(size)]

    def append(self, x):
        self.data.pop(0)
        self.data.append(x)

    def get(self):
        return self.data


def internet_on(host, port):
    try:
        response=urllib2.urlopen('http://' + host + ':' + port ,timeout=20);
        return True
    except Exception as err: return False


def diffImg(t0, t1):
    dif = cv2.absdiff(t0, t1).sum()
    ncomponents = len(t0[0]) * len(t0)
    return (dif / 254.0 * 100) / ncomponents



def main(argv=None):
    faces_buff = RingBuffer(8)
    motion_buff = RingBuffer(8)
    current_milli_time = lambda: int(round(time.time() * 1000))

    eyes=os.path.abspath(os.path.join(os.path.dirname(__file__),'cam/haarcascade_eye.xml'))
    fac =os.path.abspath(os.path.join(os.path.dirname(__file__),'cam/haarcascade_frontalface_alt.xml'))

    eye = cv2.CascadeClassifier(eyes)
    cascade = cv2.CascadeClassifier(fac)

    now = datetime.datetime.now()
    now_plus_30 = now + datetime.timedelta(minutes = 30)

    video_capture = cv2.VideoCapture(0)
    count_frames = 0;

    mac = "%12x" % uuid.getnode()

    fname = '/tmp/impacte_measure.json'

    if not os.path.isfile(fname):
        data = {'data':[]}
        with open(fname, 'w') as outfile:
            json.dump(data, outfile)


    t = cv2.cvtColor(video_capture.read()[1], cv2.COLOR_BGR2GRAY)

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        percent_difference = diffImg(t, gray)
        motion_buff.append(percent_difference)
        #sys.stdout.flush() 
        
        t = gray

        rects = cascade.detectMultiScale(frame, 2, 2, minSize=(80,80))

        eyes = eye.detectMultiScale(
            gray,
            scaleFactor=2.2,
            minNeighbors=1,
            minSize=(20, 20),
            maxSize=(25,25)
        )

        
        #count frames 
        count_frames += 1

        #list_faces_2 = []
        #for (x,y, w, h) in rects:
            #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            #aux = [x,y,w,h];
            #list_faces_2.append(aux)

        faces = 0

        #quit overlaped eyes
        quit_over = []
        for i, (x, y, w, h) in enumerate(eyes):
            is_correct = 1;
            if i == 0:
                aux = [x,y,w,h]
                quit_over.append(aux)
            else:
                for j, (x_2, y_2, w_2, h_2) in enumerate(quit_over):
                    if ((x < x_2 and x + 20 > x_2) or (x - 20 < x_2 and x >= x_2)) and ((y >= y_2 and y - 5 <= y_2) or (y < y_2 and y + 5 >= y_2)):
                        is_correct = 0;
                        break
                    else:
                        for k, (x_f, y_f, w_f, h_f) in enumerate(rects):
                            if((x+w > x_f) or (x > x_f) and (y+h) > y_f or (y > y_f)):
                                is_correct = 0;
                                break;
                if is_correct == 1:
                    aux = [x,y,w,h]
                    quit_over.append(aux)

        list_true_faces = []
        for i, (x,y,w,h) in enumerate(quit_over):
            for j, (x_aux, y_aux, w_aux, h_aux) in enumerate(quit_over):
                if i < j:
                    if ((x < x_aux and x + 100 > x_aux) or (x - 100 < x_aux and x >= x_aux)) and ((y >= y_aux and y - 8 <= y_aux) or (y < y_aux and y + 8 >= y_aux)):
                        #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                        #cv2.rectangle(frame, (x_aux, y_aux), (x_aux+w, y_aux+h), (0, 0, 255), 2)
                        faces += 1

        #quit overlaped faces
        faces_over = []
        for i, (x, y, w, h) in enumerate(rects):
            is_correct = 1;
            if i == 0:
                aux = [x,y,w,h]
                faces_over.append(aux)
                #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            else:
                for j, (x_2, y_2, w_2, h_2) in enumerate(faces_over):
                    if ((x < x_2 and x + w > x_2) or (x - w < x_2 and x >= x_2)) and ((y >= y_2 and y - h <= y_2) or (y < y_2 and y + h >= y_2)):
                        is_correct = 0;
                        break
                if is_correct == 1:
                    #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    aux = [x,y,w,h]
                    faces_over.append(aux)


        
        faces_buff.append(faces + len(faces_over))
        if count_frames == 8:
            faces = abs(math.ceil(sum(faces_buff.get()) / float(len(faces_buff.get())) - 0.40))
            motion = abs(math.ceil(sum(motion_buff.get()) / len(motion_buff.get())))
            if faces > 0:
                i = datetime.datetime.now()

                config.read(os.path.abspath(os.path.join(os.path.dirname(__file__),'config.ini')));
                config_aux.read(os.path.abspath(os.path.join(os.path.dirname(__file__),'config-aux.ini')));
                
                if config['DEFAULT']['active'] == '1':
                    a_dict = {'createdAt': str(i), 'people': str(faces), 'mac': str(mac), 'itemId': str(config_aux['DEFAULT']['playing_now']), 'type': 'impact'}
                    with open(fname) as f:
                        data = json.loads(f.read())

                    data['data'].append(a_dict)

                    with open(fname, 'w') as f:
                        json.dump(data, f, separators=(',',':'))

            if motion > 3:
                i = datetime.datetime.now()
                config.read(os.path.abspath(os.path.join(os.path.dirname(__file__),'config.ini')));
                config_aux.read(os.path.abspath(os.path.join(os.path.dirname(__file__),'config-aux.ini')));
                
                if config['DEFAULT']['active'] == '1':
                    a_dict = {'createdAt': str(i), 'motion': str(motion), 'mac': str(mac), 'itemId': str(config_aux['DEFAULT']['playing_now']), 'type': 'motion'}
                    with open(fname) as f:
                        data = json.loads(f.read())

                    data['data'].append(a_dict)

                    with open(fname, 'w') as f:
                        json.dump(data, f, separators=(',',':'))
                        

            if (faces == 0 and motion <= 3):
                now = datetime.datetime.now()
                if now > now_plus_30 and len(data['data']) > 0:
                    config.read(os.path.abspath(os.path.join(os.path.dirname(__file__),'config.ini')));
                    if internet_on(config['DEFAULT']['host'], config['DEFAULT']['port']):
                        #try:
                        req = urllib2.Request('http://' + config['DEFAULT']['host'] +':'+ config['DEFAULT']['port'] + '/api/set_impact')
                        req.add_header('Content-Type', 'application/json');
                        
                        with open(fname) as f:
                            data = json.loads(f.read())

                        data_send = {'statistics' : data['data']};
                        response = urllib2.urlopen(req, json.dumps(data_send));

                        now_plus_30 = now + datetime.timedelta(minutes = 30)

                        data_clean = {'data':[]}
                        with open(fname, 'w') as f:
                            json.dump(data_clean, f, separators=(',',':'))

                        #except Exception as err:
                        #    print err

            count_frames = 0


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything is done, release the capture
    video_capture.release()
    #cv2.destroyAllWindows()

    return

if __name__ == "__main__":
    sys.exit(main())

