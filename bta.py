#!/usr/bin/env python3

#------------- BATTERY THRESHOLD ACTIONS  -------------#
#													   #
# To help ensure longevity of your laptop battery,     #
#  this python based utility was created to check      #
# battery levels at intervals and notify either to     #
#          plug out or to plug in and charge.          #
#													   #
#           ~~~ John Newman @JNTNewman ~~~             #
#          ~~~ john.nt.newman@gmail.com ~~~            #
#													   #
#------------------------------------------------------#

import psutil
from plyer import notification
import time
import datetime
import os


program_path = os.getcwd()
config_file = program_path + '/bta.config'
icon_root = program_path + '/icons/'
event_file = program_path + '/event.log'
log_file = program_path + '/error.log'

while(True):
    battery = psutil.sensors_battery()
    percentage = round(battery.percent, 1)
    info = []
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            info.append(f.readline().split(';'))
            info = info[0]
            lt = int(info[1])
            ut = int(info[3])
            interval = int(info[5])
            # with open(event_file, "a") as f:
            #     current_timesamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            #     log_details = "{}: Lower Threshold = {}; Upper Threshold = {}; Current Battery Level = {}%.\n".format(current_timesamp, lt, ut, percentage)
            #     f.write(log_details)
            #     f.close()
        if(percentage >= ut and battery.power_plugged):
            print('\a')
            info = "Your battery is now @ {}%. Please unplug.".format(
                percentage)
            notification.notify(
                title="Battery Notification",
                message=str("Your battery is now @ {}%. Please unplug.".format(percentage)), app_icon=icon_root + '/battery-full.png',
                timeout=10)
        elif(percentage <= lt and not battery.power_plugged):
            print('\a')
            notification.notify(
                title="Battery Notification",
                message=str("Your battery is now @ {}%. Please charge.".format(percentage)), app_icon=icon_root + '/battery-empty.png',
                timeout=10)
        time.sleep(interval)

    except Exception as e:
        notification.notify(
            title="Battery Notification",
            message=str("{}".format(e)), app_icon=icon_root + '/exclamation-triangle-solid.png',
            timeout=10)
        current_timesamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        error_details = "{}: {}.\n".format(current_timesamp, str(e))
        log = open(log_file, "a")
        log.write(error_details)
        log.close()
        quit()

    continue
