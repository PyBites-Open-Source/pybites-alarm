import os
import sys

from alarm.alarm import countdown_and_play_alarm
from alarm.cli import parse_args
from alarm.files import get_alarm_file


def main(args=None):
    args = args if args else parse_args(sys.argv[1:])

    if args.seconds:
        seconds = int(args.seconds)
        minutes = seconds / 60
    else:
        minutes = int(args.minutes)
        seconds = minutes * 60

    alarm_file = get_alarm_file(args)

    if args.background:
        if minutes < 1:
            time_till_alarm = f"{seconds} seconds"
        else:
            time_till_alarm = f"{minutes} minute{'' if minutes == 1 else 's'}"

        print(f"Playing alarm in {time_till_alarm}")

        package = __package__

        cmd = f"{sys.executable} -m {package} -s {seconds} -f '{alarm_file}' &"
        os.system(cmd)
    else:
        try:
            countdown_and_play_alarm(
                seconds, alarm_file, display_timer=args.display_timer
            )
        except KeyboardInterrupt:  # pragma: no cover
            pass


if __name__ == "__main__":  # pragma: no cover
    main()
