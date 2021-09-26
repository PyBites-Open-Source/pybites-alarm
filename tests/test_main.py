import os
import sys
from time import sleep
from unittest.mock import patch

from alarm.cli import parse_args
from alarm.__main__ import main
from alarm.utils import alarm_process_is_running
from tests.constants import BIRDS_ALARM_FILE, FAKE_FILE


@patch("os.system")
def test_main_background_with_specified_file(os_mock, capfd):
    args = parse_args(["-s", "3", "-b", "-f", str(BIRDS_ALARM_FILE)])
    main(args)
    os_mock.assert_called_with(
        f"{sys.executable} -m alarm -s 3 -f '{str(BIRDS_ALARM_FILE)}' &"
    )
    captured = capfd.readouterr()
    assert captured.out == "Playing alarm in 3 seconds\n"


@patch("os.system")
@patch.dict(os.environ, {"ALARM_MUSIC_FILE": str(BIRDS_ALARM_FILE)})
def test_main_background_with_file_from_env(os_mock, capfd):
    args = parse_args(["-m", "1", "-b"])
    main(args)
    os_mock.assert_called_with(
        f"{sys.executable} -m alarm -s 60 -f '{str(BIRDS_ALARM_FILE)}' &"
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


@patch.dict(os.environ, {"ALARM_DURATION_IN_SECONDS": "1"})
def test_background_process_starts_and_terminates():
    """
    This test checks if the alarm process is running in the background and
    stops running when done.
    """
    assert alarm_process_is_running() is False
    args = parse_args(["-s", "2", "-b", "-f", str(FAKE_FILE)])
    main(args)
    assert alarm_process_is_running() is True
    sleep(3)
    assert alarm_process_is_running() is False
