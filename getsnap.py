#/usr/bin/python3
#getsnap.py
# by Derek French
# grab a single frame from a UniFi camera to later assemble a timelapse video
# It is expected that this is called from a cron job so no interactive error messaging is currently provided
#TODO add command line parsing, and add:
#-verbose - print error messages
#-config  - specify the getsnap.ini config file location 
# v0.11
# - (0.11) switching to def main(), if...is

#imports
import configparser
from datetime import datetime
import os
import requests
import sys

#constants
VERSION = '0.11'
CONFIG_FILENAME = 'getsnap.ini'
SECTION_CAMERA = 'Camera'
SECTION_GENERAL = 'general'
ENTRY_CAMERANAME = 'CameraName'
ENTRY_FOLDERNAME = 'FolderName'
ENTRY_JPEGSNAPPATH = 'jpegSnapPath'
ENTRY_PATH = 'Path'

#mainline
def main():
  #get the folder from where the script is being run; that is where the INI file needs to be
  scriptDir = os.path.dirname(sys.argv[0])
  configFile = os.path.join(scriptDir, CONFIG_FILENAME)
  #check for the config file to exist
  if os.path.exists(configFile) is False:
    #quit the program
    #if args.verbose: print('configfile "' + configFile + '" not found.')
    quit(1)
  #read config file
  config = configparser.ConfigParser()
  config.read(configFile)
  #TODO allow for section missing
  snapPath = config[SECTION_GENERAL][ENTRY_PATH]
  #get the date and time and use it for all cameras, regardless of any processing delays
  now = datetime.now()
  snapDate = now.strftime("%Y-%m-%d")    #'2022-11-30'
  snapTime = now.strftime("%H-%M-%S")    #'15-25-24'
  timestamp = snapDate + '_' + snapTime  #'2022-11-30_15-25-24'
  #loop through the cameras listed in the config file
  cameraNumber = 1
  sectionName = SECTION_CAMERA + str(cameraNumber)
  while sectionName in config:
    #cameraName = config[sectionName][ENTRY_CAMERANAME]
    folderName = config[sectionName][ENTRY_FOLDERNAME]
    jpegSnapPath = config[sectionName][ENTRY_JPEGSNAPPATH]
    savePath = os.path.join(snapPath, folderName)         #'.../backyard/'
    #if the camera folder name doesn't exist, create it
    if os.path.exists(savePath) is False:
      os.mkdir(savePath)
    #store all snaps in date subfolders
    savePath = os.path.join(savePath, snapDate)           #'.../backyard/2022-11-30/'
    #if the date subfolder doesn't exist, create it
    if os.path.exists(savePath) is False:
      os.mkdir(savePath)
    saveName = savePath + '/' + timestamp + '_snap.jpeg'  #'.../backyard/2022-11-30/2022-11-30_15-25-24_snap.jpeg'
    imgData = requests.get(jpegSnapPath).content
    with open(saveName, 'wb') as handler:
      handler.write(imgData)
    #try to read the next entry in the config
    cameraNumber = cameraNumber + 1
    sectionName = SECTION_CAMERA + str(cameraNumber)
  #end while sectionName
#end main()

if __name__ == "__main__":
  main()