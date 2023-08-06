import os
import subprocess

import click

import libmv.image.__main__
import libmv.pitch.__main__
import libmv.pitch.evaluation
import libmv.record
import libmv.video.__main__
import libmv.watch
from libmv.util import Track


# def main(track_id: str, single: bool = False, pitch_only: bool = False):
#     Track.makedirs()
#     libmv.pitch.__main__.compute_pitches(track_id)
#     if pitch_only:
#         return
#     if single:
#         libmv.image.__main__.main(track_id, single=single)
#         libmv.video.__main__.main(track_id, single=single)
#     else:
#         libmv.image.__main__.main(track_id)
#         libmv.video.__main__.main(track_id)


# def main_docker(track_id: str, single: bool = False, pitch_only: bool = False):
#     cmd = [
#         'docker', 'run', '--rm', '-it', '--gpus', 'all',
#         '-v', f'{Track.DATA_DIRECTORY.absolute()}:/app/data',
#         'gitea.tandav.me/bhairava/libmv',
#         'python3', '-m',
#         'libmv', 'make',
#     ]
#     if single:
#         cmd.append('--single')
#     if pitch_only:
#         cmd.append('--pitch-only')
#     cmd.extend(['--track-id', track_id])
#     subprocess.check_call(cmd)


@click.group()
@click.option('--data-directory', type=str, required=False, help='directory to store data')
@click.pass_context
def cli(ctx, data_directory: str):
    ctx.obj['data_directory'] = data_directory
    pass


MAKE_OPTIONS = [
    'pitch',
    'evaluation',
    'image',
    'video',
    'image-single',
    'video-single',
]


@cli.group()
@click.option('--track-id', type=str, required=True, multiple=True, help='id of track to process')
# @click.option('--task', type=click.Choice(MAKE_OPTIONS), required=True, help='type of task to perform')
# def make(track_id: str, task: str):
@click.pass_context
def make(ctx, track_id: tuple[str]):
    ctx.obj['track_id'] = track_id


@make.command()
@click.option('--algorithm', type=str, required=True, multiple=True, help='pitch detection algorithm')
@click.option('--rescale', type=float, required=False, default=100000, help='rescale audio to fit in -rescale..rescale range')
@click.option('--save-json/--no-save-json', default=True, help='whether to save json file with pitch data')
@click.pass_context
def pitch(ctx, algorithm: str, rescale: float, save_json: bool):
    track_id = ctx.obj['track_id']
    libmv.pitch.__main__.compute_pitches(track_id, algorithm, rescale, save_json)

    # track = Track(track_id)
    # print('libmv.__main__:make', data_dir, track.audio)

    # if task != 'pitch':
    #     track_id = track_id[0]

    # if task == 'prepare-record':
    #     libmv.record.prepare_external_record(track_id)
    # elif task == 'pitch':
    #     libmv.pitch.__main__.compute_pitches(track_id)
    # elif task == 'evaluation':
    #     libmv.pitch.evaluation.main(track_id)
    # elif task == 'image':
    #     libmv.image.__main__.main(track_id)
    # elif task == 'video':
    #     libmv.video.__main__.main(track_id)
    # elif task == 'image-single':
    #     libmv.image.__main__.main(track_id, single=True)
    # elif task == 'video-single':
    #     libmv.video.__main__.main(track_id, single=True)


@cli.command()
@click.option('--path', type=str, required=True, help='path to audio file to prepare')
def prepare_record(path: str):
    libmv.record.prepare_external_record(path)


@cli.command()
def healthcheck():
    print('OK')

# @click.command()
# @click.option('--track-id', type=str, required=False, help='id of track to process')
# @click.option('--single/--no-single', default=False, help='whether to make single image (for quick vocal iterations) or images for video')
# @click.option('--pitch-only/--no-pitch-only', default=False, help='whether to only compute pitches')
# @click.pass_context
# def make(
#     ctx,
#     track_id: str,
#     single: bool,
#     pitch_only: bool,
# ):
#     if ctx.parent.command is watch:
#         if track_id is not None:
#             raise click.UsageError('track-id is not allowed when using watch')
#         libmv.watch.make(ctx.parent.params['folder'], single)
#     else:
#         if track_id is None:
#             raise click.UsageError('track-id is required')
#         if pitch_only and single:
#             raise click.UsageError('pitch-only and single are mutually exclusive')
#         main(track_id, single, pitch_only)


# @click.group()
# @click.option('--folder', type=str, required=True, help='folder to watch')
# def watch(folder: str):
#     print(f'watch {folder=}...')


# cli.add_command(make)
# cli.add_command(watch)
# watch.add_command(make)


if __name__ == '__main__':
    cli(obj={}, auto_envvar_prefix='LIBMV')
