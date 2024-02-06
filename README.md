# EyeGuardian-Code-and-Care
Created special Python script for you called "EyeGuardian." It's not just about coding; it's your buddy for taking care of your eyes while you code. Let's check out the awesome features that make EyeGuardian your go-to companion for both coding and eye care.

# Features of EyeGuardian:

## Multi-Mode Notifications:

### Simple Notification Mode:
Receive gentle reminders on your window every 20 minutes, encouraging you to take a rejuvenating break.

### Blank Screen Mode:
Immerse yourself in a 20-second screen blackout, providing instant relief to your eyes.

### Beep Sound Mode:
Experience a precisely timed 20-second beep sequence, aligning perfectly with the renowned 20-20-20 rule.

### Intelligent Monitoring:

EyeRest is not just a timer; it's intelligent. Notifications are delivered only when your monitor is active, seamlessly respecting your workflow.

### Smart Detection:
Recognizes when you're in meetings (Teams, Zoom, Google Meet) or engaged in multimedia activities, ensuring only notifications, not beeps, to avoid disruptions.


# Dependencies:

    OS: Ubuntu 20.04 (>= 18.04)
    python 3.8.9
    pygame: sudo pip3 install plyer
    plyer: sudo pip install plyer
    cv2: sudo pip install opencv-python
    xvfb: apt-get install -y xvfb
    screeninfo: sudo pip install screeninfo

#### After Downloading EyeGuardian project
move eye_rest_project to HOME directory
    mv ./eye_rest_project ~/.
    cd ~/./eye_rest_project

#### After installing Dependencies
for dry run test
    python eye_rest.py beep_sound

#### To automate script when you turn on your system
    crontab -e

#### add following line
    @reboot sleep 30  && /usr/bin/python3 /path/of/eye_rest.py beep_sound >> /path/of/eye_rest_project/logfile.log 2>&1


