import os
import sys
from time import sleep
from unittest.mock import patch

import pytest

from alarm.cli import parse_args
from alarm.constants import TMP_SONG, ON_WINDOWS
from alarm.__main__ import main
from tests.constants import BIRDS_ALARM_FILE, FAKE_FILE
from tests.helpers import alarm_process_is_running

BACKGROUND_SKIP_REASON = "Background option not supported on Windows"


@pytest.mark.skipif(ON_WINDOWS, reason=BACKGROUND_SKIP_REASON)
@patch("os.system")
def test_main_background_with_specified_file(os_mock, capfd):
    parsed_args = parse_args(["-s", "3", "-b", "-f", str(BIRDS_ALARM_FILE)])
    main(parsed_args)
    os_mock.assert_called_with(
        f"{sys.executable} -m alarm -s 3 -f '{str(BIRDS_ALARM_FILE)}' &"
    )
    captured = capfd.readouterr()
    assert captured.out == "Playing alarm in 3 seconds\n"


@pytest.mark.skipif(ON_WINDOWS, reason=BACKGROUND_SKIP_REASON)
@patch("os.system")
def test_main_background_with_timeout(os_mock):
    parsed_args = parse_args(["-s", "3", "-b", "-f", str(BIRDS_ALARM_FILE), "-t", "2"])
    main(parsed_args)
    os_mock.assert_called_with(
        f"{sys.executable} -m alarm -s 3 -f '{str(BIRDS_ALARM_FILE)}' -t 2 &"
    )


@pytest.mark.skipif(ON_WINDOWS, reason=BACKGROUND_SKIP_REASON)
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
def test_main_foreground_with_timer(countdown_mock):
    parsed_args = parse_args(["-m", "1", "-d", "-f", str(BIRDS_ALARM_FILE)])
    main(parsed_args)
    countdown_mock.assert_called_with(
        60, str(BIRDS_ALARM_FILE), display_timer=True, timeout=None
    )


@patch("alarm.__main__.countdown_and_play_alarm")
def test_main_foreground_different_duration_and_file(countdown_mock):
    parsed_args = parse_args(["-m", "5", "-f", str(FAKE_FILE)])
    main(parsed_args)
    countdown_mock.assert_called_with(
        300, str(FAKE_FILE), display_timer=False, timeout=None
    )


@pytest.mark.skipif(ON_WINDOWS, reason=BACKGROUND_SKIP_REASON)
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


def test_voice_alarm_temp_file_cleanup():
    parsed_args = parse_args(["-s", "1", "-M", "code Python", "-t", "2"])
    main(parsed_args)
    assert not TMP_SONG.exists()


@patch("alarm.__main__.countdown_and_play_alarm")
def test_repeated_alarm_for_pomodoros(countdown_mock):
    parsed_args = parse_args(["-m", "25", "-M", "wrap up pomodoro", "-r", "4"])
    main(parsed_args)
    assert countdown_mock.call_count == 4
