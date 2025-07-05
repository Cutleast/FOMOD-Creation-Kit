"""
Copyright (c) Cutleast

Script for preparing and compiling the installer.iss script for the Inno Setup compiler.
"""

import subprocess
import tomllib
from pathlib import Path
from typing import Any

from semantic_version import Version

project_file = Path("pyproject.toml")
project_data: dict[str, Any] = tomllib.loads(project_file.read_text(encoding="utf8"))[
    "project"
]
project_version: Version = Version(project_data["version"])

if __name__ == "__main__":
    command: list[str] = [
        "iscc",
        "installer.iss",
        f"-DAppVersion={project_version}",
        f"-DAppExeVersion={project_version.major}.{project_version.minor}.{project_version.patch}.0",
    ]
    subprocess.run(command, check=True)
