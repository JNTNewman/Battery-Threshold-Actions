#!/usr/bin/env python3

#-------------- BATTERY THRESHOLD ACTIONS -------------#
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

from numpy import byte
import psutil
from plyer import notification
import time
import datetime
import os


config_file = "./bta.config"
icon_root = os.getcwd() + '/icons/'

while(True):
    battery = psutil.sensors_battery()
    percentage = round(battery.percent, 1)
    info = []

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            info.append(f.readline().split(';'))
            info = info[0]
            # print('Info = {}'.format(info))
            lt = int(info[1])
            ut = int(info[3])
            interval = int(info[5])
            print(lt, ut, interval, percentage)
        if(percentage >= ut and battery.power_plugged):
            info = "Your battery is now @ {}%. Please unplug.".format(
                percentage)
            notification.notify(
                title="Battery Notification",
                message=str("Your battery is now @ {}%. Please unplug.".format(percentage)), app_icon="/mnt/LinuxData/DevEnv/python/bta@jnt.newman/bta/icons/battery-full.png",
                timeout=10)
            print('\a')
        elif(percentage <= lt and not battery.power_plugged):
            notification.notify(
                title="Battery Notification",
                message=str("Your battery is now @ {}%. Please charge.".format(percentage)), app_icon="/mnt/LinuxData/DevEnv/python/bta@jnt.newman/bta/icons/battery-empty.png",
                timeout=10)
            print('\007')

        time.sleep(interval)

    except Exception as e:
        notification.notify(
            title="Battery Notification",
            message=str("There was and error: {}".format(e)), app_icon="./icons/battery-empty.png",
            timeout=10)
        # creating/opening a file
        # logger.error(e)
        current_timesamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        error_details = "There was an error at: {}\n\tType: {}.\n".format(current_timesamp, str(e))
        log_file = open("./error.log", "a")
        log_file.write(error_details)
        log_file.close()
        print(error_details, '\a')
        quit()

    continue
