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
    parsed_args = parse_args(["-s", "3", "-b", "-f", str(BIRDS_ALARM_FILE)])
    main(parsed_args)
    os_mock.assert_called_with(
        f"{sys.executable} -m alarm -s 3 -f '{str(BIRDS_ALARM_FILE)}' &"
    )
    captured = capfd.readouterr()
    assert captured.out == "Playing alarm in 3 seconds\n"


@patch("os.system")
def test_main_background_with_timeout(os_mock, capfd):
    parsed_args = parse_args(["-s", "3", "-b", "-f", str(BIRDS_ALARM_FILE), "-t", "2"])
    main(parsed_args)
    os_mock.assert_called_with(
        f"{sys.executable} -m alarm -s 3 -f '{str(BIRDS_ALARM_FILE)}' -t 2 &"
    )


@patch("os.system")
@patch.dict(os.environ, {"ALARM_MUSIC_FILE": str(BIRDS_ALARM_FILE)})
def test_main_background_with_file_from_env(os_mock, capfd):
    parsed_args = parse_args(["-m", "1", "-b"])
    main(parsed_args)
    os_mock.assert_called_with(
        f"{sys.executable} -m alarm -s 60 -f '{str(BIRDS_ALARM_FILE)}' &"
    )
    captured = capfd.readouterr()
    assert captured.out == "Playing alarm in 1 minute\n"


@patch("alarm.__main__.countdown_and_play_alarm")
def test_main_foreground_with_timer(countdown_mock, capfd):
    parsed_args = parse_args(["-m", "1", "-d", "-f", str(BIRDS_ALARM_FILE)])
    main(parsed_args)
    countdown_mock.assert_called_with(
        60, str(BIRDS_ALARM_FILE), display_timer=True, timeout=None
    )


@patch("alarm.__main__.countdown_and_play_alarm")
def test_main_foreground_different_duration_and_file(countdown_mock, capfd):
    parsed_args = parse_args(["-m", "5", "-f", str(FAKE_FILE)])
    main(parsed_args)
    countdown_mock.assert_called_with(
        300, str(FAKE_FILE), display_timer=False, timeout=None
    )


def test_background_process_starts_and_terminates():
    """
    This test checks if the alarm process is running in the background and
    stops running when done.
    """
    assert alarm_process_is_running() is False
    parsed_args = parse_args(["-s", "2", "-b", "-f", str(FAKE_FILE), "-t", "1"])
    main(parsed_args)
    assert alarm_process_is_running() is True
    sleep(3)
    assert alarm_process_is_running() is False
