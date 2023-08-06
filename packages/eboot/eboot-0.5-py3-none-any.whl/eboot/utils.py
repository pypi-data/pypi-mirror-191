import sys
import os
import codecs
import shutil
import typer
import glob

def move(src: str, dst: str):
    if os.path.exists(src):
        realpath = os.path.realpath(dst)

        if not os.path.isdir(realpath):
            os.makedirs(realpath)

        shutil.copy(src, os.path.join(realpath, os.path.basename(src)))
        os.remove(src)


def remove(path: str):
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path)
