from pathlib import Path

import click
import sys
import requests
from stochasticx.utils.preferences import Preferences, AppModes
from stochasticx.constants.urls import LocalRoutes
from stochasticx.datasets.datasets import Datasets, Dataset
from stochasticx.utils.parse_utils import print_table
from stochasticx.utils.auth_utils import AuthUtils
from stochasticx.utils.spinner_slash import Spinner
from stochasticx.utils.stat_controller import EventLogger


@click.group(name="datasets")
def datasets():
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
        EventLogger.log_event("datasets")


@click.command(name="ls")
def ls_datasets():
    preferences = Preferences.load()

    click.secho("\n[+] Collecting all datasets\n", fg="blue", bold=True)
    if preferences.current_mode == AppModes.CLOUD:
        columns, values = Datasets.get_datasets(mode="cloud", fmt="table")
    else:
        columns, values = Datasets.get_datasets(mode="local", fmt="table")
    print_table(columns, values)


@click.command(name="inspect")
@click.option("--id", help="Dataset ID")
def dataset_inspect(id):
    preferences = Preferences.load()

    click.secho("\n[+] Collecting information from the dataset\n", fg="blue", bold=True)
    if preferences.current_mode == AppModes.CLOUD:
        dataset = Datasets.get_dataset("cloud", id)
        if dataset is not None:
            click.echo(dataset.dataset_info)
    else:
        dataset = Datasets.get_dataset("local", id)
        click.echo(dataset)


@click.command(name="columns")
@click.option("--id", required=True, help="Dataset ID")
def dataset_columns(id):
    preferences = Preferences.load()
    click.secho("\n[+] Collecting columns from the dataset\n", fg="blue", bold=True)
    if preferences.current_mode == AppModes.CLOUD:
        dataset = Datasets.get_dataset("cloud", id)
        if dataset is not None:
            click.echo(dataset.column_names)
    else:
        dataset = Datasets.get_dataset("local", id)
        click.echo(dataset)


@click.command(name="download")
@click.option("--id", required=True, help="Dataset ID")
@click.option(
    "--path", required=True, help="Path where the downloaded dataset will be saved"
)
def dataset_download(id, path):
    preferences = Preferences.load()
    click.secho("\n[+] Downloading dataset\n", fg="blue", bold=True)
    if preferences.current_mode == AppModes.CLOUD:
        dataset = Datasets.get_dataset("cloud", id)
        dataset.download(path)


@click.command(name="add")
@click.option(
    "--name", required=True, help="Path where the dataset to upload is located"
)
@click.option(
    "--dir_path", required=True, help="Directory where the dataset to upload is located"
)
@click.option(
    "--type", required=True, help="Dataset type. It should be hf, csv or json"
)
def dataset_add(name, dir_path, type):
    preferences = Preferences.load()

    type = type.strip()
    assert type in ["hf", "csv", "json"], "Dataset type should be hf, csv or json"
    dir_path = Path(dir_path)
    assert dir_path.is_dir(), "The path should be a directory"

    dataset = Dataset(name=name, directory_path=dir_path, dataset_type=type)

    click.secho("\n[+] Uploading dataset...\n", fg="blue", bold=True)
    if preferences.current_mode == AppModes.CLOUD:
        with Spinner():
            dataset.upload(mode="cloud")
    else:
        with Spinner():
            dataset.upload(mode="local")
    click.secho("[+] Dataset uploaded\n", fg="green", bold=True)


@click.command(name="remove")
@click.option("--dataset_id", help="ID of the dataset to be deleted")
def dataset_remove(dataset_id):
    preferences = Preferences.load()

    if preferences.current_mode == AppModes.LOCAL:
        dataset = Datasets.get_dataset("local", dataset_id)
        click.echo("Deleting the following dataset:")
        click.echo(dataset_id)

        click.confirm("Do you want to continue?", abort=True)

        Datasets.remove_local_dataset(dataset_id)
        click.echo("Deleted dataset")
        EventLogger.log_event("datasets_local_remove")


datasets.add_command(ls_datasets)
datasets.add_command(dataset_inspect)
datasets.add_command(dataset_download)
datasets.add_command(dataset_add)
datasets.add_command(dataset_remove)
datasets.add_command(dataset_columns)
