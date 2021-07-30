"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
import logging
from pathlib import Path
from typing import Optional

import typer
from minos.common import (
    EntrypointLauncher,
    MinosConfig,
)

logging.getLogger("aiohttp.access").setLevel(logging.WARNING)

app = typer.Typer()


class _MyEntrypointLauncher(EntrypointLauncher):
    async def _setup(self):
        import src

        await self.injector.wire(modules=[src] + self._internal_modules)


@app.command("start")
def start(
    file_path: Optional[Path] = typer.Argument(
        "config.yml", help="Microservice configuration file.", envvar="MINOS_CONFIGURATION_FILE_PATH",
    )
):
    """Start the microservice."""
    config = MinosConfig(file_path)
    launcher = _MyEntrypointLauncher.from_config(config=config)
    launcher.launch()


@app.callback()
def callback():
    """Minos microservice CLI."""


def main():  # pragma: no cover
    """CLI's main function."""
    app()
