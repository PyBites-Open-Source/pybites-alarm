# PyBites Alarm

Play a music file or voice message after an interval of N minutes or seconds.

## Install the tool

```
$ pip install pybites-alarm
$ alarm
usage: alarm [-h] (-s SECONDS | -m MINUTES) [-b | -d] [-l SONG_LIBRARY | -f FILE | -M MESSAGE] [-v] [-t TIMEOUT]
alarm: error: one of the arguments -s/--seconds -m/--minutes is required
```

**Note** that you'll need [`ffmpeg`](https://www.gyan.dev/ffmpeg/builds/) to play an alarm sound file. You'll also need [`libasound2-dev`](https://packages.debian.org/sid/libasound2-dev) on Linux. On Windows you will additionally need [Visual Studio tools](https://visualstudio.microsoft.com/downloads/). Currently it does not work great yet on WSL.

## Usage

You can specify an interval time using seconds (`-s`) or minutes (`-m`).

By default it runs in the foreground, but on Mac/Linux (not Windows) you can run it in the background using `-b`.

To display the seconds countdown use `-d`.

There are three ways to play an alarm file:

1. Specify one with `-f`.
2. Pick a random file from your music library directory. For that use `-l`.
3. Use a default file by setting `ALARM_MUSIC_FILE` in `.env`, for example:

	```
	$ cat .env
	ALARM_MUSIC_FILE=/Users/bbelderbos/Music/alarm.mp4
	```

It can be confusing when a music file plays so since `0.0.4` you can play a voice message instead using `-M` (`--message`).

For example:

```
alarm -M "stand up for a walk" -m 20 -b
```

A voice repeats "stand up for a walk" three times after 20 minutes. Pretty useful for programmers :)

**Note** that we have a PR open with `apg` to hide the `tqdm` progress bar that shows with the `-M` option.

For long alarm files you can set a timeout to stop the alarm after N seconds using the `t` (`--timeout`) switch.

---

Here are all the supported options again:

```
$ alarm -h
usage: alarm [-h] (-s SECONDS | -m MINUTES) [-b | -d] [-l SONG_LIBRARY | -f FILE | -M MESSAGE] [-v] [-t TIMEOUT]

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
  -M MESSAGE, --message MESSAGE
                        Set an audio message to play for alarm (default: None)
  -v, --version         show program's version number and exit
  -t TIMEOUT, --timeout TIMEOUT
```

Again the `-b` option is not available on Windows, although it seems you can get that working with:

```
start /b alarm -s 3 -f test.mp3
```

This backgrounds a process on windows and CTRL + BREAK/SCRLLCK kills it. Or use the `-t` option, e.g. `start /b alarm -s 3 -f test.mp3 -t 20` (thanks Lee!)
