# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# --------------------------------------------------------------------------

# This file can be modified by setup.py when building a manylinux2010 wheel
# When modified, it will preload some libraries needed for the python C extension
import os
from ctypes import CDLL, RTLD_GLOBAL, util
def LoadLib(lib_name):
    lib_path = util.find_library(lib_name)
    if lib_path: _ = CDLL(lib_path, mode=RTLD_GLOBAL)
    else: _ = CDLL(lib_name, mode=RTLD_GLOBAL)
for lib_name in ["RE2", "ZLIB1"]:
    try:
        LoadLib(lib_name)
    except OSError:
        print("Could not load ort azure-ep dependency: " + lib_name)
        os.environ["ORT_" + lib_name + "_UNAVAILABLE"] = "1"
