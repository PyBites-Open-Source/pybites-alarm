import os
from pathlib import Path

ALLOWED_EXTENSIONS = {".mp3", ".mp4", ".wav"}
TMP = Path(os.getenv("TMP", "/tmp"))
TMP_SONG = TMP / "alarm.mp3"
