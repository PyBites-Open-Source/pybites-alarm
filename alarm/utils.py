from io import StringIO
from functools import partial
from pathlib import Path

from audio_program_generator.apg import AudioProgramGenerator
import psutil
from pydub import AudioSegment
import speech_recognition as sr


from alarm.constants import TMP, TMP_SONG


def process_is_running(cmd: str, args: str) -> bool:
    for process in psutil.process_iter():
        if cmd.lower() in process.name().lower():
            cmd_line = " ".join(process.cmdline())
            if args.lower() in cmd_line:
                return True
    return False


alarm_process_is_running = partial(process_is_running, "python", "-m alarm")


def create_alarm_audio_file(
    text: str, file: Path = TMP_SONG, pause: int = 2, loops: int = 3
) -> Path:
    alarm_text = "\n".join(f"{text};{pause}" for _ in range(loops))
    kwargs = {"hide_progress_bar": True}
    apg = AudioProgramGenerator(StringIO(alarm_text), **kwargs)
    result = apg.invoke()
    with open(file, "wb") as f:
        f.write(result.getbuffer())
    result.close()
    return file


def get_text_from_audio_file(file: Path) -> str:
    sound = AudioSegment.from_mp3(str(file))
    transcript_wav = TMP / "transcript.wav"
    sound.export(str(transcript_wav), format="wav")

    recognizer = sr.Recognizer()
    with sr.AudioFile(str(transcript_wav)) as source:
        audio = recognizer.record(source)
        ret = recognizer.recognize_google(audio, show_all=True)

    transcript_wav.unlink()
    return ret["alternative"][0]["transcript"]
