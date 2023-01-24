from ipaddress import ip_address

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db=firestore.client()

'''import requests


r= requests.get('https://get.geojs.io/')
ip_address=requests.get('https://get.geojs.io/v1/ip.json')

ipAdd = ip_address.json()['ip']
print(ipAdd)

url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
geo_request = requests.get(url)
geo_data= geo_request.json()
print(geo_data)'''

db.collection('persons').add({'name':'dylan','age':23})

# importing geopy library
from geopy.geocoders import Nominatim
# calling the Nominatim tool
loc = Nominatim(user_agent="GetLoc")
# entering the location name
try:
    getLoc = loc.geocode("museum, bulawayo,zimbabwe")
    # printing address
    print(getLoc.address)

    # printing latitude and longitude
    print("Latitude = ", getLoc.latitude, "\n")
    print("Longitude = ", getLoc.longitude)
    print("///////////////////////////////////////////////////////////")
except:
    print("sorry there was an error")    
# importing modules
from geopy.geocoders import Nominatim

# calling the nominatim tool
geoLoc = Nominatim(user_agent="GetLoc")

# passing the coordinates
locname = geoLoc.reverse("-17.815, 31.0478")

# printing the address/location name
print("the address is ",locname.address)
