import os
import pack_helper.update.tags
import shutil

_test_mode = True

def do_update():
    shutil.rmtree("pack/base_content", ignore_errors=True)
    os.makedirs("pack/base_content")
    
    print("- Updating tags from KubeJS export...")
    _kubejs_export()

def _kubejs_export():
    if not _test_mode:
        shutil.rmtree("../kubejs", ignore_errors=True)
    
    _intervention()
    print("Please launch this modpack and join a world, and allow kubejs to create its tag export, then press enter.")
    print("WARNING: Do not join a world you care about! Many important scripts are missing and this *will* corrupt your save if you aren't careful.")
    print("")
    
    _wait()
    while not os.path.exists("../kubejs"):
        print("Please run the modpack.")
        _wait()
    print("")
    
    pack_helper.update.tags.make_tags_from_kubejs()    

def _intervention():
    print("")
    print("===========================")
    print("User intervention required!")
    print("===========================")
    print("")
def _wait():
    if not _test_mode:
        _ = input("Press enter to continue...")
    else:
        print("Press enter to continue... [not waiting - test mode enabled]")
