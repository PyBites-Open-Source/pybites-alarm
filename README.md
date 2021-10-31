# PyBites Alarm

Play a music file or voice message after an interval of N minutes or seconds.

----
## Table of Contents
- [PyBites Alarm](#pybites-alarm)
  * [Install the tool](#install-the-tool)
  * [Usage](#usage)
    + [Voice messages](#voice-messages)
    + [Duration of the alarm](#duration-of-the-alarm)
    + [Repeating an alarm](#repeating-an-alarm)
  * [Installing ffmpeg on Windows](#installing-ffmpeg-on-windows)
----

## Install the tool

```
$ pip install pybites-alarm
$ alarm
usage: alarm [-h] (-s SECONDS | -m MINUTES) [-b | -d] [-l SONG_LIBRARY | -f FILE | -M MESSAGE] [-v] [-t TIMEOUT]
alarm: error: one of the arguments -s/--seconds -m/--minutes is required
```

**Note** that you'll need [`ffmpeg`](https://www.gyan.dev/ffmpeg/builds/) to play an alarm sound file. You'll also need [`libasound2-dev`](https://packages.debian.org/sid/libasound2-dev) on Linux. On Windows you will additionally need [Visual Studio tools](https://visualstudio.microsoft.com/downloads/). Currently it does not work great yet on WSL. See section ***Installing ffmpeg on Windows* for more details**.

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

### Voice messages

It can be confusing when a music file plays so since `0.0.4` you can play a voice message instead using `-M` (`--message`).

For example:

```
alarm -M "stand up for a walk" -m 20 -b
```

A voice repeats "stand up for a walk" three times after 20 minutes. Pretty useful for programmers :)

### Duration of the alarm

For long alarm files you can set a timeout to stop the alarm after N seconds using the `t` (`--timeout`) switch.

### Repeating an alarm

Since version `0.0.6` you can repeat an alarm using the `-r` switch. For example, to track 25 minute _pomodoro_ time blocks (as per the [Pomodoro Technique](https://en.wikipedia.org/wiki/Pomodoro_Technique)), you can run this command:

```
alarm -m 25 -M "pomodoro completed" -r 4
```

A voice will notify you every 25 minutes (for 4 times) that you have completed a _pomodoro_.

Another use case is to have it alert you to stand up and drink more water during the day - direct health benefits :)

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
                        Stop alarm after N seconds (default: None)
  -r REPEAT, --repeat REPEAT
                        Repeat alarm cycle N times (only works in foreground) (default: 1)
```

Again the `-b` option is not available on Windows, although it seems you can get that working with:

```
start /b alarm -s 3 -f test.mp3
```

This backgrounds a process on windows and CTRL + BREAK/SCRLLCK kills it. Or use the `-t` option, e.g. `start /b alarm -s 3 -f test.mp3 -t 20` (thanks [Lee](https://github.com/l1dge)!)

## Installing ffmpeg on Windows

Installing [`ffmpeg`](https://www.gyan.dev/ffmpeg/builds/) on Windows isn't as intuitive as we'd like so we thought we'd include a quick install guide for this too. The following is performed on Windows 10 and has not been tested on any other Windows releases.

1. Head to the [`ffmpeg` builds page](https://www.gyan.dev/ffmpeg/builds/).
2. Scroll down to *release builds* and select the latest `ffmpeg-release-full.7z` available file for download. This downloads the latest ffmpeg binaries.
3. Extract the files to a folder where you'd like ffmpeg to exist in your file system. Feel free to leave it in your Downloads folder, it doesn't really matter.

> **Note:** `pybites-alarm` utilises ffmpeg assuming it's in your path so you'll need to add the file path of the ffmpeg `bin` folder to your Windows `PATH` environment variable.

4. Open yout Start menu and type in *env*. The first search result returned should be "Edit the system environment variables". This setting lives in your Advanced System Properties. In the window that opens, click *Environment Variables*.
5. In the window that opens you'll see two separate variable sections: *User variables for username* and *System variables*. The former set of variables are unique to your Windows user profile, the latter variables are system wide so will affect all users on your PC. We suggest focusing on the section just for your unique user.
6. Click the *Path* variable and click *Edit*.
7. In the next window that opens, click *New*. This creates a text entry box under the last variable in the list.
8. Enter the full path to the ffmpeg `bin` folder. E.g.: `C:\Users\pybites\Downloads\ffmpeg-4.4.1-full_build\ffmpeg-4.4.1-full_build\bin`. Click OK.
9. Click OK on the Environment Variables window and then on the System Properties window too.
10. If you had any programs using the windows shell open, refresh or close and reopen them to pick up the environment variable changes.
11. You should now be able to run `alarm` as described earlier in this README.

----
<small><i><a href='http://ecotrust-canada.github.io/markdown-toc/'>Table of contents generated with markdown-toc</a></i></small>
