#!/usr/bin/python3

import sys, os

# now that we're in directory 'tools/' we have to update sys.path
mainDir = os.path.dirname(sys.path[0])
sys.path.append(mainDir)

from utils.db import DB

with DB() as db:
    result = db.execSelect("show processlist;")
    if result is not None:
        print("processlist:")
        for p in result:
            print(p)
    else:
        print("result is None")
