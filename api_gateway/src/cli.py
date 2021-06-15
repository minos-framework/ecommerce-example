"""
Copyright (C) 2021 Clariteia SL

This file is part of minos framework.

Minos framework can not be copied and/or distributed without the express permission of Clariteia SL.
"""
from pathlib import (
    Path,
)
from typing import (
    Optional,
)

import typer

from minos.api_gateway.common import (
    MinosConfig,
)
from minos.api_gateway.rest.launchers import (
    EntrypointLauncher,
)
from minos.api_gateway.rest.service import (
    ApiGatewayRestService,
)

app = typer.Typer()


@app.command("start")
def start(
    file_path: Optional[Path] = typer.Argument(
        "config.yml", help="API Gateway configuration file.", envvar="MINOS_API_GATEWAY_CONFIG_FILE_PATH"
    )
):  # pragma: no cover
    """Start Api Gateway services."""

    try:
        config = MinosConfig(file_path)
    except Exception as exc:
        typer.echo(f"Error loading config: {exc!r}")
        raise typer.Exit(code=1)

    services = (ApiGatewayRestService(config=config),)
    try:
        EntrypointLauncher(config=config, services=services).launch()
    except Exception as exc:
        typer.echo(f"Error launching Api Gateway: {exc!r}")
        raise typer.Exit(code=1)

    typer.echo("Api Gateway is up and running!\n")


@app.command("status")
def status():
    """Get the Api Gateway status."""
    raise NotImplementedError


@app.command("stop")
def stop():
    """Stop the Api Gateway."""
    raise NotImplementedError


def main():  # pragma: no cover
    """CLI's main function."""
    app()
