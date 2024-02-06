Dependencies:

    OS: Ubuntu 20.04
    python 3.8.9
    pygame: sudo pip3 install plyer
    plyer: sudo pip install plyer
    cv2: sudo pip install opencv-python
    xvfb: apt-get install -y xvfb
    screeninfo: sudo pip install screeninfo

move eye_rest_project to HOME directory
    mv ./eye_rest_project ~/.
    cd ~/./eye_rest_project

After installing Dependencies
for dry run test
    python eye_rest.py beep_sound

To automate script when you turn on your system
    crontab -e

    add following line
    @reboot sleep 30  && /usr/bin/python3 /path/of/eye_rest.py beep_sound >> /home/sahil/eye_rest_project/logfile.log 2>&1
