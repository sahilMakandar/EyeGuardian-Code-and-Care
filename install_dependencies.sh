#!/bin/bash

# Check if the OS is Ubuntu 18.04 or higher
ubuntu_version=$(lsb_release -rs)
if (( $(echo "$ubuntu_version >= 18.04" | bc -l) )); then
    echo "Ubuntu version $ubuntu_version is supported."
else
    echo "This script requires Ubuntu 18.04 or higher."
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
sudo apt-get update
sudo apt-get install -y python3-pip xvfb
sudo pip3 install pygame plyer opencv-python screeninfo

# Move eye_rest_project to HOME directory
echo "Moving eye_rest_project to HOME directory..."
mv ./eye_rest_project ~/

# Change directory to eye_rest_project
cd ~/eye_rest_project

echo "Setup completed successfully!"