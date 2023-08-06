import json
import time
from pathlib import Path
import os
import click

from stochasticx.utils.docker import (
    exists_container,
    start_container,
    stop_and_remove_container,
    auto_port_selection,
    wait_container_is_up,
)
from stochasticx.utils.preferences import Preferences, AppModes
from stochasticx.benchmark.local_benchmark import LocalBenchmark
from stochasticx.models.models import Models
from stochasticx.constants.docker_images import DockerImages, ContainerNames
from stochasticx.utils.auth_utils import AuthUtils
from stochasticx.constants.urls import get_local_url, LocalRoutes
import sys

from stochasticx.utils.stat_controller import EventLogger

preferences = Preferences.load()


@click.group(name="benchmarking")
def benchmarking():
    try:
        AuthUtils.get_auth_headers()
    except:
        sys.exit()
    EventLogger.log_event("benchmarking")


@click.command(name="start")
@click.option(
    "--port",
    default=5001,
    help="Port which Stochastic local benchmark container will run on",
)
@click.option(
    "--job_name", required=True, help="Directory where the model to upload is located"
)
@click.option("--model_id", required=True, help="Id of registered model")
@click.option(
    "--task_type",
    required=True,
    help="Task type. It should be sequence_classification, token_classification, question_answering, summarization,translation",
)
@click.option(
    "--task_name",
    required=True,
    help="Name of task: onnx_benchmark, nvfuser_benchmark, tensorrt_benchmark",
)
@click.option(
    "--params_file",
    required=True,
    help="File with params for benchmarking like input information and server config",
)
def benchmarking_start(port, job_name, model_id, task_type, task_name, params_file):
    preferences = Preferences.load()
    if (
        not exists_container(ContainerNames.BENCHMARK)
        and preferences.current_mode == AppModes.LOCAL
    ):
        click.secho(
            "\n[+] We are configuring the environment for model benchmarking. If it is the first time, it will take some minutes\n",
            fg="yellow",
            bold=True,
        )

        original_port = port
        port, is_replace = auto_port_selection(port, ContainerNames.BENCHMARK)
        if is_replace:
            click.secho(
                f"[+] Port {original_port} is using on another service, port {port} will be selected to run stochasticx model benchmark",
                fg="blue",
                bold=True,
            )

        start_container(
            docker_image=DockerImages.BENCHMARK,
            ports={
                "3000": port,
            },
            container_name=ContainerNames.BENCHMARK,
            detach=True,
            gpu=True,
            volumes=["stochasticx:/vol"],
            network_links={"x-local": "x-local"},
        )

        click.echo("[+] Setting up preferences...")
        preferences = Preferences.load()
        preferences.current_mode = AppModes.LOCAL
        preferences.local_benchmark_url = f"http://127.0.0.1:{port}"
        Preferences.save(preferences)

        local_url = get_local_url(LocalRoutes.BENCHMARKING_URL, "local_benchmark_url")

        wait_container_is_up(local_url)

        click.secho(
            f"[+] x-local-benchmarking server running in the port {port}",
            fg="green",
            bold=True,
        )

    local_url = get_local_url(LocalRoutes.BENCHMARKING_URL, "local_benchmark_url")
    model = Models.get_model(model_id, "local")
    with open(params_file) as f:
        params = json.load(f)
    if preferences.current_mode == AppModes.LOCAL:
        benchmark = LocalBenchmark(
            job_name=job_name,
            task_name=task_name,
            model_type=model.model_type,
            model_path=model.directory_path,
            task_type=task_type,
            params=params,
            server_url=local_url,
        )
        click.echo("Benchmarking model...")
        result = benchmark.benchmark().json()
        if benchmark["status"] == "successful":
            click.secho(
                f"\n[+] Benchmark is done, here is the result: \n {result['message']}",
                fg="green",
                bold=True,
            )
        else:
            click.secho(
                f"\n[-] Convertion has failed, the error is:\n {str(result['message'])}",
                fg="red",
                bold=True,
            )

        if exists_container(ContainerNames.BENCHMARK):
            click.secho(
                f"[+] Stopping and removing {ContainerNames.BENCHMARK}",
                fg="blue",
                bold=True,
            )
            stop_and_remove_container(ContainerNames.BENCHMARK)
            click.secho("[+] Removed", fg="green", bold=True)
    EventLogger.log_event("benchmarking_start")


benchmarking.add_command(benchmarking_start)
