"""Do the thing."""
import argparse
import datetime
import time
import os
from multiprocessing import Process
from typing import Sequence, Dict, Any
import yaml
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

action_registry = {}

class Action():  # pylint: disable=too-few-public-methods
    """Concerns itself with doing some thing."""

    def __init__(self):
        """Create the action object."""
    def do(self):  # pylint: disable=invalid-name
        """Do the action."""

def interpret_configuration(config: Dict[str, Any]) -> Sequence[Action]:
    """Change the configuration into a context."""
    action_schedulers = []
    for outer_action in config:
        for action_key in outer_action:
            action_impl = action_registry[action_key]
            action_scheduler = action_impl(outer_action[action_key])
            action_schedulers.append(action_scheduler)
    return action_schedulers

def loop_sleep():
    """Let the computer do something else."""
    time.sleep(1)

def homespeaker_entrypoint():
    """Entrypoint to start homespeaker."""
    parser = argparse.ArgumentParser(
        prog="homespeaker",
        description="Does homespeaker stuff.",
    )
    _args = parser.parse_args()
    configuration = load_configuration()
    context = interpret_configuration(configuration)
    try:
        while True:
            homespeaker(context)
            loop_sleep()
    except KeyboardInterrupt:
        pass

def load_configuration() -> Dict[str, Any]:
    """Load the configuration file if it exists."""
    if os.environ.get("XDG_CONFIG_HOME"):
        config_path = os.path.join(os.environ.get("XDG_CONFIG_HOME"), "homespeaker", "config.yaml")
    else:
        config_path = os.path.join(os.environ.get("HOME"), ".config", "homespeaker", "config.yaml")
    with open(config_path, "r", encoding="utf8") as f:  # pylint: disable=invalid-name
        return yaml.safe_load(f)

class CronActionScheduler(Action):  # pylint: disable=too-few-public-methods
    """Handle the schedule of other actions with a cron-like syntax."""

    def __init__(self, config: Dict[str, Any]):
        """Given a snippet of configuration, configure yourself."""
        minutes, hours, day_of_month, month, day_of_week = config["schedule"].split(" ")
        self.minutes = minutes
        self.hours = hours
        self.month = month
        self.day_of_month = day_of_month
        self.day_of_week = day_of_week
        self.actions = []
        for i, action_list in enumerate(config["actions"]):
            for action_key in action_list:
                action_impl = action_registry[action_key]
                action_obj = action_impl(config["actions"][i][action_key])
                self.actions.append(action_obj)
    def do(self):
        """Do the action."""
        now = datetime.datetime.now()
        if self.minutes == str(now.minute):
            if self.hours == str(now.hour):
                for action in self.actions:
                    process = Process(target=action.do, args=())
                    process.start()
                process.join()

action_registry["cron"] = CronActionScheduler

def homespeaker(context: Sequence[Action]):
    """Do homespeaker things."""
    for action_scheduler in context:
        action_scheduler.do()

def cursor_sleep():
    """Sleep between cursor movements."""
    time.sleep(1)

class KeepTheSceenAliveAction(Action):  # pylint: disable=too-few-public-methods
    """Action to keep the screen alive."""

    def __init__(self, config: Dict[str, Any]):
        """Create an object instance."""
        self.duration = config["duration"]
    def do(self):
        """
        Keep the screen alive.

        @param duration: The duration in seconds to keep the screen alive.
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
        while current_time + self.duration > time.time():
            x_coord, y_coord = circle.next()
            pyautogui.moveRel(x_coord, y_coord)
            cursor_sleep()
action_registry["light-screen"] = KeepTheSceenAliveAction

class PlayAudioAction(Action):  # pylint: disable=too-few-public-methods
    """Action to play audio."""

    def __init__(self, config: Dict[str, Any]):
        """
        Construct the Action.
        
        @param src:  path to the file to play.
        """
        self.src = config["src"]

    def do(self):
        """Play audio of some type."""
        playsound(self.src)
action_registry["play-sound"] = PlayAudioAction
