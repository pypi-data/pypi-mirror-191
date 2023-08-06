#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from .PlatformEnvirConfigs import configs
from .PlatformEnvirConfigs import platform_configs
from . import Copyfiles


def Create(option):
    platform = configs.get('PLATFORM')
    lib_dir = platform_configs.get(platform)

    root_path = configs.get('ROOT_PATH')
    out_path = configs.get('OUT_PATH')

    if platform == "WINDOWS":
        Copyfiles.copyFiles(os.path.join(
            root_path, 'addons', lib_dir, 'ffmpeg'), os.path.join(out_path))
        Copyfiles.copyFiles(os.path.join(
            root_path, 'addons', lib_dir, 'lcm'), os.path.join(out_path))
        Copyfiles.copyFiles(os.path.join(
            root_path, 'addons', lib_dir, 'qt', 'debug'), os.path.join(out_path))
        Copyfiles.copyFiles(os.path.join(
            root_path, 'addons', lib_dir, 'qt_agent', 'c'), os.path.join(out_path))
        Copyfiles.copyFiles(os.path.join(
            root_path, 'addons', lib_dir, 'zmq'), os.path.join(out_path))
        Copyfiles.copyFiles(os.path.join(
            root_path, 'addons', lib_dir, 'commadapt'), os.path.join(out_path))
        Copyfiles.copyFiles(os.path.join(
            root_path, 'addons', lib_dir, 'opencv'), os.path.join(out_path))
    elif platform == "RCAR":
        Copyfiles.copyFiles(os.path.join(
            root_path, 'addons', lib_dir, 'commadapt'), os.path.join(out_path, 'addons'))
        Copyfiles.copyFiles(os.path.join(
            root_path, 'addons', lib_dir, 'ncnn'), os.path.join(out_path, 'addons'))
        Copyfiles.copyFiles(os.path.join(
            root_path, 'addons', lib_dir, 'ofilmneon'), os.path.join(out_path, 'addons'))
        Copyfiles.copyFiles(os.path.join(
            root_path, 'addons', lib_dir, 'rtecallback'), os.path.join(out_path, 'addons'))
        Copyfiles.copyFiles(os.path.join(
            root_path, 'addons', lib_dir, 'opencv'), os.path.join(out_path, 'addons'))
        Copyfiles.copyFiles(os.path.join(
            root_path, 'addons', lib_dir, 'mace'), os.path.join(out_path, 'addons'))
        Copyfiles.copyFiles(os.path.join(
            root_path, 'addons', lib_dir, 'zmq'), os.path.join(out_path, 'addons'))
        Copyfiles.copyFiles(os.path.join(
            root_path, 'addons', lib_dir, 'lcm'), os.path.join(out_path, 'addons'))
    else:
        pass
