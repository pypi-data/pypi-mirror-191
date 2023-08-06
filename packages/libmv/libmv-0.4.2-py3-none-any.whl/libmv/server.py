import json
from pathlib import Path

import aiofiles
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import FileResponse
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

import libmv.pitch.evaluation
from libmv import config
from libmv import util
from libmv.util import Track

static_folder = Path('data')
app = FastAPI()
app.mount('/static/', StaticFiles(directory=static_folder), name='static')
templates = Jinja2Templates(directory=static_folder / 'templates')
templates.env.filters['format_time'] = util.format_time


@app.get('/', response_class=HTMLResponse)
async def root():
    return RedirectResponse('/tracks/')


@app.get('/favicon.ico', response_class=HTMLResponse)
async def favicon():
    return FileResponse(static_folder / 'favicon.ico')


@app.get('/audios/', response_class=HTMLResponse)
async def audios(request: Request):
    audios = await util.dirstat(static_folder / 'audio', sort_by='created', reverse=True)
    return templates.TemplateResponse('audios.j2', {'audios': audios, 'request': request})


@app.get('/audios/{track_id}.wav', response_class=FileResponse)
async def audio(track_id: str):
    return FileResponse(static_folder / 'audio' / f'{track_id}.wav')


@app.get('/tracks/', response_class=HTMLResponse)
async def tracks(request: Request):
    track_ids = [x['name'].split('.')[0] for x in await util.dirstat(static_folder / 'meta', sort_by='created', reverse=True)]
    tracks = [Track(track_id) for track_id in track_ids]
    return templates.TemplateResponse('tracks.j2', {'tracks': tracks, 'request': request})


@app.get('/tracks/{track_id}.json', response_class=FileResponse)
async def track_json(track_id: str):
    return FileResponse(static_folder / 'meta' / f'{track_id}.json')


@app.get('/tracks/{track_id}', response_class=HTMLResponse)
async def track(track_id: str, request: Request):
    track = Track(track_id)
    stat = await util.path_stat(track.meta)
    async with aiofiles.open(track.meta) as f:
        meta = json.loads(await f.read())
    return templates.TemplateResponse(
        'track.j2', {
            'track': track,
            'meta': meta,
            'stat': stat,
            'request': request,
        },
    )


@app.get('/pitches/{track_id}.json', response_class=FileResponse)
async def pitch_json(track_id: str):
    return FileResponse(static_folder / 'pitch' / f'{track_id}.json')


@app.get('/videos/{track_id}.mp4', response_class=FileResponse)
async def video(track_id: str):
    return FileResponse(static_folder / 'video' / f'{track_id}.mp4')


@app.get('/videos-single/{track_id}.mp4', response_class=FileResponse)
async def video_single(track_id: str):
    return FileResponse(static_folder / 'single/video' / f'{track_id}.mp4')


@app.get('/images/{track_id}.png', response_class=FileResponse)
async def image(track_id: str):
    return FileResponse(static_folder / 'single/image/background' / f'{track_id}.png')


@app.get('/words/', response_class=HTMLResponse)
async def words(request: Request, sort: str = 'std_log2', order: str = 'desc'):
    words = await libmv.pitch.evaluation.load_words()
    words.sort(key=lambda x: x[sort], reverse=order == 'desc')
    return templates.TemplateResponse(
        'words.j2', {
            'request': request,
            'words': words,
            'sort': sort,
            'order': order,
        },
    )


@app.get('/plans/', response_class=HTMLResponse)
async def plans(request: Request):
    stats = await libmv.pitch.evaluation.plan_info()
    return templates.TemplateResponse('plans.j2', {'request': request, 'plan': config.plan, 'stats': stats})
