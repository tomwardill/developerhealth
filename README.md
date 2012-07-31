developerhealth
===============

This was created for [leedshack 2012](http://leedshack.com/). The code is rough, and it requires arcane bits and pieces that just happened to work on the day. Patches gleefully accepted.

The Idea
--------

The idea for this was that some code can make you angry. Find out how angry by graphing your heart rate against your git commit times, and know how much the average increased.
It also gained a bit of [lolcommits](https://github.com/mroth/lolcommits/), as it will take your picture as you commit, and use OSX Location Services to find out where you were when you commited.

The Pieces
----------

### HRM
This is a small daemon that uses [python-ant](https://github.com/mvillalba/python-ant) to talk to an ANT+ Heart Rate Monitor (such as the Garmin HRM chest straps) via a USB ANT+ Device (such as the Garmin ANT+ stick, or the Suunto Movestick Mini, which I used). It constantly runs, and pushes a value every 10 seconds into a mongodb database. Currently only working on a linux host.

### GIT
This is a post-commit hook that posts the available data to the web section. The address to post to is at the bottom of the file. It also requires [get-location](https://github.com/lindes/get-location) to be available on your path. It will only run on OSX. Patches to make it work on Linux gratefully accepted.

### WEB
This is the main website. It uses Flask as the server, and mongodb, jquery and flot for the data storage and viewing.

### SD
A bonus [server density](http://www.serverdensity.com) plugin that will take the values that the HRM daemon has put into mongodb and post the values to server density. Requires the SD agent installed and configured for plugins.

Installation
------------

The installation requirements for this were very changeable during the course of the 24 hour hack, so it's entirely possible that there's bits missing, or wrong. I'll try and confirm and tidy it up when I get chance

### Dependencies

This is the dependencies that will not be installed using pip.

1. MongoDB
2. Python 2.7
3. [get-location](https://github.com/lindes/get-location)
4. [python-ant](https://github.com/mvillalba/python-ant)

### Client Installation

On your OSX Client:

1. Compile and put get-location somewhere on your path.
2. Put the git/post-commit file into .git/hooks
3. Edit the post-commit file url to point to your host

### Host Installation

On your linux host

1. Checkout, and install python-ant
2. pip install -r requirements.txt
3. Install and ensure mongodb is running
4. run `python web.py` from the web folder
5. Visit http://localhost:5000