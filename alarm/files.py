import os
import random
from pathlib import Path

from alarm.constants import ALLOWED_EXTENSIONS
from alarm.exceptions import AlarmFileException


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
