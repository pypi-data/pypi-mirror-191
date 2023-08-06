#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
copyFileCounts = 0


def copyFiles(source_dir, target_dir):
    global copyFileCounts
    print('source dir %s ---> target_dir %s ' % (source_dir, target_dir))
    print(u"%s 当前处理文件夹%s已处理%s 个文件" % (time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), source_dir, copyFileCounts))

    if os.path.isfile(source_dir):
        [sourceDir, fsrc] = os.path.split(source_dir)
        targetF = target_dir
        [targetDir, fdest] = os.path.split(target_dir)
        print(targetDir)
        print(fdest)
        print(targetF)
            
        sourceF = os.path.join(sourceDir, fsrc)
        if os.path.isfile(sourceF):
            #创建目录
            if not os.path.exists(targetDir):
                os.makedirs(targetDir)
            copyFileCounts += 1
            #文件不存在，或者存在但是大小不同，覆盖
            if not os.path.exists(targetF) or (os.path.exists(targetF) and ((os.path.getsize(targetF) != os.path.getsize(sourceF)) or (os.path.getctime(targetF) != os.path.getctime(sourceF)))):
                #2进制文件
                open(targetF, "wb").write(open(sourceF, "rb").read())
                print(u"%s %s 复制完毕" %(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), targetF))
            else:
                print(u"%s %s 已存在，不重复复制" %(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())), targetF))
        return

    if not os.path.isdir(source_dir):
        return

    for f in os.listdir(source_dir):
        sourceF = os.path.join(source_dir, f)
        targetF = os.path.join(target_dir, f)
        if os.path.isfile(sourceF):   
            #创建目录   
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            copyFileCounts += 1
            #文件不存在，或者存在但是大小不同，覆盖   
            if not os.path.exists(targetF) or (os.path.exists(targetF) and (os.path.getsize(targetF) != os.path.getsize(sourceF))):
                #2进制文件
                open(targetF, "wb").write(open(sourceF, "rb").read())
                print(u"%s %s 复制完毕" %(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), targetF))
            else:
                print(u"%s %s 已存在，不重复复制" %(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())), targetF))
           
        if os.path.isdir(sourceF):
            copyFiles(sourceF, targetF)
