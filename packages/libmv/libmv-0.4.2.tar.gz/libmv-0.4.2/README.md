# libmv

## dev install

```shell
pip-sync requirements.txt dev-requirements.txt
```

https://stackoverflow.com/questions/20023131/cannot-install-pyaudio-gcc-error#comment69269324_35593426

# nvidia notes
- image/video should have even dimenshions (add 1px to fix)
- my GPU support max 4096x4096 encoding using `h264_nvenc`. You should scale image down if it exceeds this size

```sh
# download single videos from server to local
rsync -avhP --delete u60:/home/tandav/docs/bhairava/libmv/data/single/video/* video/
```
