import os
import functools
import json
import multiprocessing
from pathlib import Path
from typing import Type

import click
import numpy as np
from dsplib.scale import minmax_scaler
from scipy.io import wavfile
from extraredis._sync import ExtraRedis

from libmv.pitch import algorithms
from libmv.util import Track


# @click.group()
# def cli():
#     pass


def compute_pitch(
    track_id: str,
    cls: Type[algorithms.PitchDetector],
    rescale: float = 100000,
    save_json: bool = True,
) -> algorithms.PitchDetector:
    track = Track(track_id)
    print('compute_pitch:', cls, track_id)
    # for p in (Path.cwd() / 'data').iterdir():
    #     print('->', p)
    # print('------------------ end ------------------')
    fs, a = wavfile.read(track.audio)
    a = minmax_scaler(a, a.min(), a.max(), -rescale, rescale).astype(np.float32)
    assert a.dtype == np.float32, track.audio
    p = cls(a, fs)
    if save_json:
        extraredis = ExtraRedis.from_url(os.environ['REDIS_URL'], decode_responses=True)
        p_dict = {'f0': p.f0.tolist(), 't': p.t.tolist()}
        extraredis.redis.set(track.pitch_algorithm(p.name), json.dumps(p_dict))
    return p


def compute_pitches(track_id: tuple[str], algorithm: tuple[str], rescale: float, save_json: bool) -> None:
    for _track_id in track_id:
        for _algorithm in algorithm:
            compute_pitch(_track_id, getattr(algorithms, _algorithm), rescale, save_json)


# @functools.singledispatch
# def compute_pitches(track_id) -> None:
#     ...


# @compute_pitches.register
# def compute_pitches_single(track_id: str) -> None:
#     # with concurrent.futures.ProcessPoolExecutor() as pool:
#     #     for cls in algorithms.ALGORITHMS:
#     #         pool.submit(compute_pitch, track_id, cls)
#     for cls in algorithms.ALGORITHMS:
#         compute_pitch(track_id, cls)  # single threaded is kinda faster!

#     merge_pitches(track_id)
#     add_mean_pitch(track_id)


# @compute_pitches.register
# def compute_pitmches_multiple(track_id: tuple) -> None:
#     for _track_id in track_id:
#         compute_pitches_single(_track_id)


# def compute_pitch_wrapper(
#     track_id: str,
#     cls: Type[algorithms.PitchDetector],
# ):
#     process_eval = multiprocessing.Process(target=compute_pitch, args=(track_id, cls))
#     process_eval.start()
#     process_eval.join()

#     # https://stackoverflow.com/a/60354785/4204843
#     # from numba import cuda
#     # device = cuda.get_current_device()
#     # device.reset()


# @cli.command()
# @click.option('--track-id', type=str, required=True, help='id of track to process')
# def add_mean_pitch(
#     track_id: str,
#     pitch_fs: int = 1024,
#     min_duration: float = 1,
#     min_algorithms: int = 3,
# ):
#     extraredis = ExtraRedis.from_url(os.environ['REDIS_URL'], decode_responses=True)
#     track = Track(track_id)
#     print('add_mean_pitch:', track_id)
#     pitch = json.loads(extraredis.redis.get(track.pitch))
#     seconds = float(extraredis.redis.hget(track.meta, 'seconds'))
#     single_n = int(seconds * pitch_fs)
#     t_resampled = np.linspace(0, seconds, single_n)
#     f0_resampled = {}
#     F0 = np.empty((len(pitch), single_n))
#     for i, algorithm in enumerate(pitch):
#         t = np.array(pitch[algorithm]['t'])
#         f0 = np.array(pitch[algorithm]['f0'])
#         f0_resampled[algorithm] = np.full_like(t_resampled, fill_value=np.nan)
#         notna_slices = np.ma.clump_unmasked(np.ma.masked_invalid(f0))

#         for sl in notna_slices:
#             t_slice = t[sl]
#             f0_slice = f0[sl]
#             t_start, t_stop = t_slice[0], t_slice[-1]
#             duration = t_stop - t_start
#             if duration < min_duration:
#                 continue
#             mask = (t_start < t_resampled) & (t_resampled < t_stop)
#             t_interp = t_resampled[mask]
#             f0_interp = np.interp(t_interp, t_slice, f0_slice)
#             f0_resampled[algorithm][mask] = f0_interp
#         F0[i] = f0_resampled[algorithm]

#     F0_mask = np.isfinite(F0).astype(int)
#     F0_mask_sum = F0_mask.sum(axis=0)
#     min_alg_mask = F0_mask_sum > min_algorithms
#     f0_mean = np.full_like(t_resampled, fill_value=np.nan)
#     f0_mean[min_alg_mask] = np.nanmedian(F0[:, min_alg_mask], axis=0)

#     pitch['mean'] = {'t': t_resampled.tolist(), 'f0': f0_mean.tolist()}
#     extraredis.redis.set(track.pitch, json.dumps(pitch))


# @cli.command()
# @click.option('--track-id', type=str, required=True, help='id of track to process')
# @click.option('--data-dir', type=str, required=False, default='data', help='directory to store data')
# def merge_pitches(track_id: str) -> None:
#     track = Track(track_id)
#     print('merge_pitches:', track_id)
#     pitches = {}
#     extraredis = ExtraRedis.from_url(os.environ['REDIS_URL'], decode_responses=True)
#     for cls in algorithms.ALGORITHMS:
#         pitches[cls.name] = json.loads(extraredis.redis.get(track.pitch_algorithm(cls.name)))
#     extraredis.redis.set(track.pitch, json.dumps(pitches))


# def main(track_id: str, algorithm: str) -> None:
    # compute_pitch(track_id, getattr(algorithms, algorithm))
    # call tf_wrapper() in a separate process because of GPU freeing issues


# @cli.command()
# @click.option('--track-id', type=str, required=True, multiple=True, help='id of track to process')
# @click.option('--algorithm', type=str, required=True, multiple=True, help='pitch detection algorithm')
# @click.option('--data-dir', type=str, required=False, default='data', help='directory to store data')
# def make(track_id: str, algorithm: str, data_directory: str) -> None:
#     for _track_id in track_id:
#         for _algorithm in algorithm:
#             compute_pitch(_track_id, getattr(algorithms, _algorithm))


if __name__ == '__main__':
    cli()
