import json
import os
import operator

import aiofiles
import numpy as np
import pipe21 as P
from musictool.note import SpecificNote
from musictool.noterange import NoteRange
from musictool.pitch import Pitch
from extraredis._sync import ExtraRedis

import libmv.util
from libmv import config
from libmv.util import Track


def std_log2(y):
    return np.std(np.log2(y))


def mae_log2(y_true, y_pred):
    return np.mean(np.abs(np.log2(1 + y_true) - np.log2(1 + y_pred)))


def mse_log2(y_true, y_pred):
    return np.mean((np.log2(1 + y_true) - np.log2(1 + y_pred)) ** 2)


def rmse_log2(y_true, y_pred):
    return np.sqrt(mse_log2(y_true, y_pred))


def main(track_id: str) -> None:
    print(f'hello from evaluation.main {track_id = }')
    extraredis = ExtraRedis.from_url(os.environ['REDIS_URL'], decode_responses=True)
    track = Track(track_id)
    pitch = json.loads(extraredis.redis.get(track.pitch))
    meta = json.loads(extraredis.redis.get(track.meta))
    p = Pitch()
    algorithm = 'mean'
    t = np.array(pitch[algorithm]['t'])
    f0 = np.array(pitch[algorithm]['f0'])
    notna_slices = np.ma.clump_unmasked(np.ma.masked_invalid(f0))

    words = []

    for i, sl in enumerate(notna_slices):
        t_slice = t[sl]
        f0_slice = f0[sl]
        t_start, t_stop = t_slice[0], t_slice[-1]
        f0_start, f0_stop = f0_slice[0], f0_slice[-1]
        mean_hz = np.mean(f0_slice)
        closest_note = p.hz_to_note(mean_hz)
        closest_note_hz = p.note_to_hz(closest_note)
        word = {
            'word_id': f'{track_id}-{i}',
            'track_id': track_id,
            'word_index': i,
            't_start': t_start,
            't_stop': t_stop,
            'f0_start': f0_start,
            'f0_stop': f0_stop,
            'duration': t_stop - t_start,
            'closest_note': str(closest_note),
            'std_log2': std_log2(f0_slice),
            'mae_log2': mae_log2(closest_note_hz, f0_slice),
            'rmse_log2': rmse_log2(closest_note_hz, f0_slice),
        }
        words.append(word)

    meta['words'] = words
    extraredis.redis.set(track.meta, json.dumps(meta))


async def load_words() -> list[dict]:
    tracks = [
        Track(track_id)
        for track_id in
        libmv.util.dirset(Track('dummy').META_DIR, glob='*.json', stem=True)
    ]
    words = []
    for track in tracks:
        async with aiofiles.open(track.meta) as f:
            meta = json.loads(await f.read())

        if 'words' in meta:
            words += meta['words']
    return words


async def plan_info():
    words = await libmv.pitch.evaluation.load_words()

    def _correct(word):
        return word['std_log2'] < config.plan['max_std_log2']

    def _note_stats(it):
        it = list(it)
        stats = {}
        stats['min_std'] = min(it, key=operator.itemgetter('std_log2'))['std_log2']
        stats['max_std'] = max(it, key=operator.itemgetter('std_log2'))['std_log2']
        stats['min_mae'] = min(it, key=operator.itemgetter('mae_log2'))['mae_log2']
        stats['max_mae'] = max(it, key=operator.itemgetter('mae_log2'))['mae_log2']
        stats['min_rmse'] = min(it, key=operator.itemgetter('rmse_log2'))['rmse_log2']
        stats['max_rmse'] = max(it, key=operator.itemgetter('rmse_log2'))['rmse_log2']
        stats['min_duration'] = min(it, key=operator.itemgetter('duration'))['duration']
        stats['max_duration'] = max(it, key=operator.itemgetter('duration'))['duration']
        stats['n'] = len(it)
        stats['n_correct'] = sum(1 for word in it if _correct(word))
        return stats

    note_stats = (
        words
        | P.GroupBy(lambda word: word['closest_note'])
        | P.MapValues(_note_stats)
        | P.Pipe(dict)
    )

    noterange = NoteRange(SpecificNote.from_str(config.plan['note_min']), SpecificNote.from_str(config.plan['note_max']))
    out = {}
    for note in noterange:
        out[str(note)] = note_stats.get(
            str(note), {
                'min_std': None,
                'max_std': None,
                'min_mae': None,
                'max_mae': None,
                'min_rmse': None,
                'max_rmse': None,
                'min_duration': None,
                'max_duration': None,
                'n': 0,
                'n_correct': 0,
            },
        )

    return out
