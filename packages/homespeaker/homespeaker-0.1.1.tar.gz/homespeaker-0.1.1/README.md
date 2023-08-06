# homespeaker
Code to turn a laptop into a home speaker.

## Functionality

Currently only supports scheduling "waking the screen" and "playing an alarm."  The voice interface does not yet exist, it depends on a config file to exist.

## Installation

```bash
pip install homespeaker
```

## Contributions

If you would like to see something, make an issue.  At this time I think this product is to far from "1.0" to take contributions, but happy to have a conversation on it through the issue process.

## Developer

Due to a dependency on `pyautogui`, this product requires a GUI to run.

 Action | Description
 ------ | -----------
`./build.sh setup`   | Setup a virtual environment named `venv` and get it ready for development.
`./build.sh test`    | Run linting and tests.
`./build.sh build` | Package the application into a wheel.
`./build.sh upload`  | Upload the wheel(s) to pypi.
`./build.sh clean`   | Remove a registry of generated files and folders.
