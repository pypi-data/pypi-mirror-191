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

    Copyfiles.copyFiles(os.path.join(
        root_path, 'lib', lib_dir, 'emc'), os.path.join(out_path))
