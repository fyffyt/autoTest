#!/usr/bin/env python
#
# create by Yifei.Fu at 2015-04-22
#

TESTCASE_ID = "Tc.vworker.comp.001"
TESTCASE_PRI = "M"

import os
import sys
import time
import pexpect


if __name__ == '__main__':
    INFOSTR = """change video mode config frequently, the video module can change mode immediately"""

    #####################<prerequisites>########################
    # caller pass the workdir pathname,test conf by commandline args
    workdir = sys.argv[1]
    conf = eval(sys.argv[2])
    os.chdir(workdir)

    # load TestModules
    sys.path.append(conf["test_lib_dir"])
    import interact



