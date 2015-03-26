import cv2
import sys
from time import sleep

nose='Nariz.xml'
mouth='Mouth.xml'
frontal_face='haarcascade_frontalface_alt_tree.xml'
eyes='frontalEyes35x16.xml'


frontal_face = cv2.CascadeClassifier(frontal_face)
mouth = cv2.CascadeClassifier(mouth)
nose = cv2.CascadeClassifier(nose)
eyes = cv2.CascadeClassifier(eyes)

video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = frontal_face.detectMultiScale(
        frame,
        scaleFactor=3,
        minNeighbors=2,
        minSize=(30, 30),
        maxSize=(500,500)
    )

    mouthes = mouth.detectMultiScale(
        frame,
        scaleFactor=3,
        minNeighbors=2,
        minSize=(10, 10),
        maxSize=(200,200)
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
       cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

       # Draw a rectangle around the faces
    for (x, y, w, h) in mouthes:
       cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)
    sys.stdout.write('\r' + "Num of faces:" + str(len(faces)) + ' ' * 20)
    sys.stdout.flush() # important

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
