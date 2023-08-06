import json
import socket
import ssl
import time
from pathlib import Path

import libmv.__main__
from libmv import config
from libmv import record
# from pitch_detection.video import meta
from libmv.util import Track
from libmv.util import dirset


def server(
    host: str = '',
    port: int = config.port,
    certchain_path: str = config.certchain_path,
    certkey_path: str = config.certkey_path,
    chunksize: int = 1024,
):
    ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    ssl_context.load_cert_chain(certchain_path, certkey_path)
    ssl_context.load_verify_locations('fullchain-client.pem')
    ssl_context.verify_mode = ssl.CERT_REQUIRED

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((host, port))
        sock.listen(1)
        with ssl_context.wrap_socket(sock, server_side=True) as ssock:
            print(f'Listening port {port} ...')
            while True:
                conn, addr = ssock.accept()
                with conn:
                    print('Connected by', addr)
                    while True:
                        data = conn.recv(chunksize)
                        if not data:
                            break
                        print('Sending', data)
                        conn.sendall(data)


def load_db(db_path: str | Path) -> dict[str, str]:
    """source_filename to track_id"""
    fn2id = {}
    with open(db_path) as f:
        for line in f:
            fn2id.update(json.loads(line))
    return fn2id


def make(
    folder: str,
    single: bool = False,
    pitch_only: bool = False,
):
    Track.makedirs()
    folder = Path(folder)
    assert folder.exists()
    fn2id = load_db(Track.SINGLE_DONE_DB)
    docker_output_dir = Track.SINGLE_VIDEO_DIR if single else Track.VIDEO_DIR
    docker_glob = '*.mp4'

    with open(Track.SINGLE_DONE_DB, 'a') as f:
        while True:
            print(f'Watching {folder} ...')
            prepare_external_todo = dirset(folder, glob='*.wav', stem=False, absolute=True) - set(fn2id.keys())

            for p in prepare_external_todo:
                try:
                    track_id = record.prepare_external_record(p)
                except ValueError:
                    print(f'Corrupted or incomplete file, skip: {p}')
                    continue
                fn2id[p] = track_id
                f.write(json.dumps({p: track_id}) + '\n')

            docker_tasks = set(fn2id.values()) - dirset(docker_output_dir, glob=docker_glob, stem=True)
            for track_id in docker_tasks:
                print(f'Running docker task for {track_id} ...')
                libmv.__main__.main_docker(track_id, single=single, pitch_only=pitch_only)

            time.sleep(1)
