from sre_constants import SUCCESS
import cv2
import numpy as np
import face_recognition
import os
import datetime
from ipaddress import ip_address
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from geopy.geocoders import Nominatim
import random

############################### DATABASE CONNECTION and Global variables ##############################################################
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
dataG = {"name": "Tanaka", "age": 55}
############################################### FUNCTIONS#############################################################################


def findencodings(image):  # function to encode  of the images loaded from the folder
    encodingList = []
    for img in image:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # converting it to rbg
        encode = face_recognition.face_encodings(img)[0]  # encoding the image
        encodingList.append(encode)
    return encodingList    # this is the list of the encoded faces


def randomlocation():
    mylocations = ["Msu, Gweru, Zimbabwe",
                   "Pick n pay, gweru, zimbabwe ",
                   "cbz , Harare, zimbabwe",
                   "UZ, Harare,zimbabwe",
                   "parirenyatwa hospital, Harare, zimbabwe",
                   "hellenic school, Harare, zimbabwe",
                   "zbc , harare zimbabwe",
                   "ecobank, Harare,zimbabwe",
                   "holiday inn, Bulawayo,zimbabwe",
                   "sports club, Bulawayo,zimbabwe",
                   ]
    print(random.choice(mylocations))
    return random.choice(mylocations)


def geocodingfunc():
    try:
        loc = Nominatim(user_agent="GetLoc")
        # entering the location name
        currentloc = randomlocation()
        getLoc = loc.geocode(currentloc)
        datenow = datetime.datetime.today()  # timestamp to get
        date_time = datenow.strftime("%m/%d/%Y, %H:%M:%S")
        # printing address
        print(getLoc.address)

        print("Latitude = ", getLoc.latitude, "\n")
        print("Longitude = ", getLoc.longitude)
        dataG["name"]=name.lower()
        dataG["lat"]=getLoc.latitude
        dataG["long"]=getLoc.longitude
        dataG["address"]=getLoc.address
        dataG["timestamp"]=date_time
        
        return {"lat": getLoc.latitude,
                "long": getLoc.longitude,
                "address": getLoc.address,
                "datetime":date_time}#  returning the geo code of the location 
    except:
        pass


def getdocs(id):
    result = db.collection("spottedsuspects").document(id).get()
    if result.exists:
        print(result.to_dict())
        spotteddata = result.to_dict()
        print("This is my suspects  dictionary", spotteddata)
        spottedaddr = geocodingfunc()
        print("This is my address dictionary", spottedaddr)
        if spotteddata["address"] == spottedaddr["address"]:
            pass
        else:
            db.collection("spottedsuspects").document(id).update(
                {"lat": spottedaddr["lat"], "long": spottedaddr["long"], "address": spottedaddr["address"]})
            docs = db.collection("suspects").get()
            for doc in docs:
                if doc.to_dict()["name"] == name.lower():
                    key = doc.id
                    try:
                        db.collection("suspects").document(key).update(
                        {"recentlocation": firestore.ArrayUnion([spottedaddr])})
                        print("douments created successfully")
                        # we also want to update the locatoin
                    except:
                        print("Could not saved Most likely due to network issues")    
            # get the correct suspect document and append the new location to the array
            # db.collection("spottedsuspects").document(id).get()
        # check if the address is already stored
    else:
        spottedaddr1=geocodingfunc()
        try:
            db.collection("spottedsuspects").document(id).set(dataG)
            print("document saved!!!!!!!!!!!!!!!!!!!!!!!!!")
            
        except:
            print("Could not saved Most likely due to network issues")    


def setdoc(id):
    pass


############################################### END FUNCTIONS #####################################################################################################
geocodingfunc()
path = 'images'  # path to our image file in the same directory
images = []  # array to store our suspects images
ClassNames = []  # array to store the names of the suspects
myList = os.listdir(path)
print(myList)
######################## Reading the Images from folder##################################################
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)  # adding and image in the loop
    # getting the names using string manipulation
    ClassNames.append(os.path.splitext(cl)[0])

print(ClassNames)
########################## Encoding the images that were read######################################################################

# assigning the list to encodedknownfaces
encodedknownfaces = findencodings(images)
print(len(encodedknownfaces))  # just printing the length of the array

#################################### Getting the live feed from web cam###################################################################################

cap = cv2.VideoCapture(0)


while True:
    success, img = cap.read()  # reading the frames from our webcame
    # img=
    # resizing the images to 25% width and hiegth
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    # Converting the image to rgb format for processing
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(
        imgS)   # to get the location of the image
    encodeCurFrame = face_recognition.face_encodings(
        imgS, faceCurFrame)  # to encode the areas of face location

    # now we are comparing the knownencodedfaces vs the encoded on the current frame
    for encodeFrame, faceLoca in zip(encodeCurFrame, faceCurFrame):
        print("Yes sir we are getting into the loop")
        matches = face_recognition.compare_faces(
            encodedknownfaces, encodeFrame)
        # gets the deviation distance from true value
        faceDis = face_recognition.face_distance(
            encodedknownfaces, encodeFrame)
        # the index with smallest faceDistance is the most probable
        matchindex = np.argmin(faceDis)

        print(faceDis)
        if matches[matchindex]:  # now getting the name of the face on the index with the min faceDis
            name = ClassNames[matchindex].upper()
            y1, x2, y2, x1 = faceLoca  # getting the coordinates for the face
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            # drawing the rectangle around the recognized faces
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1+6, y2-6),
                        cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
            print(name)
            getdocs(name)
            """First connect the script to firebase"""
            """THis is where we get the location of the device and time and save it to firebase """
            datenow = datetime.datetime.today()  # timestamp to get
            date_time = datenow.strftime("%m/%d/%Y, %H:%M:%S")
            print(date_time)

    cv2.imshow("Webcam", img)
    cv2.waitKey(1)
