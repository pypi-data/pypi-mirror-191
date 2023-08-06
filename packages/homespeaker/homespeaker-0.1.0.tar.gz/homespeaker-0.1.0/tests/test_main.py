"""Test main module."""
from time import time
from datetime import datetime
import argparse
from argparse import Namespace
import pathlib
from typing import Tuple
import pytest
from mockito import expect, mock, any_, patch
from homespeaker import main as sut

pytestmark = pytest.mark.usefixtures("unstub")
# pylint: disable=unused-argument

def test_circle_list():
    """Test the CircleList class."""
    circle_list = sut.CircleList((1, 2, 3, 4))
    assert circle_list.next() == 1
    assert circle_list.next() == 2
    assert circle_list.next() == 3
    assert circle_list.next() == 4
    assert circle_list.next() == 1


class FakeProcess:
    """Fake out Process since that's hard to test."""

    def __init__(self, target, args):
        """Initialize the process object."""
        self.target = target
        self.args = args

    def start(self):
        """Simulate starting a process."""
        self.target(*self.args)

    def join(self):
        """Simulated joining the process."""

@pytest.fixture(name="mock_parser")
def mock_parser_fixture() -> argparse.ArgumentParser:
    """Define a mock parser"""
    mock_parser = mock(argparse.ArgumentParser)
    expect(sut.argparse).ArgumentParser(
        prog="homespeaker", description=any_()
    ).thenReturn(mock_parser)
    expect(mock_parser).parse_args().thenReturn(Namespace())
    yield mock_parser

@pytest.fixture(name="patch_process")
def patch_process_fixture() -> None:
    """Patch Process to stay in this process."""
    patch(sut.Process, FakeProcess)
    yield


@pytest.fixture(name="make_time_miss")
def make_time_match_fixture() -> Tuple[int, int]:
    """Make time not match so nothing runs."""
    minute = 5 if datetime.now().minute != 5 else 55
    hour = 5 if datetime.now().hour != 5 else 15
    yield minute, hour

def test_light_screen_when_its_time(mock_parser: argparse.ArgumentParser, patch_process):
    """Test the light-screen action when its time to run."""
    expect(sut).load_configuration().thenReturn(
        [
            {
                "cron": {
                    "schedule": f"{datetime.now().minute} {datetime.now().hour} * * *",
                    "actions": [{"light-screen": {"duration": 8}}],
                }
            },
        ]
    )
    expect(sut.pyautogui).moveRel(1, 0)
    expect(sut, times=8).cursor_sleep().thenReturn()
    expect(sut.pyautogui).moveRel(0, 1)
    expect(sut.pyautogui).moveRel(-1, 0)
    expect(sut.pyautogui).moveRel(0, -1).thenRaise(KeyboardInterrupt())
    sut.homespeaker_entrypoint()


def test_light_screen_when_its_not_time(mock_parser: argparse.ArgumentParser, make_time_miss):
    """Test the light-screen action when its not time to run."""
    minute = make_time_miss[0]
    hour = make_time_miss[1]
    expect(sut).load_configuration().thenReturn(
        [
            {
                "cron": {
                    "schedule": f"{minute} {hour} * * *",
                    "actions": [{"light-screen": {"duration": "8"}}],
                }
            },
        ]
    )
    expect(sut.time, times=4).sleep(1).thenReturn().thenReturn().thenReturn().thenRaise(
        KeyboardInterrupt()
    )
    sut.homespeaker_entrypoint()

def test_play_sound_when_its_time(mock_parser: argparse.ArgumentParser, patch_process):
    """Test the play-sound action when its time to run."""
    expect(sut).load_configuration().thenReturn(
        [
            {
                "cron": {
                    "schedule": f"{datetime.now().minute} {datetime.now().hour} * * *",
                    "actions": [{"play-sound": {"src": "sound.mp3"}}],
                }
            },
        ]
    )
    expect(sut).playsound("sound.mp3")
    expect(sut).loop_sleep().thenRaise(KeyboardInterrupt())
    sut.homespeaker_entrypoint()


def test_play_sound_when_its_not_time(mock_parser: argparse.ArgumentParser, make_time_miss):
    """Test the play-sound action when its not time to run."""
    minute = make_time_miss[0]
    hour = make_time_miss[1]
    expect(sut).load_configuration().thenReturn(
        [
            {
                "cron": {
                    "schedule": f"{minute} {hour} * * *",
                    "actions": [{"play-sound": {"src": "sound.mp3"}}],
                }
            },
        ]
    )
    expect(sut, times=4).loop_sleep().thenReturn().thenReturn().thenReturn().thenRaise(
        KeyboardInterrupt()
    )
    sut.homespeaker_entrypoint()

def test_loop_sleep():
    """Test the loop_sleep function that exists to allow easier testing."""
    before = time()
    sut.loop_sleep()
    after = time()
    assert int(after - before) == 1

def test_load_configuration_with_home_ev(tmp_path: pathlib.Path):
    """Test the load_configuration function with a HOME environment variable."""
    config_dir = tmp_path / ".config" / "homespeaker/"
    config_dir.mkdir(parents=True)
    config_file_path = config_dir / "config.yaml"
    with open(config_file_path, "w", encoding="utf8") as f:  # pylint:disable=invalid-name
        f.write((
            "---\n"
            "- cron:\n"
            "    schedule: 20 21 * * *\n"
            "    actions:\n"
            "      - light-screen:\n"
            "          duration: 8\n"
            "- cron:\n"
            "    schedule: 20 21 * * *\n"
            "    actions:\n"
            "      - play-sound:\n"
            "          src: alarm.mp3\n"
        ))
    expect(sut.os.environ).get("XDG_CONFIG_HOME").thenReturn(None)
    expect(sut.os.environ).get("HOME").thenReturn(tmp_path)
    result = sut.load_configuration()
    assert result == [
        {
            "cron": {
                "schedule": "20 21 * * *",
                "actions": [{"light-screen": {"duration": 8}}],
            }
        },
        {
            "cron": {
                "schedule": "20 21 * * *",
                "actions": [{"play-sound": {"src": "alarm.mp3"}}],
            }
        },
    ]

def test_load_configuration_with_xdg_home(tmp_path: pathlib.Path):
    """Test the load_configuration function with XDG_CONFIG_HOME environment variable."""
    config_dir = tmp_path / "homespeaker/"
    config_dir.mkdir(parents=True)
    config_file_path = config_dir / "config.yaml"
    with open(config_file_path, "w", encoding="utf8") as f:  # pylint:disable=invalid-name
        f.write((
            "---\n"
            "- cron:\n"
            "    schedule: 20 21 * * *\n"
            "    actions:\n"
            "      - light-screen:\n"
            "          duration: 8\n"
            "- cron:\n"
            "    schedule: 20 21 * * *\n"
            "    actions:\n"
            "      - play-sound:\n"
            "          src: alarm.mp3\n"
        ))
    expect(sut.os.environ, times=2).get("XDG_CONFIG_HOME").thenReturn(tmp_path)
    result = sut.load_configuration()
    assert result == [
        {
            "cron": {
                "schedule": "20 21 * * *",
                "actions": [{"light-screen": {"duration": 8}}],
            }
        },
        {
            "cron": {
                "schedule": "20 21 * * *",
                "actions": [{"play-sound": {"src": "alarm.mp3"}}],
            }
        },
    ]

def test_cursor_sleep():
    """Test the cursor_sleep function that exists to allow easier testing."""
    before = time()
    sut.cursor_sleep()
    after = time()
    assert int(after - before) == 1
