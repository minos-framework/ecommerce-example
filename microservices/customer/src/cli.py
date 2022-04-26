from pathlib import Path
from typing import Optional

import typer
from minos.common import EntrypointLauncher

app = typer.Typer()


@app.command("start")
def start(
    file_path: Optional[Path] = typer.Argument(
        "config.yml", help="Microservice configuration file.", envvar="MINOS_CONFIGURATION_FILE_PATH",
    )
):
    """Start the microservice."""
    launcher = EntrypointLauncher.from_config(file_path)
    launcher.launch()


@app.callback()
def callback():
    """Minos microservice CLI."""


def main():  # pragma: no cover
    """CLI's main function."""
    app()
