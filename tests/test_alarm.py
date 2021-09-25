from datetime import datetime
from unittest.mock import patch

from alarm.alarm import play_alarm_file, countdown_and_play_alarm
from tests.test_cli import BIRDS_ALARM_FILE


def test_play_alarm_file():
    start = datetime.now()
    play_alarm_file(BIRDS_ALARM_FILE, 1)
    end = datetime.now()
    assert int((end - start).seconds) == 1


@patch("alarm.alarm.play_alarm_file")
def test_countdown_and_play_alarm(play_mock, capfd):
    countdown_and_play_alarm(3, str(BIRDS_ALARM_FILE), display_timer=True)
    captured = capfd.readouterr()
    assert captured.out == "00:03\r00:02\r00:01\r00:00\r"
