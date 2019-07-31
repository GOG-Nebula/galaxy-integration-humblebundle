import dataclasses
import subprocess
import pathlib
import psutil
from typing import Optional

from galaxy.api.types import LocalGameState, LocalGame


@dataclasses.dataclass
class LocalHumbleGame:
    machine_name: str
    location: Optional[pathlib.Path]
    process: Optional[psutil.Process] = None
    uninstall_cmd: Optional[str] = None
    # exe: Optional[pathlib.Path]

    @property
    def is_installed(self):
        return self.location.exists()

    @property
    def is_running(self):
        if self.process is None:
            return False
        return self.process.is_running()

    @property
    def state(self):
        state = LocalGameState.None_
        if self.is_installed:
            state = LocalGameState.Installed
        if self.is_running:
            state |= LocalGameState.Running
        return state

    def in_galaxy_format(self):
        return LocalGame(self.machine_name, self.state)

    def run(self):
        import os.path
        subprocess.run(['explorer', r'/select,', os.path.normpath(self.location)])