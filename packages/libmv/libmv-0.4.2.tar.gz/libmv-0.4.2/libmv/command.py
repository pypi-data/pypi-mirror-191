import os


def build_command(
    libmv_command: list[str],
) -> list[str]:
    return [os.environ['LIBMV_PYTHON'], '-m', *libmv_command]


def build_docker_command(
    libmv_command: list[str],
    gpu: bool = False,
    env: dict[str, str] | None = None,
) -> list[str]:
    out = []
    out += ['docker', 'run', '--rm']
    if gpu:
        out += ['--gpus', 'all']
    if env is not None:
        for k, v in env.items():
            out += ['-e', f'{k}={v}']
    out += ['-v', os.environ['LIBMV_DATA_DIRECTORY'] + ':/app/data']
    out.append(os.environ['DOCKER_IMAGE'])
    out += ['python3', '-m', *libmv_command]
    return out
