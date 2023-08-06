import click
import requests
import sys
import numpy as np
from pathlib import Path
import uuid
from stochasticx.constants.urls import CloudRoutes, get_cloud_url, LocalRoutes

from stochasticx.utils.docker import (
    start_container,
    stop_and_remove_container,
    get_logs_container,
    auto_port_selection,
)

from stochasticx.datasets.datasets import Datasets
from stochasticx.stable_diffusion.download_models import download_model_from_s3
from stochasticx.utils.logging import configure_logger
from stochasticx.deployment.deployments import (
    StableDiffusionDeployments,
    StableDiffusionDeployment,
)

from stochasticx.utils.preferences import AppModes, Preferences
from stochasticx.constants.docker_images import DockerImages, ContainerNames
from stochasticx.utils.auth_utils import AuthUtils
from stochasticx.utils.stat_controller import EventLogger


# from stochasticx.utils.gpu_utils import is_nvidia_gpu_available


@click.group(name="local")
def local():
    try:
        AuthUtils.get_auth_headers()
    except:
        sys.exit()
    EventLogger.log_event("local")


@click.command(name="init")
@click.option(
    "--port", default=3000, help="Port which Stochastic local container will run on"
)
def init(port):
    try:
        AuthUtils.get_auth_headers()
    except:
        sys.exit()

    click.secho(
        "[+] Starting stochasticx in your local environment", fg="blue", bold=True
    )
    click.secho(
        "[+] If it is the first time you deploy the model, it might take some minutes to deploy it",
        fg="blue",
        bold=True,
    )

    original_port = port
    port, is_replace = auto_port_selection(port, ContainerNames.LOCAL)

    # for 2nd port
    port2, _ = auto_port_selection(5432, ContainerNames.LOCAL, selected_ports=[port])
    if is_replace:
        click.secho(
            f"[+] Port {original_port} is using on another service, port {port} will be selected to run stochasticx",
            fg="blue",
            bold=True,
        )
    start_container(
        docker_image=DockerImages.LOCAL,
        ports={"5432": port2, "3000": port},
        container_name=ContainerNames.LOCAL,
        detach=True,
        gpu=False,
        volumes=["stochasticx:/vol"],
    )

    try:
        click.echo("[+] Setting up preferences...")
        preferences = Preferences.load()
        preferences.current_mode = AppModes.LOCAL
        preferences.local_url = f"http://127.0.0.1:{port}"
        Preferences.save(preferences)
    except:
        stop()

    click.secho(f"[+] x-local server running in the port {port}", fg="green", bold=True)
    # click.echo("[+] Using GPU: {}".format(is_nvidia_gpu_available()))
    EventLogger.log_event("local_init")


@click.command(name="logs")
def logs():
    click.secho("[+] Logs", fg="blue", bold=True)
    logs = get_logs_container(ContainerNames.LOCAL)
    click.secho(logs, fg="white", bold=True)
    EventLogger.log_event("local_logs")


@click.command(name="stop")
def stop():
    click.secho("[+] Stopping and removing x-local", fg="blue", bold=True)
    stop_and_remove_container(ContainerNames.LOCAL)
    click.secho("[+] Removed", fg="green", bold=True)
    EventLogger.log_event("local_stop")


local.add_command(init)
local.add_command(logs)
local.add_command(stop)
