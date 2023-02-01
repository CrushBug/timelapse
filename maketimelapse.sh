#!/bin/sh
# make an MP4 time lapse from JPEGs with ffMPEG
#
# $1 camera/folder name
# $2 date in yyyy-mm-dd format
#
# e.g. results in "backyard_2023-01-23.mp4" from the "backyard/2023-01-24" folder
ffmpeg -hide_banner -framerate 12 -pattern_type glob -i "$1/$2/*.jpeg" -c:v libx264 -r 24 "$1_$2.mp4"
