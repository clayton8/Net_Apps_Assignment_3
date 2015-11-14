import requests
import json
import argparse

# Used for getting lat and long from zip code
import geocoder

# Used for getting weather data
import pywapi

# Used for querying data from NASA
import cookielib
import urllib
import urllib2

# Used for text messaging
import smtplib
import time
import RPi.GPIO as GPIO
import pygame

LED = 15
GPIO.setmode(GPIO.BOARD)
GPIO.setup(int(LED), GPIO.OUT)
GPIO.output(int(LED),GPIO.LOW)


######################################################
##################### FUNCTIONS ######################
def location(zipcode):
    g = geocoder.google(zipcode)
    info = g.geojson
    data = g.latlng
    return data
    #print data

def notification(message):

    fromAddr = smtpUser

    subject = 'Data'
    header = 'To: ' + toAddr + '\n' + 'From: ' + fromAddr + '\n' + 'Subject: ' + subject

    s = smtplib.SMTP('smtp.gmail.com',587)

    s.ehlo()
    s.starttls()
    s.ehlo()

    s.login(smtpUser, smtpPass)
    s.sendmail(fromAddr, toAddr, header + '\n' + message)

    pygame.mixer.init()
    pygame.mixer.music.load("police_s.wav")
    pygame.mixer.music.play()

    GPIO.output(int(LED), GPIO.HIGH)
    time.sleep(1)
    GPIO.output(int(LED), GPIO.LOW)

    s.quit()

def parse_args():
    parser = argparse.ArgumentParser(description="Know viewable satellites given a zip code.")
    parser.add_argument("-s", "--satellite", required=True, help='Pass in satellite NORAD id number', type=str)

    parser.add_argument("-z", "--zipcode", required=True, help='Pass in zipcode for the observer', type=str)
    args = parser.parse_args()
    return args

def satellite_query(satellite_NORAD_id):
    # creates a cookie for the space-tracker server  with the credentials 
    # given at initialization. Define your credentials here
    access_user = 'clayton.kuchta@gmail.com'
    access_password = 'Vipers25!Vipers25!'

    # here is the URI login and query we try to access
    uri_login = 'https://www.space-track.org/ajaxauth/login'
    uri_quiry = 'https://www.space-track.org/basicspacedata/query/class/tle/NORAD_CAT_ID/'+ str(satellite_NORAD_id) + '/limit/1/format/tle'

    # Trying login on space-track server
    cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    data = {'identity': access_user, 'password': access_password}
    ldata = urllib.urlencode(data)
    opener.open(uri_login, ldata)

    # Qury data 
    sat_data = opener.open(uri_quiry)
    return sat_data.read()

##################### FUNCTIONS ######################
######################################################


# arguments (args.satellite and args.zipcode to access)
args = parse_args()
print "Inputs:\n    Satellite = "+ args.satellite + "\n    Zipcode = " + args.zipcode + "\n\n"

# Lat and longitude of input
observer_location = location(args.zipcode)

# Get weather
#weather =  pywapi.get_weather_from_weather_com(args.zipcode)
#print "Weather: ", weather['current_conditions']['text']

# Sending a text message
d =  "Latitude and Longitude from zipcode " + args.zipcode + " = " + str(observer_location)
print 'trying to send: \n    "' + d + '"' + '\n'
notification(d)
print 'sent message\n\n'

# Querying data NASA
print "Querying data from Space-Tracker.org with NORAD id of: " + args.satellite + "\n"
satellite_query_data = satellite_query(args.satellite)
print "Data Recieved:\n" + satellite_query_data + "\n\n"

