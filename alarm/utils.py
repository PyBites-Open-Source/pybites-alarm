from functools import partial

import psutil


def process_is_running(cmd: str, args: str) -> bool:
    for process in psutil.process_iter():
        if cmd.lower() in process.name().lower():
            cmd_line = " ".join(process.cmdline())
            if args.lower() in cmd_line:
                return True
    return False


alarm_process_is_running = partial(process_is_running, "python", "-m alarm")
