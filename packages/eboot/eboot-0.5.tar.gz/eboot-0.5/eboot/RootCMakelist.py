#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
from .PlatformEnvirConfigs import configs


def Build(option):
	opt_filename = "Build" + option + ".opt"
	print("opt filename", opt_filename)

	cfg_path = configs.get('CFG_PATH')
	root_path = configs.get('ROOT_PATH')
	with open(os.path.join(cfg_path, opt_filename)) as f_opt:
		line_opt = f_opt.readlines()
		shutil.copyfile(os.path.join(root_path, 'cmake/pythonCMake.txt'), os.path.join(root_path, 'CMakeLists.txt'))
		with open(os.path.join(root_path, 'CMakeLists.txt'), 'a+') as f_make:
			cmake_param = ''
			for line in line_opt:
				str_option = line.strip('\n').split(':')
				if str_option[0] == "src":
					str_src = str_option[1].strip()
					cmdline = "add_subdirectory(src/" + str_src + ")\n"
					print("opt cmdline", cmdline)
					f_make.write(cmdline)
				elif str_option[0] == "flags":
					cmake_param = str_option[1].strip()
					f_make.write('add_definitions(' + cmake_param + ')\n')
				pass

		current_path = os.getcwd()
		target_path = os.path.join(current_path, 'build_out')
		if not os.path.exists(target_path):
			os.makedirs(target_path)

		os.chdir(target_path)
		out_path = configs.get('OUT_PATH')
		script_path = configs.get('SCRIPT_PATH')
		platform = configs.get('PLATFORM')
		if platform == "WINDOWS":
			cmake_cmd = "cmake -G \"Visual Studio 14 2015\" -A x64 -DCMAKE_BUILD_TYPE=Debug .. -DPLATFORM=\"windows-opencl-caffe\" " + " -DFRAMEWORK_DIR=" + out_path
			os.system(cmake_cmd)
		elif platform == "PX2":
			cmake_cmd = "cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_TOOLCHAIN_FILE=../build/cmake/Toolchain-V4L.cmake  -DVIBRANTE_PDK:STRING=/opt/driveworks/vibrante-t186ref-linux ./"
			os.system(cmake_cmd)
			os.system("make -j16")
			os.system("make install")
		elif platform == "RCAR":
			compile_path = ". /opt/poky/2.4.2/environment-setup-aarch64-poky-linux"
			cmake_cmd = "cmake ..  -DPLATFORM=\"iecu-linux-arm64\" " + " -DFRAMEWORK_DIR=" + out_path + " "
			cmake_cmd = compile_path + " && " + cmake_cmd
			os.system(cmake_cmd)
			os.system("make -j8")
		elif platform == "J6":
			makefile_path = ". " + os.path.join(script_path, 'python', 'j6_makefile')
			cmake_cmd = "cmake ..  -DPLATFORM=\"tij6-linux-arm\" " + " -DFRAMEWORK_DIR=" + out_path + " "
			cmake_cmd = makefile_path + " && " + cmake_cmd
			os.system(cmake_cmd)
			os.system("make -j8")
		elif platform == "TDA4":
			cmake_cmd = "cmake .. -DCMAKE_SYSTEM_VERSION=\"700\" -DCMAKE_SYSTEM_PROCESSOR=\"aarch64\" -DCMAKE_TOOLCHAIN_FILE=./cmake/toolchain_tda4.cmake -G\"Unix Makefiles\" " + "-DPLATFORM=\"tda4-linux-arm64\" -DFRAMEWORK_DIR=" + out_path + " "
			os.system(cmake_cmd)
			os.system("make -j8")
		elif platform == "J3":
			cmake_cmd = "cmake .. -DCMAKE_SYSTEM_VERSION=\"700\" -DCMAKE_SYSTEM_PROCESSOR=\"aarch64\" -DCMAKE_TOOLCHAIN_FILE=./cmake/toolchain_J3.cmake -G\"Unix Makefiles\" " + "-DPLATFORM=\"tij3-linux-arm64\" -DFRAMEWORK_DIR=" + out_path + " "
			os.system(cmake_cmd)
			os.system("make -j8")
		elif platform == "LINUX_X86":
			cmake_cmd = "cmake ..  -DPLATFORM=\"linux-x86_64\"  -DCMAKE_TOOLCHAIN_FILE=./cmake/toolchain_linuxX86.cmake -G\"Unix Makefiles\" " +  " -DFRAMEWORK_DIR=" + out_path + " "
			os.system(cmake_cmd)
			os.system("make -j8")
		elif platform == "QNX":
			cmake_cmd = "cmake .. -DCMAKE_SYSTEM_VERSION=\"700\" -DCMAKE_SYSTEM_PROCESSOR=\"aarch64\" -DCMAKE_TOOLCHAIN_FILE=./cmake/toolchain_qnx.cmake -G\"Unix Makefiles\" " + "-DPLATFORM=\"iecu-qnx-arm64\" -DFRAMEWORK_DIR=" + out_path + " "
			os.system(cmake_cmd)
			os.system("make -j8")
		elif platform == "Xavier":
			cmake_cmd = "cmake .. -DCMAKE_SYSTEM_VERSION=\"700\" -DCMAKE_SYSTEM_PROCESSOR=\"aarch64\" -DCMAKE_TOOLCHAIN_FILE=./cmake/toolchain_Xavier.cmake -G\"Unix Makefiles\" " + "-DPLATFORM=\"tixavier-linux-arm64\" -DFRAMEWORK_DIR=" + out_path + " "
			os.system(cmake_cmd)
			os.system("make -j8")
		elif platform == "J5":
			export_cmd = "export LD_LIBRARY_PATH=/opt/J5/gcc-ubuntu-9.3.0-2020.03-x86_64-aarch64-linux-gnu/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH"			
			cmake_cmd = "cmake .. -DCMAKE_SYSTEM_VERSION=\"700\" -DCMAKE_SYSTEM_PROCESSOR=\"aarch64\" -DCMAKE_TOOLCHAIN_FILE=./cmake/toolchain_J5.cmake -G\"Unix Makefiles\" " + "-DPLATFORM=\"tij5-linux-arm64\"-DFRAMEWORK_DIR=" + out_path + " "
			cmake_cmd = export_cmd + " && " + cmake_cmd
			os.system(cmake_cmd)
			os.system(export_cmd + " && " + "make -j8")	
		else:
			pass
		print("%s cmake command = %s" % (platform, cmake_cmd))
		os.chdir(current_path)

