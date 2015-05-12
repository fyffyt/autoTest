#!/usr/bin/env python

# Yifei.Fu 2015-04-27

import os
import sys
from optparse import OptionParser
from protobuf_to_dict import protobuf_to_dict

sys.path.append('./build')
from loi_pb2 import LOIPedCountData
from loi_pb2 import LOIForegroundBlobData

def parse_option_args():
    # parse the options
    parser = OptionParser()
    parser.add_option("-f", "--targetFile", help="The target file .")
    parser.add_option("-t", "--dataType", help="pedcount|foreground")
    (options, args) = parser.parse_args()
    targetFile = options.targetFile
    dataType= options.dataType

    return (targetFile, dataType)

if __name__ == '__main__':
    USAGE_STR = """interpret a protobuf file with specified type.
    python interpret_blob.py -f fileDirName -t 'pedcount'|'foreground'
    """
    (TGT_FILE, INTPRT_TYPE) = parse_option_args()

    if(None == TGT_FILE) or (None == INTPRT_TYPE):
        print(USAGE_STR)
        sys.exit(1)

    if(INTPRT_TYPE == 'pedcount'):
        MSG = LOIPedCountData()
    elif(INTPRT_TYPE == 'foreground'):
        MSG = LOIForegroundBlobData()
    else:
        print(USAGE_STR)
        sys.exit(1)

    with open(TGT_FILE,'rb') as f:
        MSG.ParseFromString(f.read())
        print(protobuf_to_dict(MSG))

