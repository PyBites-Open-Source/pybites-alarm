from io import StringIO
from functools import partial
import os
from pathlib import Path

import psutil
from audio_program_generator.apg import AudioProgramGenerator

TMP = Path(os.getenv("TMP", "/tmp"))
TMP_SONG = TMP / "alarm.mp3"


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
):
    alarm_text = "\n".join(f"{text};{pause}" for _ in range(loops))
    kwargs = {"hide_progress_bar": True}
    apg = AudioProgramGenerator(StringIO(alarm_text), **kwargs)
    result = apg.invoke()
    with open(file, "wb") as f:
        f.write(result.getbuffer())
    result.close()
    return file
