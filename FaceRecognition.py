from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label

from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.logger import Logger

import cv2
import numpy as np
import face_recognition
import os
import datetime 

path = 'images'
images=[]
ClassNames=[]
myList = os.listdir(path)
print(myList)

#Build App and layout

class CamApp(App):
    def build(self):
        for cl in myList:
            curImg =cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            ClassNames.append(os.path.splitext(cl)[0])
        print(ClassNames)    

        self.img1=Image(size_hint=(1,.8))
        self.button=Button(text="Verify",size_hint=(1,.1) )
        self.verificafication=Label(text="Verification .......", size_hint=(1,.1))

        layout=BoxLayout(orientation='vertical')
        layout.add_widget(self.img1)
        layout.add_widget(self.button)
        layout.add_widget(self.verificafication)

        #setup video capture
        self.capture=cv2.VideoCapture(0)
        Clock.schedule_interval(self.update,1.0/33.0)

        return layout

    def findencodings(self,image):
        encodingList=[]
        for img in image:
            img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            encode=face_recognition.face_encodings(img)[0]
            encodingList.append(encode)
        return encodingList      

    # to run continously
    def update(self,*args):
        encodedknownfaces = self.findencodings(images)
        ret,frame = self.capture.read()
        frame=frame[120:250+290,100:350+250,:] 

        buf=cv2.flip(frame,0).tostring()
        img_texture=Texture.create(size=(frame.shape[1],frame.shape[0]),colorfmt='bgr')
        img_texture.blit_buffer(buf,colorfmt='bgr', bufferfmt='ubyte')
        self.img1.texture=img_texture

        #imgS=cv2.resize(self.capture,(0,0),None,0.25,0.25)
        imgS=cv2.cvtColor(self.capture,cv2.COLOR_BGR2RGB)

        faceCurFrame = face_recognition.face_locations(imgS)# to get the location of the image 
        encodeCurFrame = face_recognition.face_encodings(imgS,faceCurFrame)

        for encodeFrame,faceLoca in zip(encodeCurFrame,faceCurFrame):
            print("Yes sir we are getting into the loop")
            matches = face_recognition.compare_faces(encodedknownfaces,encodeFrame)
            faceDis= face_recognition.face_distance(encodedknownfaces,encodeFrame)
            matchindex =np.argmin(faceDis)

            print (faceDis)
            if matches[matchindex]:
                name=ClassNames[matchindex].upper()
                y1,x2,y2,x1=faceLoca
                y1,x2,y2,x1= y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(self.img1,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(self.img1,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(self.img1,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                print(name)
                """First connect the script to firebase"""
                """THis is where we get the location of the device and time and save it to firebase """
                datenow = datetime.datetime.today()
                print(datenow)
         

if __name__=='__main__':
    CamApp().run()    


 
