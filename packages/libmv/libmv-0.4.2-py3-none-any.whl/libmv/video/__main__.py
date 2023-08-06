import json
import os
import shlex
import subprocess
import tempfile
from pathlib import Path

import click

from libmv.util import Track
from libmv.video import ffmpeg_util
from extraredis._sync import ExtraRedis


def tmp_video_from_image(imagefile: str | Path, videofile: str | Path) -> None:
    cmd = f'ffmpeg -y -r 1 -i {imagefile} -r 60 -c:v h264_nvenc -crf 60 -pix_fmt yuv420p {videofile}'
    subprocess.check_call(shlex.split(cmd))


def convert_audio_to_aac(audiofile: str | Path, aacfile: str | Path) -> None:
    cmd = f'ffmpeg -y -i {audiofile} -c:a aac {aacfile}'
    subprocess.check_call(shlex.split(cmd))


def merge_video_and_audio(videofile: str | Path, audiofile: str | Path, outfile: str | Path) -> None:
    # cmd = f'ffmpeg -y -stream_loop -1 -i {tmp_video_1} -i {audiofile} -c:v copy -c:a aac -shortest {tmp_video_2}'
    cmd = f'ffmpeg -y -stream_loop -1 -i {videofile} -i {audiofile} -codec copy -shortest {outfile}'
    subprocess.check_call(shlex.split(cmd))


def add_progresspar(videofile: str | Path, imagefile: str | Path, outfile: str | Path) -> None:
    dur = ffmpeg_util.duration(videofile)
    img_w, img_h = ffmpeg_util.img_size(imagefile)
    cmd = f'ffmpeg -y -i {videofile} -filter_complex "color=c=red:s={img_w}x{img_h},format=rgba,colorchannelmixer=aa=0.3[bar];[0][bar]overlay=-w+(w/{dur})*t:H-h:shortest=1" -c:a copy -c:v h264_nvenc -vsync cfr -r 60 -b:v 45M {outfile}'  # noqa: E501
    subprocess.check_call(shlex.split(cmd))


def main_old(audiofile: str, imagefile: str, videofile: str):

    name_id = Path(audiofile).stem

    videofile = Path(videofile)
    tmp_dir = tempfile.TemporaryDirectory()
    tmp_video_1 = Path(f'{tmp_dir.name}/{name_id}-1.mp4')
    tmp_video_2 = Path(f'{tmp_dir.name}/{name_id}-2.mp4')

    tmp_video_from_image(imagefile, tmp_video_1)

    tmp_aac = Path(f'{tmp_dir.name}/{name_id}.aac')
    convert_audio_to_aac(audiofile, tmp_aac)
    merge_video_and_audio(tmp_video_1, tmp_aac, tmp_video_2)
    add_progresspar(tmp_video_2, imagefile, videofile)
    tmp_dir.cleanup()


def main(track_id: str, single: bool = False):
    track = Track(track_id)
    assert Path(track.audio).exists()

    extraredis = ExtraRedis.from_url(os.environ['REDIS_URL'], decode_responses=True)

    if single:
        assert Path(track.single_image_background)
        cmd = 'scripts/single.sh',
        env = {
            'audiofile': track.audio,
            'imagefile': track.single_image_background,
            'videofile': track.single_video,
        }
    else:
        meta = json.loads(extraredis.redis.get(track.meta))

        assert Path(track.image_background).exists()
        assert Path(track.image_pitch).exists()
        assert Path(track.image_minimapbox).exists()

        cmd = 'scripts/scroll.sh',
        env = {
            'audiofile': track.audio,
            'img_background': track.image_background,
            'img_pitch': track.image_pitch,
            'videofile': track.video,
            'duration': str(meta['seconds']),
            'width': str(meta['image']['width']),
            'height': str(meta['image']['height']),
            'minimap_width': str(meta['image']['minimap_width']),
            'minimap_box_height': str(meta['image']['minimap_box_height']),
            'img_minimapbox': track.image_minimapbox,
        }
    subprocess.check_call(cmd, env=env)


@click.command()
@click.option('--track-id', type=str, required=True, help='id of track to process')
def _main(track_id: str):
    main(track_id)


if __name__ == '__main__':
    _main()
