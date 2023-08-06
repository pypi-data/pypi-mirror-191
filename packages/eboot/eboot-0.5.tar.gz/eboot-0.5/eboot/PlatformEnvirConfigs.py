#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

# different platform
platforms = {'1': 'RCAR',
             '2': 'PX2',
             '3': 'WINDOWS',
             '4': 'J6',
             '5': 'LINUX_X86',
             '6': 'QNX',
             '7': 'TDA4',
             '8': 'J3',
             '9': 'Xavier',
             '10': 'J5', }

# lib/addons dir of different platform
platform_configs = {
    'RCAR': 'linux/RCAR',
    'TDA4': 'linux/tda4',
    'WINDOWS': 'windows/x86_64',
    'LINUX_X86': 'linux/x86_64',
    'PX2': 'linux/px2',
    'QNX': 'qnx/arm64',
    'J6': 'linux/j6',
    'J3': 'linux/j3',
    'J5': 'linux/j5',
}

configs = {'PLATFORM': 'WINDOWS',
           'SCRIPT_PATH': 'F:/CodeRoot/script/',
           'INCLUDE_PATH': "F:/CodeRoot/include/",
           'LIB_PATH': 'F:/CodeRoot/lib/',
           'SRC_PATH': 'F:/CodeRoot/src/',
           'PRJ_PATH': 'F:/CodeRoot/script/prj/',
           'CFG_PATH': 'F:/CodeRoot/script/config/',
           'DATA_PATH': 'F:/CodeRoot/data/',
           'OUT_PATH': 'F:/CodeRoot/build_out/neo/',
           'ROOT_PATH': 'F:/CodeRoot',
           }
config_file = './script/config/env_config.ini'


def SetConfig(platform):
    global configs, config_file
    file_path = os.getcwd()
    configs['PLATFORM'] = platforms.get(platform, 'WINDOWS')
    configs['SCRIPT_PATH'] = os.path.join(file_path, 'script')
    configs['INCLUDE_PATH'] = os.path.join(file_path, 'include')
    configs['LIB_PATH'] = os.path.join(file_path, 'lib')
    configs['SRC_PATH'] = os.path.join(file_path, 'src')
    configs['PRJ_PATH'] = os.path.join(file_path, 'script', 'prj')
    configs['CFG_PATH'] = os.path.join(file_path, 'script', 'config')
    configs['DATA_PATH'] = os.path.join(file_path, 'data')
    configs['OUT_PATH'] = os.path.join(file_path, 'build_out', 'neo')
    configs['ROOT_PATH'] = file_path

    with open(config_file, 'w+') as fConfig:
        for key, value in configs.items():
            # windows platform, covert \ to /
            if platforms.get(platform, 'WINDOWS') == 'WINDOWS':
                value = r"/".join(value.split('\\'))

            if key != 'PLATFORM' and key != 'ROOT_PATH':
                value = value + '/'
            configs[key] = value

            data = key + '=' + value + '\n'
            fConfig.writelines(data)
    print(configs)


def LoadConfig():
    try:
        global configs, config_file
        with open(config_file, 'r') as fConfig:
            lines = fConfig.readlines()

        for line in lines:
            key, value = line.split('=')
            key, value = key.strip(), value.strip()
            configs[key] = value

        cur_path = os.getcwd()
        if configs['ROOT_PATH'] != cur_path:
            platform_dict = dict(zip(platforms.values(), platforms.keys()))
            SetConfig(platform_dict.get(configs['PLATFORM']))

        print(configs)
    except IOError:
        print('Read Config ini Failed.')
