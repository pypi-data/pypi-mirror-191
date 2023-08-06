import os
import json
import random
import tempfile
from datetime import datetime, timedelta
from typing import Optional

import click
from .repo import get_commit_logs


@click.command('log')
@click.argument('repo_dir', type=click.Path(exists=True, file_okay=False), default=os.getcwd())
def log_command(repo_dir):
    """Show logs of repository commits."""

    click.echo(json.dumps(get_commit_logs(repo_dir), ensure_ascii=False, indent=4))


@click.command('commit')
@click.option('-m', '--message', help='Message describing the changes.', required=True)
@click.argument('repo_dir', type=click.Path(exists=True, file_okay=False), default=os.getcwd())
@click.pass_context
def commit_command(ctx: click.Context, message: str, repo_dir: str):
    """Record a commit on a repository."""

    config = ctx.obj['config']
    state = ctx.obj['state']

    random.seed()

    growth = config['commit']['timeGrowth']

    delta = timedelta(seconds=random.randint(growth[0], growth[1]))

    dt = datetime.fromisoformat(state['lastCommitted']) + delta
    dt_str = dt.replace(microsecond=0).astimezone().isoformat()

    cwd = os.getcwd()
    os.chdir(repo_dir)

    cmd = f'git commit -m "{message}" --date {dt_str}'
    os.system(cmd)

    os.chdir(cwd)

    state['lastCommitted'] = dt_str

    with open(ctx.obj['state_file'], 'w', encoding='utf-8') as fp:
        json.dump(state, fp, ensure_ascii=False, indent=4)


@click.command('grow')
@click.pass_context
def grow_command(ctx):
    """Grow date time of the last commit."""

    state = ctx.obj['state']

    dt = datetime.fromisoformat(state['lastCommitted']) + timedelta(hours=24)

    state['lastCommitted'] = dt.replace(hour=19, minute=0, second=0, microsecond=0).astimezone().isoformat()

    with open(ctx.obj['state_file'], 'w', encoding='utf-8') as fp:
        json.dump(state, fp, ensure_ascii=False, indent=4)

    click.echo(f'[git-timemachine] state.lastCommitted changed: {state["lastCommitted"]}')


def amend_commit(src_repo, dest_repo, log, pre_cmd: Optional[str]):
    os.chdir(src_repo)
    diff_file = tempfile.mktemp()
    os.system(f'git show --binary {log["id"]} > {diff_file}')

    if pre_cmd not in ['', None]:
        pre_cmd = pre_cmd.replace("'", "\\'")
        os.system(pre_cmd.replace('{}', f"'{diff_file}'"))

    os.chdir(dest_repo)

    msg = ''.join(log['subject'])

    if os.system(f'git apply --index --whitespace=nowarn --binary {diff_file}') != 0:
        return False

    os.system('git add .')

    if os.system("git commit --message='%s' --date='%s' > /dev/null" % (msg.replace("'", "'\"'\"'"), log['date'])) != 0:
        return False

    return True


@click.command('migrate')
@click.option('-g', '--growth', required=False, help='Time growth for each commit.')
@click.option('-e', '--execute', required=False, help='Command to execute before each commit.')
@click.argument('src_repo', type=click.Path(exists=True, file_okay=False), default=os.getcwd())
@click.argument('dest_repo', type=click.Path(exists=False, file_okay=False), default=f'{os.path.dirname(os.getcwd())}/{os.path.basename(os.getcwd())}.migrated')
def migrate_command(growth, execute, src_repo, dest_repo):
    """Migrate commit logs from a repository to another."""

    if not os.path.exists(dest_repo):
        os.mkdir(dest_repo)
        os.system(f'git init {dest_repo} > /dev/null')

    for log in reversed(get_commit_logs(src_repo)):
        seconds = 0

        if growth is not None:
            if growth[-1] == 's':
                seconds = int(growth[:-1])
            elif growth[-1] == 'm':
                seconds = int(growth[:-1]) * 60
            elif growth[-1] == 'h':
                seconds = int(growth[:-1]) * 60 * 60
            elif growth[-1] == 'd':
                seconds = int(growth[:-1]) * 60 * 60 * 24

        delta = timedelta(seconds=seconds)

        dt = datetime.fromisoformat(log['date']) + delta

        log['date'] = dt.replace(microsecond=0).astimezone().isoformat()

        if not amend_commit(src_repo, dest_repo, log, execute):
            break
