# Contains GMAIL account passoword and the email you want to text
import personal_data

import requests
import json

# Contains GMAIL account passoword, the email you want to text
# and space-tracks.org login info. It is in the git ignore so we 
# will not accidently add it.
import personal_data

# Used for simulation
import time

# Used for satellite prediction times
import datetime

# Used to translate between rad and degrees
import math

# Used for parsing arguments
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

LED = 15

# Used for tracking satellite
import ephem

# Attempt to import libraries to use the Raspberry Pi's
# GPIO pin and the headphone jack.
PLAY_SOUND = True
USE_GPIO = True
try:
    import pygame
except ImportError:
    print "WARNING COULD NOT IMPORT 'pygame' so not using sound"
    PLAY_SOUND = False

try:
    import RPi.GPIO as GPIO
except ImportError:
    print "WARNING COULD NOT IMPORT 'RPi.GPIO' so not using GPIO"
    USE_GPIO = False

# Default to true until we read in the args later
SEND_TEXT_MESSGE = True
LED = 15

















######################################################
##################### FUNCTIONS ######################
def GPIO_setup():
    """
        Attemps to setup GPIO pins if the library
        was installed correctly.
    """
    if(USE_GPIO):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(int(LED), GPIO.OUT)
        GPIO.output(int(LED),GPIO.LOW)
    

def location(zipcode):
    """
        Generates a latitude and longitude depending
        on a US zipcode.
    """
    g = geocoder.google(zipcode)
    info = g.geojson
    data = g.latlng
    print data
    return_data = {'latitude': data[0], 'longitude': data[1]}
    return return_data

def send_text(message):
    """
        Sends a text message with a particular message to a 
        user. It utilizes texting though emails. So to do this 
        all you have to do is add your own Gmail accound info
        and an email address you want to send to.
    """

    # Setup sending information
    smtpUser = personal_data.get_username()
    toAddr = personal_data.get_phone_number()
    smtpPass = personal_data.get_password() 
    fromAddr = smtpUser

    subject = 'Data'
    header = 'To: ' + toAddr + '\n' + 'From: ' + fromAddr + '\n' + 'Subject: ' + subject

    # Setup data to be sent
    subject = ''
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
   
    for i in range(0, (len(message)/160) + 1):
        msg = ""
        if(len(message) > 145):
            msg = message[0:145]
        else:
            msg = message
        s.sendmail(fromAddr, toAddr, header + '\n' + msg)
        message = message[145:]
    s.quit()
    
def make_sound(sound_file):
    """
        Plays audio file through headphone jack
        in Raspberry Pi.
    """
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()
    
    
def blink_LED():
    """
        Blins an LED for 1 second on a Raspberry Pi
    """
    GPIO.output(int(LED), GPIO.HIGH)
    time.sleep(1)
    GPIO.output(int(LED), GPIO.LOW)
    


def notification(message):
    """
        Sends all three notifications depending on global
        variables. Text messaging is enabled with '-t' 
        where as the other two check to see if the libraries 
        are availible.
    """
    if SEND_TEXT_MESSGE:
        send_text(message)
    if PLAY_SOUND: 
        make_sound("police_s.wav")
    if USE_GPIO:
        blink_LED()


def parse_args():
    """
        Used to parse arguments. Add here if you want any more options
    """
    parser = argparse.ArgumentParser(description="Know viewable satellites given a zip code.")
    parser.add_argument("-s", "--satellite", required=True, help='Pass in satellite NORAD id number', type=str)
    parser.add_argument("-z", "--zipcode", required=True, help='Pass in zipcode for the observer', type=str)
    parser.add_argument("-t", "--text", action='store_false', help='Flag whether or not you want to send a text message')
    parser.add_argument("--sim", action='store_false', help='Flag whether or not you want to run the simmulation')
    args = parser.parse_args()
    return args

def satellite_query(satellite_NORAD_id):
    # creates a cookie for the space-tracker server  with the credentials 
    # given at initialization. Define your credentials here
    access_user = personal_data.get_space_tracks_username()
    access_password = personal_data.get_space_tracks_password()


    # here is the URI login and query we try to access
    uri_login = 'https://www.space-track.org/ajaxauth/login'
    uri_quiry = 'https://www.space-track.org/basicspacedata/query/class/tle/NORAD_CAT_ID/'+ str(satellite_NORAD_id) + '/limit/1/format/tle'
    """
        Querey's space-track.org database for most recent trl data
        by the norad id.
    """

    # creates a cookie for the space-tracker server  with the credentials 
    # given at initialization. Define your credentials here
    access_user =  personal_data.get_space_tracks_username()
    access_password = personal_data.get_space_tracks_password()

    # here is the URI login and query we try to access
    uri_login = 'https://www.space-track.org/ajaxauth/login'
    uri_quiry = 'https://www.space-track.org/basicspacedata/query/class/tle_latest//ORDINAL/1/NORAD_CAT_ID/'+ str(satellite_NORAD_id) + '/format/3le'

    # Trying login on space-track server
    cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    data = {'identity': access_user, 'password': access_password}
    ldata = urllib.urlencode(data)
    opener.open(uri_login, ldata)

    # Qury data 
    sat_data = opener.open(uri_quiry)
    return sat_data.read()

def datetime_from_time(tr):
    """
        Translates ephem.Date into datetime object
    """
    year, month, day, hour, minute, second = tr.tuple()
    dt = datetime.datetime(year, month, day, hour, minute, int(second))
    return dt

def weather_is_clear(time, weather):
    """
        KARA: Please fill in this function. A datetime object is passed in 
              if you need more informtion, please see where it is called from
              and pass in variables that you need. It is called in the function
              right below this one 'satellite_visible.' That function is called in
              'satellite_finder.' If you need latitude and longitude the 'obs' object 
              has latitude and longitude if you call 'obs.lat' and 'obs.long'
    """
    date = datetime.datetime.now()

    """compare_date = time.days
    print 'compare date: ', compare_date.date"""
    
    delta = time - date
    delta_date = delta.days
    if(delta_date < 15 and delta_date >= 0):
        if(weather[delta_date] == 'Clear'):
            return True
        else:
            return False
    return True

def satellite_visible(sat, sun, time, weather):
    """
        Checks for 3 things to see if the satellite is visible:
            1. Satellite is not ecliped by the Eath
            2. The sun is at the right angle so the satellite can
               reflect the light to the observer
            3. The weather is not cloudy.
    """
    if sat.eclipsed is False and math.degrees(sun.alt) < -6  and math.degrees(sun.alt) > -16 and weather_is_clear(time,weather):
        return True
    else:
        return False

def convert_azimuth(azimuth):
    """
        Azimuth is esentuallly the degrees on a compass.
        This funciton converts radians into N, S, E, and W
        values
    """
    deg_azi = math.degrees(azimuth)

    if deg_azi < 11.25 or deg_azi >= 348.75:
        return "N"
    elif deg_azi < 33.75:
        return "NNE"
    elif deg_azi < 56.25:
        return "NE"
    elif deg_azi < 78.75:
        return "ENE"
    elif deg_azi < 101.25:
        return "E"
    elif deg_azi < 123.75:
        return "ESE"
    elif deg_azi < 146.25:
        return "SE"
    elif deg_azi < 168.75:
        return "SSE"
    elif deg_azi < 191.25:
        return "S"
    elif deg_azi < 213.75:
        return "SSW"
    elif deg_azi < 236.25:
        return "SW"
    elif deg_azi < 258.75:
        return "WSW"
    elif deg_azi < 281.25:
        return "W"
    elif deg_azi < 303.75:
        return "WNW"
    elif deg_azi < 326.25:
        return "NW"
    elif deg_azi < 348.75:
        return "NNW"
     

def satellite_finder(obs, sat, weather):
    """
        Function which takes an observer and
        a satellite and finds 5 instances in which
        the observer will be able to see the satellite.
        It returns a list of dictionaries, which hold information
        about the satellite sighting.
    """
    
    sun = ephem.Sun()
    sun.compute(obs)
    sat.compute(obs)
    
    start_view_time = ""
    end_view_time = ""
    visible = False

    number_times_visible = 0
    viewing_times = []

    # Loop through finding different times the satellite will pass
    # and if it is visible add it to the list. We will collect
    # 5 different satallite viewable times
    while len(viewing_times) < 5:   
        # Get the next time the satellite will be visible
        rise_time, rise_azimuth, maximum_alt_time, maximum_alt, set_time, set_azimuth = obs.next_pass(sat)
        # Now loop through while the satellite is above the horrizon
        # one second at a time and check to see if the satellite is
        # visible according math.
        while rise_time < set_time:
            obs.date = rise_time
            sun.compute(obs)
            sat.compute(obs)
            if satellite_visible(sat, sun, datetime_from_time(ephem.Date(rise_time)),weather):
                # In here if it is visible
                if visible is False:
                    # First time it was marked visible during this pass so append a new object to viewing_times
                    time = datetime_from_time(ephem.Date(rise_time))
                    new_event = {'start':time, 'end':time, 'azi_start':rise_azimuth, 'azi_end': set_azimuth, 'max_alt': maximum_alt}
                    viewing_times.append(new_event)
                else:
                    # Not first time marked visible during this pass so just update the 'end' time
                    time = datetime_from_time(ephem.Date(rise_time))
                    viewing_times[-1]['end'] = time

                visible = True
            elif visible is True:
                # Was previously marked visible so update theedn time and break 
                # out of the loop because we will assume the satellite will not become
                # visible atain in this pass
                time = datetime_from_time(ephem.Date(rise_time))
                viewing_times[-1]['end'] = time
                rise_time = set_time
            rise_time = ephem.Date(rise_time + 1.0 * ephem.second)
        
        obs.date = rise_time + ephem.minute
        visible = False
    return viewing_times

def make_satellite_message_phone(obj):
    """ 
        Pretty basic function just creates the text message to 
        help clean up other parts of the code
    """
    duration = obj['end'] - obj['start'] 
    message = "Viewing in 15 minutes!\n\n" 
    message = message + "You can see the satellite at: " + str(obj['start']) + " (UTC)\n"
    message = message + "Duration: " + str(duration) + "\n"
    message = message + "Starting from: " + str(math.degrees(obj['azi_start'])) + " (" + convert_azimuth(obj['azi_start']) + ")\n"
    message = message + "Going to: " + str(math.degrees(obj['azi_end'])) + " (" + convert_azimuth(obj['azi_end']) + ")\n"
    message = message + "Maximum altitude of: " + str(math.degrees(obj['max_alt'])) + "\n"
    return message

def time_simulation(satellite_viewing_list):
    """
        Takes in the object from 'satellite_finder; and will simulate 
        from 15 minutes and 10 seconds out, down to the 15 minute
        alert which should set off all alerts, sound, light, and text.
    """
    for view in satellite_viewing_list:
        print "SIMULATING EVENT"
        print
        curr_time = view['start'] - datetime.timedelta(minutes=15, seconds=10)
        
        while (view['start'] - curr_time) > datetime.timedelta(minutes=15):
            print "Curent time: " + str(curr_time)
            time.sleep(1)
            curr_time = curr_time + datetime.timedelta(seconds=1)
        
        print "\nIT IS NOW 15 MINUTES BEFORE A VIEWING!!!\n"
        
        text_message = make_satellite_message_phone(view)
        print "Sending out this text message: \n\n" + text_message + "\n\n"

        notification(text_message)

##################### FUNCTIONS ######################
######################################################




# Setup GPIO pins if the library exits
GPIO_setup()

# arguments (args.satellite and args.zipcode to access)
args = parse_args()

print "================================================================"
print
print "Inputs:\
       \n    Satellite  = "+ args.satellite + \
      "\n    Zipcode    = " + args.zipcode + \
      "\n    Send Text  = " + str(args.text) + \
      "\n    Simulaiton = " + str(args.sim)
print
print "================================================================"

SEND_TEXT_MESSGE = args.text

# Lat and longitude of input
observer_location = location(args.zipcode)
print "================================================================"
print
print "Oberserver's location is: " + str(observer_location)
print
print "================================================================"

print "================================================================"
print
print "Gathering wather data"
print

# Get weather
API_KEY = '1847401faa199ef4462fd85742bc1759'
LAT = str(observer_location['latitude'])
LONG = str(observer_location['longitude'])

to_get_weather = 'http://api.openweathermap.org/data/2.5/forecast/daily?lat=' + LAT + '&lon=' + LONG + '&cnt=16&mode=json&&appid=' + API_KEY
f = urllib2.urlopen(to_get_weather)

forecast = f.read()
f_json = json.loads(forecast)
list_of_data = f_json['list']
weather_list = []
for i in range(0,15):
    w = list_of_data[i]
    weather_list.append(w['weather'])
weather = []
for j in range(0,15):
    q = weather_list[j]
    r = q[0]
    data = r['main']
    weather.append(data)
    
print 'weather list: \n\n', weather
print
print "================================================================"



# Querying NASA data 
print "================================================================"
print
print "Querying data from Space-Tracker.org with NORAD id of: " + args.satellite + "\n"

satellite_query_data = satellite_query(args.satellite)
tle_array = satellite_query_data.split('\r\n')

print "Data Recieved:\n" + satellite_query_data
print
print "================================================================"


# Create the observer object
observer = ephem.Observer()
observer.lat  = str(observer_location['latitude'])
observer.long = str(observer_location['longitude'])
observer.horizon = '-0.34'

# Create the Satellite object
satellite = ephem.readtle(tle_array[0], tle_array[1], tle_array[2])



print "================================================================"
print
print "Gathering satellite data and finding when the satellite will be viewable"
satellite_viewing_list = satellite_finder(observer, satellite, weather)

print
print "================================================================"


print "================================================================"
print
print "Found " + str(len(satellite_viewing_list)) + " viewable times"

for view in satellite_viewing_list:
    duration = view['end'] - view['start']
    print
    print "    Start viewing time: " + str(view['start']) + " (UTC)"
    print "    End viewing time:   " + str(view['end'])   + " (UTC)"
    print "    Duration:           " + str(duration)
    print "    Starting from:      " + str(math.degrees(view['azi_start'])) + " degrees azimuth (" + convert_azimuth(view['azi_start']) + ")"

    print "    Going to:           " + str(math.degrees(view['azi_end'])) + " degrees azimuth (" + convert_azimuth(view['azi_end']) + ")"
    print "    Maximum altitude:   " + str(math.degrees(view['max_alt'])) + " degrees"

print
print "================================================================"

if args.sim:
    print "================================================================"
    print
    print "Simulating setting time to 15 minutes and 10 seconds before " + \
          "each satellite viewing to show alerts work correctly"
    print
    print
    time_simulation(satellite_viewing_list)

    print
    print "================================================================"



