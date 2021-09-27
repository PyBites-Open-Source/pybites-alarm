from pathlib import Path
import time
from typing import Optional

from pydub import AudioSegment
from pydub.playback import _play_with_simpleaudio


def countdown_and_play_alarm(
    seconds: int,
    alarm_file: str,
    display_timer: bool = False,
    timeout: Optional[int] = None,
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

    play_alarm_file(alarm_file, timeout)


def play_alarm_file(alarm_file: str, timeout: Optional[int] = None) -> None:
    """
    Looking at pydub/playback.py simpleaudio has the ability to stop the song
    """
    file_type = Path(alarm_file).suffix.lstrip(".")
    song = AudioSegment.from_file(alarm_file, file_type)
    # I know, should not use "internal" functions, but this was the only way
    # to stop the song after a number of seconds
    playback = _play_with_simpleaudio(song)
    if isinstance(timeout, int):
        time.sleep(timeout)
        playback.stop()
    else:
        playback.wait_done()
