import argparse
import os
from pathlib import Path
import multiprocessing
import random
import sys
import time

from dotenv import load_dotenv
from playsound import playsound

from . import __version__

load_dotenv()

ALARM_DURATION_IN_SECONDS = int(os.environ.get("ALARM_DURATION_IN_SECONDS", 20))
ALLOWED_EXTENSIONS = {".mp3", ".mp4", ".wav"}


class AlarmFileException(Exception):
    """To be used in case of an invalid alarm file"""


def countdown_and_play_alarm(
    seconds: int, alarm_file: str, display_timer: bool = False
) -> None:
    """Countdown N seconds then play an alarm file"""
    while seconds:
        mins, secs = divmod(seconds, 60)
        if display_timer:
            print(f"{mins:02}:{secs:02}", end="\r")
        time.sleep(1)
        seconds -= 1

    if display_timer:
        print("00:00", end="\r")

    play_alarm_file(alarm_file)


def play_alarm_file(alarm_file: str, timeout: int = ALARM_DURATION_IN_SECONDS) -> None:
    """Play alarm file for a number of seconds, got the idea for timeout
    from here: https://stackoverflow.com/a/52995334
    """
    proc = multiprocessing.Process(target=playsound, args=(alarm_file,))
    proc.start()
    proc.join(timeout=timeout)
    proc.terminate()


def parse_args(args):
    """Passing in args makes this easier to test:
    https://stackoverflow.com/a/18161115
    """
    parser = argparse.ArgumentParser(
        description="Play an alarm after N minutes",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    duration_group = parser.add_mutually_exclusive_group(required=True)
    duration_group.add_argument(
        "-s", "--seconds", type=int, help="Number of seconds before playing alarm"
    )
    duration_group.add_argument(
        "-m", "--minutes", type=int, help="Number of minutes before playing alarm"
    )

    run_mode_group = parser.add_mutually_exclusive_group()
    run_mode_group.add_argument(
        "-b",
        "--background",
        action="store_true",
        default=False,
        help="Run timer in the background",
    )
    run_mode_group.add_argument(
        "-d",
        "--display_timer",
        action="store_true",
        default=False,
        help="Show timer in console",
    )

    alarm_file_group = parser.add_mutually_exclusive_group()
    alarm_file_group.add_argument(
        "-l",
        "--song_library",
        help=(
            "Take a random song from a song library directory, "
            f"supported formats: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        ),
    )
    alarm_file_group.add_argument(
        "-f", "--file", help="File path to song to play as alarm"
    )
    alarm_file_group.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    return parser.parse_args(args)


def _get_file(args) -> str:
    """Get alarm song file from library, passed in file or environment"""
    if args.song_library:
        # regex of allowed extensions in rglob did not work
        files = Path(args.song_library).rglob("*")
        music_files = [f for f in files if f.suffix in ALLOWED_EXTENSIONS]
        if music_files:
            return str(random.choice(music_files))
        else:
            return ""
    elif args.file:
        return args.file
    else:
        return os.environ["ALARM_MUSIC_FILE"]


def _validate_file(file: str) -> None:
    """Make sure we get a music file that exists"""
    if not Path(file).exists():
        raise AlarmFileException(f"{file} does not exist")
    if not Path(file).suffix in ALLOWED_EXTENSIONS:
        raise AlarmFileException(
            f"{file} is not supported. {', '.join(sorted(ALLOWED_EXTENSIONS))} are."
        )


def get_alarm_file(args) -> str:
    file = _get_file(args)
    _validate_file(file)
    return file


def main(args=None):
    args = args if args else parse_args(sys.argv[1:])

    if args.seconds:
        seconds = int(args.seconds)
        minutes = seconds / 60
    else:
        minutes = int(args.minutes)
        seconds = minutes * 60

    alarm_file = get_alarm_file(args)

    if args.background:
        if minutes < 1:
            time_till_alarm = f"{seconds} seconds"
        else:
            time_till_alarm = f"{minutes} minute{'' if minutes == 1 else 's'}"

        print(f"Playing alarm in {time_till_alarm}")

        package = __package__
        module = Path(sys.argv[0]).stem

        os.system(f"python -m {package}.{module} -s {seconds} -f '{alarm_file}' &")
    else:
        try:
            countdown_and_play_alarm(
                seconds, alarm_file, display_timer=args.display_timer
            )
        except KeyboardInterrupt:  # pragma: no cover
            pass


if __name__ == "__main__":  # pragma: no cover
    main()
