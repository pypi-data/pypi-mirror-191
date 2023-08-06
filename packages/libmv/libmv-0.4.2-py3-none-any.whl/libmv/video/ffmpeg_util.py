import json
import subprocess
from pathlib import Path


def ffprobe(
    filename: str,
    show_entries: str | None = None,
    show_streams: bool = False,
):
    # cmd = f'ffprobe -loglevel error -print_format json -show_streams {filename}'.split()
    cmd = ['ffprobe', '-loglevel', 'error', '-print_format', 'json']
    if show_entries:
        cmd += ['-show_entries', show_entries]
    if show_streams:
        cmd += ['-show_streams']
    cmd.append(filename)
    result = subprocess.check_output(cmd)
    return json.loads(result)


def duration(filename: str | Path) -> float:
    return float(ffprobe(filename, show_entries='format=duration')['format']['duration'])


def img_size(filename: str | Path) -> tuple[int, int]:
    return tuple(ffprobe(filename, show_entries='stream=width,height')['streams'][0].values())
