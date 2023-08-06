import hashlib
import io
import json
import os
import shutil
from pathlib import Path

import click
import numpy as np
import pyaudio
import tqdm
from extraredis._sync import ExtraRedis
from scipy.io import wavfile

from libmv.util import Track


def record(
    seconds: float = 6,
    chunk: int = 1024,
    fs: int = 96000,
):
    FORMAT = pyaudio.paFloat32

    p = pyaudio.PyAudio()

    stream = p.open(
        format=FORMAT,
        channels=1,
        rate=fs,
        input=True,
        frames_per_buffer=chunk,
    )

    print('* recording')

    frames = []

    n_samples = int(seconds * fs)
    div, mod = divmod(n_samples, chunk)

    for _ in tqdm.trange(div):
        frames.append(stream.read(chunk))
    frames.append(stream.read(mod))

    a = np.frombuffer(b''.join(frames), dtype=np.float32)
    assert a.shape[0] == n_samples
    b = io.BytesIO()
    wavfile.write(b, fs, a)

    md5 = hashlib.md5(b.getvalue()).hexdigest()
    track = Track(md5)
    with open(track.audio, 'wb') as f:
        f.write(b.getvalue())

    with open(track.meta, 'w') as f:
        json.dump(
            {
                'record': {
                    'fs': fs,
                    'n_samples': n_samples,
                },
                'seconds': seconds,
                'track_id': md5,
            }, f,
        )

    print(f'* recording saved at {track.audio}')

    stream.stop_stream()
    stream.close()
    p.terminate()


def prepare_external_record(path: str) -> str:
    fs, a = wavfile.read(path)
    n_samples = a.shape[0]
    md5 = hashlib.md5(Path(path).read_bytes()).hexdigest()
    track = Track(md5)
    shutil.copy(path, track.audio)
    meta = {
        'fs': fs,
        'n_samples': n_samples,
        'seconds': n_samples / fs,
        'track_id': md5,
    }
    extraredis = ExtraRedis.from_url(os.environ['REDIS_URL'], decode_responses=True)
    extraredis.set(prefix='libmv:path_to_md5', key=path, value=md5)
    extraredis.set(prefix='libmv:md5_to_path', key=md5, value=path)
    extraredis.redis.hset(track.meta, mapping=meta)
    print(f'prepare done: {path} -> {track.meta}')
    return md5

