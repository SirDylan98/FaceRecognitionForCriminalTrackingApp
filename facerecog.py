import cv2
from matplotlib import image
import numpy as np
import face_recognition


imgelon = face_recognition.load_image_file('images/elon1.jpg')
imgelon = cv2.cvtColor(imgelon,cv2.COLOR_BGR2RGB)

imgelontest = face_recognition.load_image_file('images/elon2.jpg')
imgelontest = cv2.cvtColor(imgelontest,cv2.COLOR_BGR2RGB)

faceLoc = face_recognition.face_locations(imgelon)[0]# to get the location of the image 
encodeElon = face_recognition.face_encodings(imgelon)[0]
cv2.rectangle(imgelon,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)

faceLoc = face_recognition.face_locations(imgelontest)[0]
encodeElontest = face_recognition.face_encodings(imgelontest)[0] # encoding the image so that the svm algorithm can work on it 
cv2.rectangle(imgelontest,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)

results = face_recognition.compare_faces([encodeElon],encodeElontest) #Used to compare test image with known pictures
faceDis = face_recognition.face_distance([encodeElon],encodeElontest)
print(faceDis)
print(results)

cv2.imshow("Elon musk",imgelon)
cv2.imshow("Elon musk test img",imgelontest)
cv2.waitKey(0)