import os
from pathlib import Path
from unittest.mock import patch

import pytest

from alarm.cli import _get_file, _validate_file, get_alarm_file, parse_args
from alarm.exceptions import AlarmFileException

BIRDS_ALARM_FILE = Path("tests") / "payloads" / "birds.wav"
NOT_SUPPORTED_ERROR = "is not supported.*.mp3, .mp4, .wav are."


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
