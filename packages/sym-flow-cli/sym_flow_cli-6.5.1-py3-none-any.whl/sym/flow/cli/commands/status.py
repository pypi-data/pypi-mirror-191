from typing import Optional

import click

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.errors import SymAPIRequestError
from sym.flow.cli.helpers.api import SymAPI
from sym.flow.cli.helpers.config import Config
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.tracked_command import TrackedCommand


@click.command(cls=TrackedCommand, short_help="Check your stored auth token")
@click.make_pass_decorator(GlobalOptions, ensure=True)
def status(options: GlobalOptions) -> None:
    """Check if you have an existing login session that is still valid."""
    if options.access_token:
        check_status_by_env(options.sym_api)
    else:
        check_status_by_config(options.sym_api)


def check_status_by_env(api: SymAPI):
    validate_login(api)
    cli_output.info("   You are logged in via SYM_JWT.")


def check_status_by_config(api: SymAPI):
    if not Config.is_logged_in():
        cli_output.fail("You are not currently logged in", "Try running `symflow login`")

    org = Config.get_org().slug
    email = Config.get_email()
    validate_login(api, email)

    # not using cli_output here due to the complexity of the styling
    click.echo(f"   You are logged in to {click.style(org, bold=True)} as {click.style(email, bold=True)}.")


def validate_login(api: SymAPI, email: Optional[str] = None):
    try:
        if not api.verify_login(email):
            cli_output.fail("Token expired", "Try running `symflow login`")

        cli_output.success("✔️  Status check succeeded!")

    except SymAPIRequestError:
        cli_output.fail("A server error has occurred. Please try again later")
