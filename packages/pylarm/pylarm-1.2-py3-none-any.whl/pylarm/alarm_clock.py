"""Script to be used as a command in the terminal to set up an alarm."""

import time
import tkinter as tk
from datetime import datetime, timedelta
from os import fork

import click
import playsound


@click.command()
@click.option(
    "--at",
    type=str,
    prompt="When should the alarm go off? \
(Format: HH:MM, +HH:MM or +<seconds_to_wait>)",
    help="Time when the alarm should go off, or time to wait until it goes off. \n \
    Format: HH:MM if setting a time OR +HH:MM if setting the time to wait. \
        For the latter case, you can also wrtie +<seconds_to_wait>.",
)
@click.option("--sound", type=str, help="Sound file to play when alarm rings")
@click.option(
    "--message",
    type=str,
    help="Message to display in the dialog box",
    prompt="What message should be displayed?",
)
def alarm_clock(at, sound, message):
    """Set an alarm."""
    # Calculate the time to wait (in seconds) until the alarm goes off
    pid = fork()  # Create child process which will run in the background
    if pid == 0:  # Child process will run this
        if "+" not in at:
            delta = _compute_time_to_wait(target_time=at)
            time_to_wait = delta.total_seconds()
        else:
            # delta = _convert_to_datetime(after)
            # time_to_wait = delta.total_seconds()
            after = at.removeprefix("+")
            if ":" in after:
                time_to_wait = _after_to_seconds(after)
            else:  # Already in seconds
                time_to_wait = int(after)

        win = tk.Tk()
        win.withdraw()

        time.sleep(time_to_wait)

        # Play the alarm sound
        playsound.playsound(sound, block=False)

        # Display the dialog box with the message and a stop button
        messagebox = tk.Toplevel(win)
        # messagebox = tk.Toplevel(frame)
        messagebox.title("Alarm")
        label = tk.Label(messagebox, text=message, width=200, height=50)
        label.pack()
        stop_button = tk.Button(
            messagebox,
            text="Stop Alarm",
            command=lambda: _stop_alarm(win),
            height=20,
            width=20,
            background="red",
        )
        stop_button.pack()

        # Start the GUI event loop
        win.mainloop()
    else:  # For parent process
        print("\nAlarm was set.")


def _compute_time_to_wait(target_time):
    """Compute time to wait until `target_time`, in seconds.

    Arguments:
        target_time: str
            Time when alarm should go off. Format: HH:MM.

    Returns:
        delta: int
    """
    target_date = _convert_to_datetime(target_time)
    delta = target_date - datetime.now()
    return delta


def _convert_to_datetime(time_string):
    """Convert time HH:MM to datetime.

    Assumed date will be today if time has not passed yet and tomorrow otherwise.
    """
    time_only = datetime.strptime(time_string, "%H:%M").time()
    today = datetime.now().date()
    date_and_time = datetime.combine(today, time_only)
    now = datetime.now().time()
    if time_only < now:  # If time has already passed, alarm will go off tomorrow
        date_and_time += timedelta(days=1)
    return date_and_time


def _after_to_seconds(time_str):
    time = datetime.strptime(time_str, "%H:%M").time()
    today = datetime.now().date()
    target = datetime.combine(today, time)
    zero = datetime.min.time()
    minimum = datetime.combine(today, zero)
    return int((target - minimum).total_seconds())


def _stop_alarm(window):
    window.destroy()


if __name__ == "__main__":
    alarm_clock()
