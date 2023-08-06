# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import os
import codecs
import shutil
import typer
import glob

from rich import print
from pathlib import Path
from typing import List
from eboot import PlatformEnvirConfigs
from eboot import RootCMakelist
from eboot import CreateData
from eboot import CreateLib
from eboot import CreateAddons
from eboot import utils
from eboot.gtest2html import gtest2html


sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

app = typer.Typer()


def CompileVersion(option):
    print("CompileVersion__", option)
    RootCMakelist.Build(option)


def EnvConfigUpdate(option):
    CreateData.Create(option)
    CreateLib.Create(option)
    CreateAddons.Create(option)


@app.callback()
def callback():
    """
    TX1:        1     PX2:        2\n
    WINDOWS:    3     J6:         4\n
    LINUX_X86:  5     QNX:        6\n
    TDA4:       7     J3:         8\n
    J5:         10
    """


@app.command()
def config(
    set: int = typer.Option(100, "--set", "-s"),
    add: str = typer.Option(..., "--add", "-a"),
    delete: str = typer.Option(..., "--delete", "-d"),
    list: bool = typer.Option(False, "--list", "-l")
):
    print("TODO FUTURE!")


@app.command()
def clear(all: bool = typer.Option(False, "--all", "-a")):
    file_list = []

    file_list.append(os.path.join(os.getcwd(), "build_out"))
    file_list.append(os.path.join(os.getcwd(), "CMakeLists.txt"))
    file_list.append(os.path.join(
        os.getcwd(), "script/config/env_config.ini"))

    if not all:
        print("not all")
        utils.move("build_out/neo/system.xml", "./")
        utils.move("build_out/neo/globals.xml", "./")
        utils.move("build_out/neo/config.cfg", "./")

    for file in file_list:
        if os.path.exists(file):
            print("clear: " + file)
            utils.remove(file)

    if not all:
        utils.move("system.xml", "build_out/neo/")
        utils.move("globals.xml", "build_out/neo/")
        utils.move("config.cfg", "build_out/neo/")


@app.command()
def build(paltform: str, config: str):
    if os.access('./script/config/env_config.ini', os.F_OK):
        PlatformEnvirConfigs.LoadConfig()
    else:
        PlatformEnvirConfigs.SetConfig(paltform)
        EnvConfigUpdate("1")

    # Buildxx.opt
    CompileVersion(config)


@app.command()
def g2h(files: List[Path], output: Path):
    gtest2html.gtest2html(files, output)


@app.command()
def x2s(files: List[Path]):
    for file in files:
        if file.is_file():
            filedata = "\""
            output = os.path.join(os.path.dirname(
                os.path.abspath(file)), os.path.basename(file).split('.')[0] + ".inc")
            with open(file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    line = line.replace("\"", "\\\"")
                    filedata += (line[:-1] + "\\" + "\n")
            filedata += "\";"
            f.close()

            os.chdir(os.path.dirname(os.path.abspath(file)))
            if os.path.isfile(output):
                os.remove(output)
            with open(output, "w", encoding="utf-8") as f:
                f.write(filedata)
                f.close()


# if __name__ == "__main__":
#     app()
