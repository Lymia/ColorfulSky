import os

import pack_helper.update

os.chdir(os.path.dirname(os.path.realpath(__file__)) + "/../..")

pack_helper.update.do_update()
