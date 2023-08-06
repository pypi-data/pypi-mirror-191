import click
from stochasticx.client.models import models
from stochasticx.client.datasets import datasets
from stochasticx.client.jobs import jobs
from stochasticx.client.auth import login, me, logout
from stochasticx.client.deployments import instances, deployments
from stochasticx.client.inferences import inference
from stochasticx.client.local import local

from stochasticx.client.stable_diffusion import stable_diffusion
from stochasticx.client.finetuning import finetuning_jobs
from stochasticx.client.preferences import config_command
from stochasticx.client.benchmark import benchmarking
from stochasticx.client.conversion import conversion
import stochasticx


@click.group()
@click.version_option(stochasticx.__version__)
@click.pass_context
def cli(ctx):
    pass


cli.add_command(models)
cli.add_command(datasets)
cli.add_command(jobs)
cli.add_command(login)
cli.add_command(logout)
cli.add_command(me)
cli.add_command(instances)
cli.add_command(deployments)
cli.add_command(inference)
cli.add_command(stable_diffusion)
cli.add_command(finetuning_jobs)
cli.add_command(local)
cli.add_command(config_command)
cli.add_command(benchmarking)
cli.add_command(conversion)
