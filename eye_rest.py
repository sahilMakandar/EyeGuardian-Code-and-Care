
import time

import os
import subprocess
import argparse
from plyer import notification
import pygame
import numpy as np
import json

from PIL import Image
import cv2
from screeninfo import get_monitors


os.environ['DBUS_SESSION_BUS_ADDRESS'] = 'unix:path=/run/user/1000/bus'

os.environ['DISPLAY']=':1.0' 


def get_screen_resolution():
    try:
        monitors = get_monitors()
        
        if monitors:
            # Assuming the first monitor is the primary monitor
            primary_monitor = monitors[0]
            width = primary_monitor.width
            height = primary_monitor.height
            return width, height
        else:
            return None
    except Exception as e:
        print(e)
        return None


def create_blank_image(screen_width, screen_height):
    # Create a blank white image with the specified screen resolution
    image = Image.new('RGB', (screen_width, screen_height), color='black')
    image.save('black_blank_screen.png')

def is_monitor_on():
    try:
        result = subprocess.check_output(['/usr/bin/xset', '-q']).decode('utf-8')
        # print(result)
        return "Monitor is On" in result
    except subprocess.CalledProcessError:
        print("Error: xset command not found.")
        return None
    
def is_audio_playing_linux():
    try:
        output = subprocess.check_output(['pacmd', 'list-sink-inputs'])
        return b'1 sink input(s)' in output

    except subprocess.CalledProcessError:
        return False

def show_blank_screen(rest_minut, screen_width, screen_height):
    # Display a notification every 20 minutes
    time.sleep(rest_minut * 60)

    # Create a black image
    black_image = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)

    notification_title = "Eye Rest Reminder"
    notification_message = "Take a 20-second break and look at something 20 feet away!"
    
    # notify when moniter is on
    if (is_monitor_on()):
        notification.notify(
            title=notification_title,
            message=notification_message,
            app_name="EyeRestReminder",
            timeout=20  # Notification will automatically disappear after 10 seconds
        )
        cv2.namedWindow("Black Screen", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("Black Screen", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
        cv2.imshow("Black Screen", black_image)
        cv2.waitKey(20000)
        cv2.destroyAllWindows()


def play_beep_sound(beep_mp3_file, sound_level=0.03, rest_minut=20):
    
    # Display a notification every 20 minutes
    time.sleep(rest_minut * 60)

    notification_title = "Eye Rest Reminder"
    notification_message = "Take a 20-second break and look at something 20 feet away!"

    # hint = {"resident":False}
        
    # notify when moniter is on
    if (is_monitor_on()):
        notification.notify(
            title=notification_title,
            message=notification_message,
            app_name="EyeRestReminder",
            timeout=20,   # Notification will automatically disappear after 10 seconds
            # hints=hint
        )

        is_audio_playing = is_audio_playing_linux()
        # print(is_audio_playing)

        # beep notification when audio is not palying
        if (is_audio_playing == False):
            try:
                pygame.mixer.init()
                pygame.mixer.music.load(beep_mp3_file)  # You can replace "beep.mp3" with the path to your desired sound file
                pygame.mixer.music.set_volume(sound_level)
                pygame.mixer.music.play() 
                time.sleep(20)  
                # Stop the music forcefully after 20 sec
                pygame.mixer.music.stop()
                pygame.mixer.quit()
            except Exception as e:
                print(e)


def display_notification(rest_minut):
    time.sleep(rest_minut * 60)

    notification_title = "Eye Rest Reminder"
    notification_message = "Take a 20-second break and look at something 20 feet away!"
    
    # notify when moniter is on
    if (is_monitor_on()):
        notification.notify(
            title=notification_title,
            message=notification_message,
            app_name="EyeRestReminder",
            timeout=20  # Notification will automatically disappear after 10 seconds
        )

def eye_rest_reminder(rest_minut, option_taken, sound_file_path, sound_level, config_file_path):

    config = {}

    # check config file is exist
    check_file = os.path.exists(config_file_path)

    # Get the screen resolution
    screen_size = get_screen_resolution()


    if screen_size:
        screen_width, screen_height = screen_size
        xvfb_command = f'Xvfb :1 -screen 0 {screen_width}x{screen_height}x16 &'
        os.system(xvfb_command)
        print(f"Xvfb started with screen width: {screen_width} and height: {screen_height}.")
    else:
        print("No monitors found. Seeting to default beep sound")

    
    while True:

        if check_file:
            with open(config_file_path) as config_file:
                config = json.load(config_file)
                option_taken = config.get("notify_option", "beep_sound")
                if option_taken not in ['notification', 'blank_screen', 'beep_sound']:

                    notification_title = "Wrong Notification Option For Eye Rest Reminder"
                    notification_message = "Wrong option in eye_rest_config.json. Please set between ['notification', 'blank_screen', 'beep_sound']!"
                    option_taken = "beep_sound"

                    # notify when moniter is on
                    if (is_monitor_on()):
                        notification.notify(
                            title=notification_title,
                            message=notification_message,
                            app_name="EyeRestReminder",
                            timeout=20,   # Notification will automatically disappear after 10 seconds
                        )
                    

                sound_level = config.get("sound_level", 0.02)
                if sound_level < 0 and sound_level > 1:
                    sound_level = 0.02

                sound_file_path = config.get("sound_file_path", "sound_files/beep.mp3")
                is_file_exist = os.path.exists(sound_file_path)
                if is_file_exist == False:
                    user_home = os.environ.get('HOME')
                    sound_file_path = user_home + "/eye_rest_project/sound_files/beep.mp3"

                app_running_status = config.get("app_running_status", True)
                if app_running_status == False:

                    notification_title = "App Running Status For Eye Rest Reminder"
                    notification_message = "in eye_rest_config.json you seted app_running_status as False. Please make this as true reset notifcations on!"

                    notification.notify(
                        title=notification_title,
                        message=notification_message,
                        app_name="EyeRestReminder",
                        timeout=20  # Notification will automatically disappear after 10 seconds
                        )
                    exit(0)
                if screen_size == None:
                    option_taken = "beep_sound"


        if option_taken == 'notification':
            display_notification(rest_minut)
        elif option_taken == 'blank_screen':
            show_blank_screen(rest_minut, screen_width, screen_height)
        elif option_taken == 'beep_sound':
            play_beep_sound(sound_file_path, sound_level, rest_minut)
        else:
            print("Invalid option. Please choose 'notification', 'blank_screen', 'beep_sound', or 'exit'.")

    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Eye Rest Reminder Options")
    parser.add_argument('option', choices=['notification', 'blank_screen', 'beep_sound'], default='beep_sound', help="Choose the reminder option")
    parser.add_argument('--duration', type=int, default=20, help="Duration of reminder in seconds (default is 20)")

    args = parser.parse_args()

    # Default options if config file is failed
    option_taken = args.option
    
    rest_minut = 20
    
    sound_level = 0.5
    
    user_home = os.environ.get('HOME')
    config_file_path = user_home + "/eye_rest_project/eye_rest_config.json"
    sound_file_path = user_home + "/eye_rest_project/sound_files/beep.mp3"

    eye_rest_reminder(rest_minut, option_taken, sound_file_path, sound_level, config_file_path)





