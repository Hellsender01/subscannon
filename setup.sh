#!/bin/bash

clear

BLACK=`tput setaf 0`
RED=`tput setaf 1`
GREEN=`tput setaf 2`
YELLOW=`tput setaf 3`
BLUE=`tput setaf 4`
MAGENTA=`tput setaf 5`
CYAN=`tput setaf 6`
WHITE=`tput setaf 7`
BOLD=`tput bold`
RESET=`tput sgr0`

echo """${BOLD}${BLUE}
   _____ __  ______ _____ _________    _   ___   ______  _   __
  / ___// / / / __ ) ___// ____/   |  / | / / | / / __ \/ | / /
  \__ \/ / / / __  \__ \/ /   / /| | /  |/ /  |/ / / / /  |/ / 
 ___/ / /_/ / /_/ /__/ / /___/ ___ |/ /|  / /|  / /_/ / /|  /  
/____/\____/_____/____/\____/_/  |_/_/ |_/_/ |_/\____/_/ |_/   
                                                               
                                ${RED}       By - Harshit Joshi${RESET}
"""

sudo apt-get update && apt-get upgrade -y

sudo apt-get install python3

sudo apt-get install python 

sudo apt-get install python3-pip

sudo apt-get install python-pip

sudo apt-get install libgcc1:i386

sudo pip install dnspython 2>/dev/null

sudo pip3 install requests

sudo pip3 install argparse

sudo pip3 install bs4

sudo chmod +x subscannon.py

mkdir /usr/share/subscannon

cp default.txt /usr/share/subscannon/

sudo cp subscannon.py /usr/bin/subscannon

clear

subscannon --help
