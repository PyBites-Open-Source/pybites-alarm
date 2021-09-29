import os
from pathlib import Path
import platform

ALLOWED_EXTENSIONS = {".mp3", ".mp4", ".wav"}
TMP = Path(os.getenv("TMP", "/tmp"))
TMP_SONG = TMP / "alarm.mp3"
ON_WINDOWS = platform.system() == "Windows"
