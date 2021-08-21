
import pigpio 
import pytz
import schedule
import time
import math
import struct
import fileinput
import sys
import re
from astral import Astral
from dateutil import parser
from datetime import datetime
from datetime import timedelta
from colour import Color

#www.perbang.dk/rgbgradient

def hex_to_rgb(value):
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3],16) for i in range(0, lv, lv // 3 ))

def runLights():
        city_name = 'London'
        a = Astral()
        a.solar_depression = 'civil'
        city = a[city_name]
        timezone = city.timezone        
        now = datetime.now(pytz.utc)    
        sun = city.sun(date=now, local=True)    
        dawn = sun['dawn']
        inbetweenTestYES = sun['sunrise']
        dusk = sun['dusk']
        sunset = sun['sunset']
        print(now)
        ######
        #colours
        ######
        day = Color('#28FCFF')
        evening = Color('#FF0000')
        #SETTING PINS
        red = 17
        green = 24
        blue = 22       
        #checking what minute past the hour it is
        timeDiffInMins = (now - sunset).total_seconds() / 60
        timeDiffInMins = int(math.floor(timeDiffInMins))
        sunsetDuskDuration = (dusk - sunset).total_seconds() / 60       
        sunsetDuskDuration = int(math.floor(sunsetDuskDuration))
        
        if sunset < now < dusk:
                timeDiffInMins = int(math.floor(timeDiffInMins))        
                sunsetColours = list(day.range_to(Color(evening),sunsetDuskDuration)) #can replace this number with the number of minutes it takes for sunset
                newList = []
        
                for index in range(len(sunsetColours)):
                        string = str(sunsetColours[index])              
                        noHash = string.replace('#', '') #6-digit hex code with no hash
                        noHash = string.replace(' ', '') #re-adds the hash to use to unpack
                        #print(index)
                        newList.insert(index, noHash) #add new hex value to list

                for t in newList:
                        #if the number of minutes into sunset equals the index number plus one
                        
                        if timeDiffInMins == newList.index(t)+1:
                                pi = pigpio.pi()
                                print('t')
                                rgbNoBrackets = str(t)
                                h = rgbNoBrackets.replace('(', '')
                                h = h.replace(')', '')
                                h = h.split(',')                                
                                Rn = h[0]
                                hexi = Rn.lstrip('#')                           
                                hexLen = len(hexi)
                                rgb = hex_to_rgb(hexi)                          
                                #print(rgb)                             
                                pi.set_PWM_dutycycle(green, rgb[0])
                                pi.set_PWM_dutycycle(red, rgb[1])
                                pi.set_PWM_dutycycle(blue, rgb[2])
                                pi.stop()
                                
                        else:
                                nothing = 'uselessString'
                        
        else:
                print('OFF')
                #print('Now:    %s' % now)
                #print('Dawn:   %s' % str(sun['dawn']))
                #print('Sunset: %s' % str(sun['sunset']))
                #print('Sunrise: %s' % str(sun['sunrise']))
                #print('Dusk:   %s' % str(sun['dusk']))

schedule.every(1).seconds.do(runLights)

while 1:
        schedule.run_pending()
        time.sleep(5)
