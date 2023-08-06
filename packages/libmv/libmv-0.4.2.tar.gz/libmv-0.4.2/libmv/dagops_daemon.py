import asyncio
import os
import collections
from pathlib import Path

from dagops import constant
from dagops.daemon import Daemon
from dagops.dependencies import get_db_cm
from dagops.dependencies import get_redis_cm
from dagops.state.schemas import InputDataDag
from dagops.state.schemas import TaskInfo
from dagops.worker import prepare_workers
from dagops.worker import run_workers
from libmv import command
from libmv.pitch.algorithms import 

LIBMV_PYTHON_PATH = '/home/tandav/.virtualenvs/libmv/bin/python'
VOLUME = '/home/tandav/docs/bhairava/libmv/data:/app/data'
REDIS_ENV = {
    'REDIS_URL': os.environ['REDIS_URL'],
}

# build_docker_image = TaskInfo(
#     command=('bash', '/home/tandav/docs/bhairava/libmv/scripts/docker-build.sh'),
#     worker_name='docker',
# )


def prepare_record_pipeline(file: str) -> InputDataDag:
    abspath = str(Path(os.environ['WATCH_DIRECTORY']) / file)
    a = TaskInfo(
        command=command.build_command(['libmv', 'prepare-record', '--path', abspath]),
        env=REDIS_ENV,
        worker_name='cpu',
    )

    # a = TaskInfo(
    #     command=[
    #         'docker', 'run', '--rm', '-it',
    #         '-v', '/home/tandav/docs/bhairava/libmv/data:/app/data',
    #         '-e', f"REDIS_URL={os.environ['REDIS_URL']}",
    #         'gitea.tandav.me/bhairava/libmv',
    #         'python3', '-m',
    #         'libmv', 'prepare-record', '--path', abspath, '--data-dir', '/app/data',
    #     ],
    #     worker_name='cpu',
    # )

    dag = {
        a: [],
    }
    return dag


def pitch_pipeline(file: list[str]) -> InputDataDag:
    tracks = [Path(f).stem for f in file]
    grouped_tracks = collections.defaultdict(list)



    dag = {}

    for track_id in tracks:
        for algorithm in cpu_algorithms:
            cpu_task = TaskInfo(
                command=command.build_command(['libmv.pitch', 'make', '--track-id', track_id, '--algorithm', algorithm]),
                env=REDIS_ENV,
                worker_name='cpu',
            )
            dag[cpu_task] = []
            grouped_tracks[track_id].append(cpu_task)


    gpu_libmv_command = ['libmv.pitch', 'make']

    for track_id in tracks:
        for algorithm in gpu_algorithms:
            gpu_libmv_command += ['--track-id', track_id, '--algorithm', algorithm]

    gpu_task = TaskInfo(
        command=command.build_docker_command(gpu_libmv_command, gpu=True, env=REDIS_ENV),
        worker_name='gpu',
    )
    dag[gpu_task] = []


    for track_id in tracks:
        merge_pitches_task = TaskInfo(
            command=command + command_rest('merge-pitches') + ['--track-id', track_id],
            worker_name='cpu',
        )

    return dag

    # command = [
    #     'docker', 'run', '--rm', '-it', '--gpus', 'all',
    #     '-v', '/home/tandav/docs/bhairava/libmv/data:/app/data',
    # ]

    # for env in ('REDIS_HOST', 'REDIS_PORT', 'REDIS_PASSWORD'):
    #     command += ['-e', f'{env}={os.environ[env]}']

    # command += [
    #     'gitea.tandav.me/bhairava/libmv',
    #     'python3', '-m',
    #     'libmv.pitch', 'make', '--task', 'pitch', '--data-dir', '/app/data',
    # ]
    # for _file in file:
    #     command += ['--track-id', Path(_file).stem]

    # pitch = TaskInfo(
    #     command=command,
    #     worker_name='gpu',
    # )

    # dag = {
    #     # build_docker_image: [],
    #     pitch: [],
    # }
    # return dag


def rest_pipeline(file: str) -> InputDataDag:
    track_id = Path(file).stem
    make_script = '/home/tandav/docs/bhairava/libmv/scripts/make.sh'

    
    
    evaluation = TaskInfo(
        command=('bash', make_script),
        env={'track_id': track_id, 'REDIS_URL': os.environ['REDIS_URL'], 'task': 'evaluation'},
        worker_name='cpu',
    )
    image = TaskInfo(
        command=('bash', make_script),
        env={'track_id': track_id, 'REDIS_URL': os.environ['REDIS_URL'], 'task': 'image'},
        worker_name='cpu',
    )
    image_single = TaskInfo(
        command=('bash', make_script),
        env={'track_id': track_id, 'REDIS_URL': os.environ['REDIS_URL'], 'task': 'image-single'},
        worker_name='cpu',
    )
    video = TaskInfo(
        command=('bash', make_script),
        env={'track_id': track_id, 'REDIS_URL': os.environ['REDIS_URL'], 'task': 'video'},
        worker_name='gpu',
    )
    video_single = TaskInfo(
        command=('bash', make_script),
        env={'track_id': track_id, 'REDIS_URL': os.environ['REDIS_URL'], 'task': 'video-single'},
        worker_name='gpu',
    )

    dag = {
        evaluation: [],
        image: [evaluation],
        image_single: [evaluation],
        video: [image],
        video_single: [image_single],
    }
    return dag


async def main():
    with (
        get_db_cm() as db,
        get_redis_cm() as redis,
    ):
        constant.SLEEP_TIME = 0.5
        constant.CHANNEL_TASK_QUEUE = f'libmv:{constant.CHANNEL_TASK_QUEUE}'
        constant.CHANNEL_TASK_STATUS = f'libmv:{constant.CHANNEL_TASK_STATUS}'
        constant.CHANNEL_AIO_TASKS = f'libmv:{constant.CHANNEL_AIO_TASKS}'
        constant.CHANNEL_FILES = f'libmv:{constant.CHANNEL_FILES}'
        constant.LIST_LOGS = f'libmv:{constant.LIST_LOGS}'
        constant.LIST_ERROR = f'libmv:{constant.LIST_ERROR}'


        workers = await prepare_workers(db, redis, workers={'cpu': 8, 'gpu': 1})
        async with asyncio.TaskGroup() as tg:
            tg.create_task(run_workers(workers))
            tg.create_task(
                Daemon(
                    watch_directory=os.environ['WATCH_DIRECTORY'],
                    db=db,
                    redis=redis,
                    create_dag_func=prepare_record_pipeline,
                )()
            )
            # tg.create_task(
            #     Daemon(
            #         watch_directory=f"{os.environ['LIBMV_DATA_DIRECTORY']}/audio",
            #         db=db,
            #         redis=redis,
            #         create_dag_func=pitch_pipeline,
            #         batch=True,
            #     )()
            # )
            # tg.create_task(
            #     Daemon(
            #         watch_directory=f"{os.environ['LIBMV_DATA_DIRECTORY']}/pitch",
            #         db=db,
            #         redis=redis,
            #         create_dag_func=rest_pipeline,
            #     )()
            # )



if __name__ == '__main__':
    asyncio.run(main())
