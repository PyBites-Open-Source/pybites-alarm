from datetime import datetime
import os
from pathlib import Path
import sys
from unittest.mock import patch

import pytest

from alarm.alarm import (
    AlarmFileException,
    play_alarm_file,
    _validate_file,
    _get_file,
    parse_args,
    get_alarm_file,
    countdown_and_play_alarm,
    main,
)

BIRDS_ALARM_FILE = Path("tests") / "payloads" / "birds.wav"
FAKE_FILE = Path("tests") / "payloads" / "file.mp4"
NOT_SUPPORTED_ERROR = "is not supported.*.mp3, .mp4, .wav are."


@patch("alarm.alarm.play_alarm_file")
def test_countdown_and_play_alarm(play_mock, capfd):
    countdown_and_play_alarm(3, str(BIRDS_ALARM_FILE), display_timer=True)
    captured = capfd.readouterr()
    assert captured.out == "00:03\r00:02\r00:01\r00:00\r"


def test_play_alarm_file():
    start = datetime.now()
    play_alarm_file(BIRDS_ALARM_FILE, 1)
    end = datetime.now()
    assert int((end - start).seconds) == 1


def test_get_file_for_empty_library(tmpdir):
    args = parse_args(["-s", "3", "-l", str(tmpdir)])
    with pytest.raises(AlarmFileException, match=NOT_SUPPORTED_ERROR):
        file = _get_file(args)
        _validate_file(file)


def test_get_file_for_filled_mp3_library(tmpdir):
    music_dir = tmpdir
    songs = {music_dir / f"{song}.mp3" for song in "live love train enjoy".split()}
    for song in songs:
        open(song, "a").close()
    args = parse_args(["-s", "3", "-l", str(music_dir)])
    assert _get_file(args) in songs


def test_get_file_for_one_wav_file(tmpdir):
    wav_file = "my_song.wav"
    open(tmpdir / wav_file, "a").close()
    args = parse_args(["-s", "3", "-l", str(tmpdir)])
    assert Path(_get_file(args)).name == wav_file


def test_get_file_for_one_txt_file(tmpdir):
    txt_file = "notes.txt"
    open(tmpdir / txt_file, "a").close()
    args = parse_args(["-s", "3", "-l", str(tmpdir)])
    assert _get_file(args) == ""


def test_get_file_for_file(tmpdir):
    music_file = str(tmpdir / "file.mp3")
    args = parse_args(["-s", "3", "-f", music_file])
    assert _get_file(args) == music_file


def test_get_file_from_env(tmpdir):
    args = parse_args(["-s", "3"])
    with patch.dict(os.environ, {"ALARM_MUSIC_FILE": str(BIRDS_ALARM_FILE)}):
        assert get_alarm_file(args) == str(BIRDS_ALARM_FILE)


def test_validate_file():
    with pytest.raises(AlarmFileException, match="does not exist"):
        file = Path("tests") / "birds2.wav"
        _validate_file(file)
    with pytest.raises(AlarmFileException, match=NOT_SUPPORTED_ERROR):
        file = Path("tests") / "test_alarm.py"
        _validate_file(file)


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


@patch("alarm.alarm.countdown_and_play_alarm")
@patch.dict(os.environ, {"ALARM_MUSIC_FILE": str(BIRDS_ALARM_FILE)})
def test_main_foreground(countdown_mock, capfd):
    args = parse_args(["-m", "1", "-d"])
    main(args)
    countdown_mock.assert_called_with(60, str(BIRDS_ALARM_FILE), display_timer=True)


@patch("alarm.alarm.countdown_and_play_alarm")
@patch.dict(os.environ, {"ALARM_MUSIC_FILE": str(BIRDS_ALARM_FILE)})
def test_main_foreground_other_options(countdown_mock, capfd):
    args = parse_args(["-m", "5", "-f", str(FAKE_FILE)])
    main(args)
    countdown_mock.assert_called_with(300, str(FAKE_FILE), display_timer=False)
