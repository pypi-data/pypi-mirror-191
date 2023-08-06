from pathlib import Path
from typing_extensions import Required

import click
import requests
import sys
from stochasticx.utils.preferences import Preferences, AppModes
from stochasticx.models.models import Models, Model
from stochasticx.utils.parse_utils import print_table
from stochasticx.constants.urls import LocalRoutes
from stochasticx.utils.auth_utils import AuthUtils
from stochasticx.utils.spinner_slash import Spinner
import sys

from stochasticx.utils.stat_controller import EventLogger

preferences = Preferences.load()


@click.group(name="models")
def models():
    try:
        AuthUtils.get_auth_headers()
    except:
        sys.exit()

    preferences = Preferences.load()

    if preferences.current_mode == AppModes.LOCAL:
        try:
            preferences = Preferences.load()
            response = requests.get(preferences.local_url)
            response.raise_for_status()
        except:
            click.secho(
                "[+] Registry is not initilized. Run the command stochasticx local init",
                fg="red",
                bold=True,
            )
            sys.exit(1)
        EventLogger.log_event("models_local")


@click.command(name="ls")
@click.option("--optimized", is_flag=True, help="Show only optimized models")
@click.option("--all", is_flag=True, help="Show all models")
def ls_models(optimized, all):
    if preferences.current_mode == AppModes.CLOUD:
        if not optimized or all:
            if all:
                click.secho("\n[+] Collecting all models\n", fg="blue", bold=True)
            else:
                click.secho("\n[+] Collecting uploaded models\n", fg="blue", bold=True)

            columns, values = Models.get_models(mode="cloud", fmt="table")
            print_table(columns, values)

        if optimized or all:
            if all:
                click.secho("\n[+] Collecting all models\n", fg="blue", bold=True)
            else:
                click.secho("\n[+] Collecting optimized models\n", fg="blue", bold=True)

            columns, values = Models.get_optimized_models(fmt="table")
            print_table(columns, values)
        EventLogger.log_event("models_cloud_ls")
    else:
        click.secho("\n[+] Collecting all local models\n", fg="blue", bold=True)
        columns, values = Models.get_models(mode="local", fmt="table")
        print_table(columns, values)
        EventLogger.log_event("models_local_ls")


@click.command(name="inspect")
@click.option("--id", required=True, help="Model ID")
def model_inspect(id):
    click.secho("\n[+] Collecting information from this model\n", fg="blue", bold=True)

    if preferences.current_mode == AppModes.CLOUD:
        model = Models.get_model(id, mode="cloud")
        click.echo(model)
    else:
        model = Models.get_model(id, mode="local")
        click.echo(model)


@click.command(name="download")
@click.option("--id", required=True, help="Model ID that you want to download")
@click.option(
    "--path", required=True, help="Path where the downloaded model will be saved"
)
def model_download(id, path):
    click.secho("\n[+] Downloading the model\n", fg="blue", bold=True)

    if preferences.current_mode == AppModes.CLOUD:
        model = Models.get_model(id, mode="cloud")
        model.download(path)
        click.secho("\n[+] Model downloaded\n", fg="green", bold=True)


@click.command(name="add")
@click.option("--name", required=True, help="Path where the model to upload is located")
@click.option(
    "--dir_path", required=True, help="Directory where the model to upload is located"
)
@click.option("--type", required=True, help="Model type. It should be hf, pt or custom")
def model_add(name, dir_path, type):
    type = type.strip()
    assert type in [
        "hf",
        "pt",
        "custom",
        "onnx",
    ], "Model type should be hf, pt or custom"
    dir_path = Path(dir_path)
    assert dir_path.is_dir(), "The path should be a directory"

    model = Model(name=name, directory_path=dir_path, model_type=type)
    click.secho("\n[+] Uploading model...\n", fg="blue", bold=True)
    with Spinner():
        if preferences.current_mode == AppModes.CLOUD:
            model.upload("cloud")
        else:
            model.upload("local")
    click.secho("\n[+] Model uploaded\n", fg="green", bold=True)


@click.command(name="remove")
@click.option("--model_id", help="ID of the model to be deleted")
def model_remove(model_id):
    if preferences.current_mode == AppModes.LOCAL:
        model = Models.get_model(model_id, mode="local")
        click.echo("Deleting the following model:")
        click.echo(model)

        click.confirm("Do you want to continue?", abort=True)

        Models.remove_local_model(model_id)
        click.echo("Deleted model")
        EventLogger.log_event("models_local_remove")


models.add_command(ls_models)
models.add_command(model_inspect)
models.add_command(model_download)
models.add_command(model_add)
models.add_command(model_remove)
