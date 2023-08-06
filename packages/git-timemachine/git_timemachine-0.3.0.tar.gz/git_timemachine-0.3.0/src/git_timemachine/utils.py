import shlex
import subprocess


def run_command(cmd: str, stdin: str = None, timeout: int = None, decode: str = None):
    args = shlex.split(cmd)

    p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_data, stderr_data = p.communicate(stdin, timeout)

    if decode is None:
        return p.returncode, stdout_data, stderr_data
    else:
        return p.returncode, stdout_data.decode(decode), stderr_data.decode(decode)
