import cv2
import sys
from time import sleep
from utils import *
import math


eyes='haarcascade_eye.xml'
fac ='haarcascade_frontalface_alt.xml'
faces_buff = RingBuffer(20)

eye = cv2.CascadeClassifier(eyes)
cascade = cv2.CascadeClassifier(fac)

video_capture = cv2.VideoCapture(0)
count_frames = 0;

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    
    rects = cascade.detectMultiScale(frame, 2, 1, minSize=(80,80))



    eyes = eye.detectMultiScale(
        gray,
        scaleFactor=3,
        minNeighbors=1,
        minSize=(20, 20),
        maxSize=(25,25)
    )

    
    #count frames 
    count_frames += 1

    list_faces_2 = []
    for (x,y, w, h) in rects:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        aux = [x,y,w,h];
        list_faces_2.append(aux)

    #buf.append(eyes)
    faces = 0
    list_faces = []
    #num_old_correct = 0
    for (x, y, w, h) in eyes:
        aux = [x,y,w,h];
        list_faces.append(aux)

    #quit overlaped eyes
    quit_over = []
    for i, (x, y, w, h) in enumerate(list_faces):
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
                    for k, (x_f, y_f, w_f, h_f) in enumerate(list_faces_2):
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
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                    cv2.rectangle(frame, (x_aux, y_aux), (x_aux+w, y_aux+h), (0, 0, 255), 2)
                    faces += 1


    
    faces_buff.append(faces + len(list_faces_2))
    if count_frames == 20:
        faces = math.ceil(sum(faces_buff.get()) / float(len(faces_buff.get())))
        sys.stdout.write('\r' + "Num of faces:" + str(faces) + ' ' * 20)
        sys.stdout.flush() # important
        count_frames = 0

    # Display the resulting frame
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()

