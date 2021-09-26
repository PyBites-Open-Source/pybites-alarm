from io import StringIO

from audio_program_generator.apg import AudioProgramGenerator

from alarm.constants import TMP_SONG


def create_alarm_audio_file(
    text: str, file: str = str(TMP_SONG), pause: int = 2, loops: int = 3
) -> str:
    alarm_text = "\n".join(f"{text};{pause}" for _ in range(loops))
    kwargs = {"hide_progress_bar": True}
    apg = AudioProgramGenerator(StringIO(alarm_text), **kwargs)
    result = apg.invoke()
    with open(file, "wb") as f:
        f.write(result.getbuffer())
    result.close()
    return file
