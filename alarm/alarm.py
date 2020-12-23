from pathlib import Path
import sys
import time

from decouple import config
from playsound import playsound  # requires PyObjC (Mac)

ALARM_MUSIC_FILE = config('ALARM_MUSIC_FILE')
SECONDS_IN_MIN = 60
POMODORO_TIMING = 25 * SECONDS_IN_MIN

if not Path(ALARM_MUSIC_FILE).exists():
    sys.exit(f"Cannot locate music file: [{ALARM_MUSIC_FILE}]")


def countdown(seconds: int) -> None:
    while seconds:
        mins, secs = divmod(seconds, SECONDS_IN_MIN)
        print(f'{mins:02}:{secs:02}', end="\r")
        time.sleep(1)
        seconds -= 1

    print("00:00", end="\r")
    playsound(ALARM_MUSIC_FILE)


def main():
    while True:
        minutes = input(
            ("Enter minutes till alarm (hit enter for a "
             "standard pomodoro (25 min), 'q' for exit) "))
        seconds = POMODORO_TIMING

        if minutes.lower() == 'q':
            print('Bye')
            break

        elif minutes:
            try:
                minutes = int(minutes)
            except ValueError:
                print('Minutes needs to be an integer')
                continue
            else:
                seconds = minutes * 60

        try:
            countdown(seconds)
        except KeyboardInterrupt:
            print('Interruption, starting over ...')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        minutes = int(sys.argv[1])
        countdown(minutes * 60)
    else:
        main()
