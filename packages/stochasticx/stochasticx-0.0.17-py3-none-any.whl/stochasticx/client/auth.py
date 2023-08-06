import os
from pathlib import Path
import click
from getpass import getpass
from stochasticx.utils.stat_controller import EventLogger
from stochasticx.auth.auth import Stochastic
from stochasticx.constants.urls import TOKEN_AUTH_PATH

stochastic = Stochastic()


@click.command(name="login")
@click.option("--username", help="Username for login")
@click.option("--password", help="Password for login")
def login(username, password):
    if username is None and password is None:
        stochastic.link_login()
    else:
        if username is None:
            username = input("Enter your email: ")

        if password is None:
            password = getpass()

        stochastic.login(username, password)

    click.secho("[+] Login successfully", fg="green", bold=True)
    EventLogger.log_event("login")


@click.command(name="logout")
def logout():
    token_path = Path(TOKEN_AUTH_PATH).resolve()

    if token_path.exists():
        os.remove(token_path)

    click.secho("[+] Logged out successfully", fg="green", bold=True)
    EventLogger.log_event("logout")


@click.group(name="me")
def me():
    pass


@click.command(name="profile")
def profile():
    click.secho("\n[+] Collecting profile information", fg="blue", bold=True)
    profile_info = stochastic.get_profile()
    click.secho(profile_info, bold=True)
    EventLogger.log_event("profile")


@click.command(name="company")
def company():
    company_info = stochastic.get_company()
    click.secho("\n[+] Collecting company information", fg="blue", bold=True)
    click.secho(company_info, bold=True)
    EventLogger.log_event("company")


@click.command(name="usage")
def usage():
    usage_info = stochastic.get_usage_quota()
    click.secho("\n[+] Collecting usage information", fg="blue", bold=True)
    click.secho(usage_info, bold=True)
    EventLogger.log_event("usage")


me.add_command(profile)
me.add_command(company)
me.add_command(usage)
