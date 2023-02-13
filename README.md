# Timelapse
Timelapse is a Python script to pull still frames from a UniFi security camera. The shell script takes these frames and assemble them into a timelapse MP4 video via ffmpeg.

While this can be run on Windows, it was designed to run on Linux for cron and for the glob support in ffmpeg.

Your UniFi camera must support still frame capture via an HTTP camera URL.

## getsnap.py
getsnap.py reads from getsnap.ini to determine the image storage path and the list of cameras to read from. getsnap.ini must be in the same folder as getsnap..py It loops through the Camera* sections from 1 to N, to support multiple cameras. The FolderName entry is appended to the Path entry to create the output path.
```
[general]
Path = /home/local/timelapse/

[Camera1]
CameraName = Backyard
FolderName = backyard
jpegSnapPath = http://192.168.50.50/snap.jpeg
```
getsnap.py requires the following libraries in Python.
```
configparser
datetime
os
requests
sys
```
The files will come out in the following format, 2023-02-13_04-29-01_snap.jpeg, as YYYY-MM-DD_HH-MM-SS_snap.jpeg. The seconds entry, SS, usually varies between 00 and 02 seconds, depending on cron calling timing.

## maketimelapse.sh
This is a simple shell script that calls ffmpeg to build an mp4 video from a directory of jpeg files. This script expects there to be a camera folder below it, and the jpeg files to be in an chronological alphabetical order. This script is usually called in the following manner. The video file will end up in the same folder as the script.

./maketimelapse.sh backyard 2023-01-30
```
ffmpeg -hide_banner -framerate 12 -pattern_type glob -i "$1/$2/*.jpeg" -c:v libx264 -r 24 "$1_$2.mp4"
```
More details about the ffmpeg command line can be found on the ffmpeg web site - https://ffmpeg.org/

## cron example
Here is a sample cron entry for calling the getsnap.py script every minute.
```
* * * * * /usr/bin/python3 /home/local/python/getsnap.py
```
For more cron help, please visit Crontab Guru - https://crontab.guru/
