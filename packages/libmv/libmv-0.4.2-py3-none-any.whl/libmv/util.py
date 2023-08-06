import concurrent.futures
import datetime
import json
import operator
import os
import random
from pathlib import Path

import aiofiles.os
import humanize


def random_name():
    return f"{int.from_bytes(random.randbytes(8), 'little'):x}"


def dirset(
    path: str | Path,
    glob: str = '*',
    stem: bool = False,
    absolute: bool = False,
) -> set[str | Path]:
    it = Path(path).glob(glob)
    if stem and absolute:
        raise ValueError('stem and absolute are mutually exclusive')
    if stem:
        return {p.stem for p in it}
    if absolute:
        return {str(p.absolute()) for p in it}
    return set(it)


class Track:

    def __init__(self, track_id):
        self.track_id = track_id

    # @classmethod
    # def makedirs(cls):
    #     cls.DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)
    #     cls.META_DIR.mkdir(parents=True, exist_ok=True)
    #     cls.AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    #     cls.VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    #     cls.IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    #     cls.SINGLE_DIR.mkdir(parents=True, exist_ok=True)
    #     cls.SINGLE_VIDEO_DIR.mkdir(parents=True, exist_ok=True)
    #     cls.IMAGE_PITCH_DIR.mkdir(parents=True, exist_ok=True)
    #     cls.IMAGE_PIANO_DIR.mkdir(parents=True, exist_ok=True)
    #     cls.IMAGE_MINIMAP_DIR.mkdir(parents=True, exist_ok=True)
    #     cls.IMAGE_MINIMAPBOX_DIR.mkdir(parents=True, exist_ok=True)
    #     cls.IMAGE_LABELS_DIR.mkdir(parents=True, exist_ok=True)
    #     cls.IMAGE_BACKGROUND_DIR.mkdir(parents=True, exist_ok=True)
    #     cls.SINGLE_IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    #     cls.SINGLE_IMAGE_PITCH_DIR.mkdir(parents=True, exist_ok=True)
    #     cls.SINGLE_IMAGE_PIANO_DIR.mkdir(parents=True, exist_ok=True)
    #     cls.SINGLE_IMAGE_LABELS_DIR.mkdir(parents=True, exist_ok=True)
    #     cls.SINGLE_IMAGE_BACKGROUND_DIR.mkdir(parents=True, exist_ok=True)
    #     cls.SINGLE_DONE_DB.touch(exist_ok=True)

    @property
    def DATA_DIRECTORY(self):
        return Path(os.environ['LIBMV_DATA_DIRECTORY'])

    @property
    def META_DIR(self):
        return self.DATA_DIRECTORY / 'meta'

    @property
    def AUDIO_DIR(self):
        return self.DATA_DIRECTORY / 'audio'

    @property
    def VIDEO_DIR(self):
        return self.DATA_DIRECTORY / 'video'

    @property
    def IMAGE_DIR(self):
        return self.DATA_DIRECTORY / 'image'

    @property
    def IMAGE_PITCH_DIR(self):
        return self.IMAGE_DIR / 'pitch'

    @property
    def IMAGE_PIANO_DIR(self):
        return self.IMAGE_DIR / 'piano'

    @property
    def IMAGE_MINIMAP_DIR(self):
        return self.IMAGE_DIR / 'minimap'

    @property
    def IMAGE_MINIMAPBOX_DIR(self):
        return self.IMAGE_DIR / 'minimapbox'

    @property
    def IMAGE_LABELS_DIR(self):
        return self.IMAGE_DIR / 'labels'

    @property
    def IMAGE_BACKGROUND_DIR(self):
        return self.IMAGE_DIR / 'background'

    @property
    def SINGLE_DIR(self):
        return self.DATA_DIRECTORY / 'single'

    @property
    def SINGLE_IMAGE_DIR(self):
        return self.SINGLE_DIR / 'image'

    @property
    def SINGLE_IMAGE_PITCH_DIR(self):
        return self.SINGLE_IMAGE_DIR / 'pitch'

    @property
    def SINGLE_IMAGE_PIANO_DIR(self):
        return self.SINGLE_IMAGE_DIR / 'piano'

    @property
    def SINGLE_IMAGE_LABELS_DIR(self):
        return self.SINGLE_IMAGE_DIR / 'labels'

    @property
    def SINGLE_IMAGE_BACKGROUND_DIR(self):
        return self.SINGLE_IMAGE_DIR / 'background'

    @property
    def SINGLE_VIDEO_DIR(self):
        return self.SINGLE_DIR / 'video'

    @property
    def SINGLE_DONE_DB(self):
        return self.SINGLE_DIR / 'done.jsonl'

    @property
    def meta(self):
        return f'libmv:meta:{self.track_id}'

    @property
    def audio(self):
        return f'{self.AUDIO_DIR}/{self.track_id}.wav'

    def pitch_algorithm(self, algorithm: str):
        return f'libmv:pitch-partial:{algorithm}:{self.track_id}'

    @property
    def pitch(self):
        return f'libmv:pitch:{self.track_id}'

    @property
    def video(self):
        return f'{self.VIDEO_DIR}/{self.track_id}.mp4'

    @property
    def image_pitch(self):
        return f'{self.IMAGE_PITCH_DIR}/{self.track_id}.png'

    @property
    def image_minimap(self):
        return f'{self.IMAGE_MINIMAP_DIR}/{self.track_id}.png'

    @property
    def image_minimapbox(self):
        return f'{self.IMAGE_MINIMAPBOX_DIR}/{self.track_id}.png'

    @property
    def image_piano(self):
        return f'{self.IMAGE_PIANO_DIR}/{self.track_id}.png'

    @property
    def image_labels(self):
        return f'{self.IMAGE_LABELS_DIR}/{self.track_id}.png'

    @property
    def image_background(self):
        return f'{self.IMAGE_BACKGROUND_DIR}/{self.track_id}.png'

    @property
    def single_image_pitch(self):
        return f'{self.SINGLE_IMAGE_PITCH_DIR}/{self.track_id}.png'

    @property
    def single_image_piano(self):
        return f'{self.SINGLE_IMAGE_PIANO_DIR}/{self.track_id}.png'

    @property
    def single_image_labels(self):
        return f'{self.SINGLE_IMAGE_LABELS_DIR}/{self.track_id}.png'

    @property
    def single_image_background(self):
        return f'{self.SINGLE_IMAGE_BACKGROUND_DIR}/{self.track_id}.png'

    @property
    def single_video(self):
        return f'{self.SINGLE_VIDEO_DIR}/{self.track_id}.mp4'

    def is_exists(self, file: str) -> bool:
        return Path(getattr(self, file)).exists()

    def stat(self, file: str, stat: str) -> float:
        return getattr(Path(getattr(self, file)).stat(), stat)

    @property
    def mtime(self) -> float:
        return datetime.datetime.fromtimestamp(self.stat('meta', 'st_mtime'))

    @property
    def exists_info(self) -> dict[str, bool]:
        return {
            'meta': self.is_exists('meta'),
            'audio': self.is_exists('audio'),
            'pitch': self.is_exists('pitch'),
            'video': self.is_exists('video'),
            'image_pitch': self.is_exists('image_pitch'),
            'image_minimap': self.is_exists('image_minimap'),
            'image_minimapbox': self.is_exists('image_minimapbox'),
            'image_piano': self.is_exists('image_piano'),
            'image_labels': self.is_exists('image_labels'),
            'image_background': self.is_exists('image_background'),
            'single_image_pitch': self.is_exists('single_image_pitch'),
            'single_image_piano': self.is_exists('single_image_piano'),
            'single_image_labels': self.is_exists('single_image_labels'),
            'single_image_background': self.is_exists('single_image_background'),
            'single_video': self.is_exists('single_video'),
        }

    @property
    def done_info(self) -> str:
        e = self.exists_info
        done = sum(e.values())
        return f'{done}/{len(e)}'


class ErrorPool:
    def __init__(self, max_workers=None):
        self.pool = concurrent.futures.ThreadPoolExecutor(max_workers=None)
        self.tasks = []

    def submit(self, f, *args, **kwargs):
        task = self.pool.submit(f, *args, **kwargs)
        self.tasks.append(task)

    def shutdown(self):
        for task in concurrent.futures.as_completed(self.tasks):
            # if task raises an exception inside,
            # it will be raised in main thread
            task.result()
        self.pool.shutdown(wait=True)

    def __enter__(self): return self

    def __exit__(self, exc_type, exc_val, exc_tb): self.shutdown()


def format_time(
    t: datetime.datetime,
    absolute: bool = False,
    pad: bool = False,
) -> str:
    if absolute or (datetime.datetime.now() - t).days > 30:
        return t.strftime('%Y %b %d %H:%M')
    out = humanize.naturaltime(t)
    if pad:
        out = out.rjust(17)
    return out


async def path_stat(path: str) -> dict[str, float]:
    p = await aiofiles.os.stat(path)
    return {
        'created': datetime.datetime.fromtimestamp(p.st_mtime),
        'size': humanize.naturalsize(p.st_size),
    }


async def dirstat(
    path: str,
    sort_by: str | None = None,
    reverse: bool = False,
) -> list[dict]:
    out = [
        {
            'name': p.name,
            'created': datetime.datetime.fromtimestamp(p.stat().st_mtime),
            'size': humanize.naturalsize(p.stat().st_size),
        }
        for p in await aiofiles.os.scandir(path)
    ]
    if sort_by is not None:
        if sort_by not in {'name', 'created', 'size'}:
            raise ValueError(f'Invalid sort_by: {sort_by}')
        out.sort(key=operator.itemgetter(sort_by), reverse=reverse)

    return out
