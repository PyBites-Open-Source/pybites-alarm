import os
import sys
from unittest.mock import patch

from alarm.cli import parse_args
from alarm.__main__ import main
from tests.constants import BIRDS_ALARM_FILE, FAKE_FILE


@patch("os.system")
def test_main_background_with_specified_file(os_mock, capfd):
    args = parse_args(["-s", "3", "-b", "-f", str(BIRDS_ALARM_FILE)])
    main(args)
    os_mock.assert_called_with(
        f"{sys.executable} -m alarm.pytest -s 3 -f '{str(BIRDS_ALARM_FILE)}' &"
    )
    captured = capfd.readouterr()
    assert captured.out == "Playing alarm in 3 seconds\n"


@patch("os.system")
@patch.dict(os.environ, {"ALARM_MUSIC_FILE": str(BIRDS_ALARM_FILE)})
def test_main_background_with_file_from_env(os_mock, capfd):
    args = parse_args(["-m", "1", "-b"])
    main(args)
    os_mock.assert_called_with(
        f"{sys.executable} -m alarm.pytest -s 60 -f '{str(BIRDS_ALARM_FILE)}' &"
    )
    captured = capfd.readouterr()
    assert captured.out == "Playing alarm in 1 minute\n"


@patch("alarm.__main__.countdown_and_play_alarm")
@patch.dict(os.environ, {"ALARM_MUSIC_FILE": str(BIRDS_ALARM_FILE)})
def test_main_foreground(countdown_mock, capfd):
    args = parse_args(["-m", "1", "-d"])
    main(args)
    countdown_mock.assert_called_with(60, str(BIRDS_ALARM_FILE), display_timer=True)


@patch("alarm.__main__.countdown_and_play_alarm")
@patch.dict(os.environ, {"ALARM_MUSIC_FILE": str(BIRDS_ALARM_FILE)})
def test_main_foreground_other_options(countdown_mock, capfd):
    args = parse_args(["-m", "5", "-f", str(FAKE_FILE)])
    main(args)
    countdown_mock.assert_called_with(300, str(FAKE_FILE), display_timer=False)
