import os

from dotenv import load_dotenv

load_dotenv()

ALARM_DURATION_IN_SECONDS = int(os.environ.get("ALARM_DURATION_IN_SECONDS", 20))
ALLOWED_EXTENSIONS = {".mp3", ".mp4", ".wav"}
