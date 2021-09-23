# PyBites Alarm

Play a music file after an interval of N minutes. You can configure the tune to play ...

## Setup

```
git clone git@github.com:PyBites-Open-Source/pybites-alarm.git
cd pybites-alarm
make install
make test
```

## Configure

Create an `.env` file and add `ALARM_MUSIC_FILE` to an absolute path of the music file that should play when the timer ends. For example:

```
$ cat .env
ALARM_MUSIC_FILE=/Users/bbelderbos/Music/alarm.mp4
```

You can also set `ALARM_DURATION_IN_SECONDS=<number_of_seconds_int>` to stop the alarm after N seconds.

## Usage

```
$ python -m alarm.alarm -h
usage: alarm.py [-h] (-s SECONDS | -m MINUTES) [-b | -d] [-l SONG_LIBRARY | -f FILE | -v]

Play an alarm after N minutes

optional arguments:
  -h, --help            show this help message and exit
  -s SECONDS, --seconds SECONDS
                        Number of seconds before playing alarm (default: None)
  -m MINUTES, --minutes MINUTES
                        Number of minutes before playing alarm (default: None)
  -b, --background      Run timer in the background (default: False)
  -d, --display_timer   Show timer in console (default: False)
  -l SONG_LIBRARY, --song_library SONG_LIBRARY
                        Take a random song from a song library directory, supported formats: .mp3, .mp4, .wav (default: None)
  -f FILE, --file FILE  File path to song to play as alarm (default: None)
  -v, --version         show program's version number and exit
```
