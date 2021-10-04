from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from alarm.alarm import play_alarm_file, countdown_and_play_alarm
from alarm.audio import create_alarm_audio_file
from tests.constants import BIRDS_ALARM_FILE, BIRDS_ALARM_FRAGMENT
from tests.helpers import get_text_from_audio_file


def test_play_alarm_file_no_timeout():
    start = datetime.now()
    play_alarm_file(BIRDS_ALARM_FRAGMENT)
    end = datetime.now()
    assert int((end - start).seconds) == 2


def test_play_alarm_file_with_timeout():
    start = datetime.now()
    play_alarm_file(BIRDS_ALARM_FILE, 1)
    end = datetime.now()
    assert int((end - start).seconds) == 1


@patch("alarm.alarm.play_alarm_file")
def test_countdown_and_play_alarm(play_mock, capfd):
    countdown_and_play_alarm(3, str(BIRDS_ALARM_FILE), display_timer=True)
    captured = capfd.readouterr()
    assert captured.out == "00:03\r00:02\r00:01\r00:00\r"


def test_voice_alarm_text():
    sentence = "take the trash out"
    file = create_alarm_audio_file(sentence)
    countdown_and_play_alarm(0, file, timeout=2)
    actual = get_text_from_audio_file(file)
    assert actual.startswith(sentence)
    Path(file).unlink()
