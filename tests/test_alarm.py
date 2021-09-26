from datetime import datetime
import os
from unittest.mock import patch

from pydub import AudioSegment
import speech_recognition as sr

from alarm.alarm import play_alarm_file, countdown_and_play_alarm
from alarm.utils import create_alarm_audio_file
from tests.constants import BIRDS_ALARM_FILE, BIRDS_ALARM_FRAGMENT


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
    file = create_alarm_audio_file("take the trash out")
    countdown_and_play_alarm(0, file, timeout=2)
    recognizer = sr.Recognizer()

    sound = AudioSegment.from_mp3(str(file))
    transcript_wav = "transcript.wav"
    sound.export(transcript_wav, format="wav")

    with sr.AudioFile(transcript_wav) as source:
        audio = recognizer.record(source)
        ret = recognizer.recognize_google(audio, show_all=True)

    actual = ret["alternative"][0]["transcript"]
    expected = "take the trash out take the trash out take the trash out"
    assert actual == expected

    file.unlink()
    os.remove(transcript_wav)
