"""Do the thing."""
import argparse
import time
from typing import Sequence
import pyautogui
from playsound import playsound


class CircleList:  # pylint: disable=too-few-public-methods
    """A datastructure that lets you call next continously."""

    def __init__(self, elements: Sequence):
        """Create a CircleList object."""
        self.elements = elements
        self.i = 0

    def next(self):
        """Return the next element in the sequence."""
        try:
            element = self.elements[self.i]
            self.i = self.i + 1
        except IndexError:
            self.i = 0
            element = self.elements[self.i]
        return element


def keep_screen_alive_entrypoint():
    """Entrypoint to keep the screen alive."""
    parser = argparse.ArgumentParser(
        prog="keep-screen-alive",
        description="Keeps the screen alive by subtly moving the mouse.",
    )
    parser.add_argument(
        "seconds", type=int, help="the number of seconds to keep the screen alive for."
    )
    args = parser.parse_args()
    print(f"Args is {args}")
    keep_screen_alive(args.seconds)


def keep_screen_alive(duration: int) -> None:
    """
    Keep the screen alive.

    @param duration: The duration to keep the screen alive.
    """
    current_time = time.time()
    circle = CircleList(
        (
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1),
        )
    )
    while current_time + duration > time.time():
        x_coord, y_coord = circle.next()
        pyautogui.moveRel(x_coord, y_coord)
        time.sleep(1)


def play_audio_entrypoint():
    """Entrypoint to play an audio file."""
    parser = argparse.ArgumentParser(
        prog="play-audio",
        description="Plays the provided audio file.",
    )
    parser.add_argument("file", help="the file to play.")
    args = parser.parse_args()
    play_audio(args.file)


def play_audio(src: str) -> None:
    """
    Play audio of some type.

    @param src:  path to the file to play.
    """
    playsound(src)
