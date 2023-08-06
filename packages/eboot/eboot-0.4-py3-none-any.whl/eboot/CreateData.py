#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from .PlatformEnvirConfigs import configs
from . import Copyfiles
import shutil
import tarfile


def Create(option):
    platform = configs.get('PLATFORM')
    src_path = configs.get('SRC_PATH')
    out_path = configs.get('OUT_PATH')

    if not os.path.exists(out_path):
        os.makedirs(out_path)
    if not os.path.isfile(os.path.join(out_path, 'config.cfg')):
        shutil.copyfile(os.path.join(src_path, '../data/config/config.cfg'),
                        os.path.join(out_path, 'config.cfg'))

    global_xml = '../data/config/globals_emos2.xml'
    system_xml = '../data/config/system_emos2.xml'
    if not os.path.isfile(os.path.join(out_path, 'globals.xml')):
        shutil.copyfile(os.path.join(src_path, global_xml),
                        os.path.join(out_path, 'globals.xml'))
    if not os.path.isfile(os.path.join(out_path, 'system.xml')):
        shutil.copyfile(os.path.join(src_path, system_xml),
                        os.path.join(out_path, 'system.xml'))

    if not os.path.isfile(os.path.join(out_path, 'system.xml')):
        with open(os.path.join(out_path, 'system.xml'), "w", encoding="utf-8") as f:
            f.write("""
<emos:project xmlns:emos="emos">
    <configurations>
        <configuration url="udp://localhost:10001" description="The master for the message bus." name="system">
            <graph>
            <!-- <comp alias="service_discovery" idref="oid.emos.core.service_discovery" priority="2">
                    <settings>
                        <property value="0" type="Int" name="nClientID"/>
                        <property value="1" type="Int" name="nEcuID"/>
                        <property value="30000" type="Int" name="nSdPort"/>
                        <property value="10.10.60.77" type="String" name="strAddress"/>
                        <property value="224.1.1.11" type="String" name="strSdMultiAddress"/>
                    </settings>
                </comp> -->
            </graph>
        </configuration>
    </configurations>
</emos:project>
            """)
            f.close()

    if not os.path.isfile(os.path.join(out_path, 'globals.xml')):
        with open(os.path.join(out_path, 'globals.xml'), "w", encoding="utf-8") as f:
            f.write("""
<emos:configuration xmlns:emos="emos">
    <plugins>
        <!-- <plugin optional="true" url="sd.comp"/> -->
    </plugins>
</emos:configuration>

            """)
            f.close()
