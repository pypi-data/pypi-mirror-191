import signal
import sys
import time

from dls_utilpack.signal import Signal


def main():
    """
    Wait a bit then die unless interrupt comes first, exit code says what happened.
    """

    try:
        sleep_time = 2.0

        # Catch sigint signals and just count them.
        sigint_signal = Signal(signal.SIGINT)
        sigint_signal.activate()

        end_time = time.time() + sleep_time
        while time.time() < end_time:
            if sigint_signal.count() > 0:
                sys.exit(2)

        sys.exit(1)
    except Exception:
        sys.exit(-1)


# ---------------------------------------------------------------------
# Run the main program.
main()
