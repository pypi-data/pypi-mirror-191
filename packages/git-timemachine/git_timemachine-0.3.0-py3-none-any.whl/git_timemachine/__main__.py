import os
import json
import shutil
from pathlib import Path
from pkg_resources import resource_filename

import click
from . import __version__

from .commands import log_command, commit_command, grow_command, migrate_command


def print_version(ctx: click.Context, _, value: bool):
    if not value or ctx.resilient_parsing:
        return

    click.echo(__version__)
    ctx.exit()


def init(ctx: click.Context, _, value: bool):
    if not value or ctx.resilient_parsing:
        return

    config_file = ctx.params['config_file']

    os.makedirs(os.path.dirname(config_file), 0o700, exist_ok=True)
    shutil.copyfile(resource_filename('git_timemachine', 'config.json'), config_file)
    os.chmod(config_file, 0o600)

    state_file = ctx.params['state_file']

    os.makedirs(os.path.dirname(state_file), 0o700, exist_ok=True)
    shutil.copyfile(resource_filename('git_timemachine', 'state.json'), state_file)
    os.chmod(state_file, 0o600)

    ctx.exit()


@click.group()
@click.option('--version', help='Show version information.', is_flag=True, callback=print_version, expose_value=False, is_eager=True)
@click.option('--init', help='Create essential files for git-timemachine.', is_flag=True, callback=init, expose_value=False)
@click.option('--config-file', help='Path of configuration file.', type=click.Path(dir_okay=False), default=Path(Path.home(), '.git-timemachine', 'config.json'), is_eager=True)
@click.option('--state-file', help='Path of state file.', type=click.Path(dir_okay=False), default=Path(Path.home(), '.git-timemachine', 'state.json'), is_eager=True)
@click.pass_context
def cli(ctx, config_file: str, state_file: str):
    """A command-line utility to help you manage Git commits for various time nodes."""

    ctx.ensure_object(dict)

    with open(config_file, 'r', encoding='utf-8') as fp:
        ctx.obj['config'] = json.load(fp)

    ctx.obj['config_file'] = config_file

    with open(state_file, 'r', encoding='utf-8') as fp:
        ctx.obj['state'] = json.load(fp)

    ctx.obj['state_file'] = state_file


cli.add_command(log_command)
cli.add_command(commit_command)
cli.add_command(grow_command)
cli.add_command(migrate_command)

if __name__ == '__main__':
    cli(obj={})  # pylint: disable=no-value-for-parameter
