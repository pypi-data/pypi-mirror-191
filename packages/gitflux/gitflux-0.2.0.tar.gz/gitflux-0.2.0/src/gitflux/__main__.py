import json
from pathlib import Path
from typing import TextIO

import click
from github import Github
from . import __version__
from .commands import list_repos_command, create_repos_command, delete_repos_command


def print_version(ctx, _, value):
    if not value or ctx.resilient_parsing:
        return

    click.echo(__version__)
    ctx.exit()


@click.group()
@click.option('--version', help='Show version information.', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
@click.option('--config', 'config_file', help='Path of configuration file.', type=click.File(encoding='utf-8'), default=Path(Path.home(), '.gitflux', 'config.json'))
@click.pass_context
def cli(ctx: click.Context, config_file: TextIO):
    """A command-line utility to help you manage Git repositories."""

    ctx.ensure_object(dict)

    config = json.load(config_file)
    ctx.obj['github'] = Github(login_or_token=config['github']['accessToken'])


cli.add_command(list_repos_command)
cli.add_command(create_repos_command)
cli.add_command(delete_repos_command)

if __name__ == '__main__':
    cli(obj={})
