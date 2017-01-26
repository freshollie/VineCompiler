# VineCompiler - Used for http://youtube.com/newvinecomps/

All sourcecode created 2014 by Oliver Bell

Depricated python script to download and compile popular vines into a single video.

This script will no longer work, but examples of how it did work can be seen on the youtube channel



# Explanation

## Main.py

Combines the downloader and compiler to make a video when a correct amount of vines are downloaded in the folder with todays date

## SeevineDownloader.py

Attempts to download videos from "seevine.com", a website now shutdown. It will thread these downloads and when it gets to a given number of videos it will stop.

## VineCompiler.py 

Combines the videos in the given root folder into a video with their titles.

# Libaries

- MoviePy | https://github.com/Zulko/moviepy
