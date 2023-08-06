import importlib.resources as pkg_resources
import os

import click

import sym.flow.cli.helpers.output as cli_output
from sym.flow.cli.code_generation import (  # import the *package* containing the tf files
    approval,
)
from sym.flow.cli.errors import NotLoggedInError
from sym.flow.cli.helpers.config import Config
from sym.flow.cli.helpers.global_options import GlobalOptions
from sym.flow.cli.helpers.tracked_command import TrackedCommand


@click.command(cls=TrackedCommand, short_help="Generate starter Terraform code")
@click.make_pass_decorator(GlobalOptions, ensure=True)
@click.option(
    "--workspace-id",
    prompt=f"Slack Workspace ID {click.style('(You can find this in Slack by running /sym whoami)', dim=True, italic=True)}",
)
def init(options: GlobalOptions, workspace_id: str) -> None:
    """Generates the Terraform configuration needed to create a Sym approval-only Flow in a new directory."""

    if not Config.is_logged_in():
        raise NotLoggedInError()

    cli_output.info(
        "Welcome to Sym! This command will generate a new directory containing the Terraform and Python files needed "
        "to configure your first Sym Flow.",
        bold=True,
    )

    while True:
        init_dir = click.prompt("What should we name the directory?", type=str, prompt_suffix="")

        # Check if a file/directory already exists at the given path
        if os.path.exists(init_dir):
            cli_output.error(
                f"Looks like the directory '{init_dir}' already exists! Please provide the name for a new directory."
            )
        else:
            break

    # Create the directory
    os.makedirs(init_dir)

    # Note: The impl file is stored as a `.txt` resource because PyOxidizer (the tool used to package symflow CLI)
    # Does NOT support reading `.py` files with `importlib.resources`
    # https://github.com/indygreg/PyOxidizer/issues/237
    #
    # However, we don't care about reading the source code, we simply need to pull the text file and write it
    # to the filesystem with a `.py` extension. As a workaround, we have stored `impl.py` as `impl.txt` in the
    # code_generation.approval package so that we can read it with importlib.resources.
    static_files = [("impl.txt", "impl.py"), ("versions.tf", "versions.tf"), ("README.md", "README.md")]

    # These files don't need any values substituted in them.
    for resource_name, output_file in static_files:
        template = pkg_resources.read_text(approval, resource_name)
        with open(f"{init_dir}/{output_file}", "w") as f:
            f.write(template)

    # Fill in the org slug and workspace ID variables with values
    org = Config.get_org().slug
    main_tf = pkg_resources.read_text(approval, "main.tf")
    with open(f"{init_dir}/main.tf", "w") as f:
        main_tf = main_tf.replace("${var.sym_org_slug}", org)
        main_tf = main_tf.replace("${var.slack_workspace_id}", workspace_id.upper())

        f.write(main_tf)

    cli_output.info(
        "Successfully generated your Sym Terraform configuration! Run the following to check the configuration:"
    )
    cli_output.success(f"cd {init_dir} && terraform init && terraform plan")
    cli_output.info("\nWhen you are ready to apply your configuration, run the following:")
    cli_output.success("terraform apply")
