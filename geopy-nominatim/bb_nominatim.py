#take an input and produce bounding box using Nominatim from OpenStreetMap
#this makes a kml file with the box in a transparent red color
#this is for Python 2.7, but will be moving to Python 3.6

#note: geopy/nominatim is currently changing for v.2 of the api, so it's warning against
#using a default user agent. I am assuming geopy will change for this, but for now
#just roll with the warning

from geopy.geocoders import Nominatim
import sys
import simplekml
import chardet
from django.utils.encoding import smart_str, smart_unicode

#these two lines will be required in the future - can't use default user agent anymore
from geopy.geocoders import options
options.default_user_agent = "your_user_agent_name"


geolocator = Nominatim()

#take named location directly from command line
#command form  is "python bb_nominatim.py "New York City" or...
#"python bb_nominatim.py "Brazil"

loc_name = sys.argv[1].encode('utf-8')
location = geolocator.geocode(loc_name, language = 'en')

#get bounding_box (geo_box) from location.raw
#this gives [South Latitude, North Latitude, West Longitude, East Longitude]
#for other things (twitter filtering for example) we need two corner points (WLong, SLat, ELong, NLat)

geo_box = location.raw[u'boundingbox']
twit_order = [0, 2, 1, 3]
twit_geo_box = [float(geo_box[i]) for i in twit_order]


print smart_unicode(location.raw[u'display_name'])
#display_name =  u''.join(location.raw[u'display_name']).encode('utf-16').strip()

print [float(x) for x in location.raw[u'boundingbox']]

#output to kml to test it

kml = simplekml.Kml()
b_box = kml.newgroundoverlay (name=loc_name)
b_box.color = '371400FF' #this is transparent red AABBGGRR (alpha, blue, green, red)
b_box.latlonbox.north = twit_geo_box[2]
b_box.latlonbox.south = twit_geo_box[0]
b_box.latlonbox.east = twit_geo_box[3]
b_box.latlonbox.west = twit_geo_box[1]

#save kml file with name based on the full location name
kml.save (smart_unicode(location.raw[u'display_name'].replace(', ', '-').replace(' ', '_') + '_bounding_box.kml'))
