import argparse
from alarm import __version__
from alarm.constants import ALLOWED_EXTENSIONS


def parse_args(args):
    """Passing in args makes this easier to test:
    https://stackoverflow.com/a/18161115
    """
    parser = argparse.ArgumentParser(
        description="Play an alarm after N minutes",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    duration_group = parser.add_mutually_exclusive_group(required=True)
    duration_group.add_argument(
        "-s", "--seconds", type=int, help="Number of seconds before playing alarm"
    )
    duration_group.add_argument(
        "-m", "--minutes", type=int, help="Number of minutes before playing alarm"
    )

    run_mode_group = parser.add_mutually_exclusive_group()
    run_mode_group.add_argument(
        "-b",
        "--background",
        action="store_true",
        default=False,
        help="Run timer in the background",
    )
    run_mode_group.add_argument(
        "-d",
        "--display_timer",
        action="store_true",
        default=False,
        help="Show timer in console",
    )

    alarm_file_group = parser.add_mutually_exclusive_group()
    alarm_file_group.add_argument(
        "-l",
        "--song_library",
        help=(
            "Take a random song from a song library directory, "
            f"supported formats: {', '.join(sorted(ALLOWED_EXTENSIONS))}"
        ),
    )
    alarm_file_group.add_argument(
        "-f", "--file", help="File path to song to play as alarm"
    )
    alarm_file_group.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    return parser.parse_args(args)
