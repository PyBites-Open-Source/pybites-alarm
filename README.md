# PyBites Alarm

Play a music file after an interval of N minutes.

## Setup

```
git clone git@github.com:pybites/pbalarm.git
cd pbalarm
poetry install
```

## Configure

Create an `.env` file and add `ALARM_MUSIC_FILE` to an absolute path of the music file that should play when the timer ends. For example:

```
$ cat .env
ALARM_MUSIC_FILE=/Users/bbelderbos/Music/alarm.mp4
```

## Demo

You can run it inside the checkout directory using: `poetry run alarm`.

To run it from anywhere add this to your `~/.zshrc` (or `~/.bashrc`):

```
function alarm() {
    cd $HOME/code/alarm
    poetry run python -m alarm.alarm $1
}
```

Now I can run it with a number of minutes:

```
$ alarm 2
02:00
```

When the timer ends it will play your configured audio file.

Or you can set the interval in interactive mode:

```
$ alarm
Enter minutes till alarm (hit enter for a standard pomodoro (25 min), 'q' for exit) 5
05:00
```

Enjoy!
