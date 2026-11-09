
"""

utils/setup.py

Sets up the folder workspace for the installs and the helpers.

Calls the installers for the other tools

"""

import os 
import path
from config import *
from betterleaks-setup import *


fn = "utils/setup.py"

def setupFolders():
    try:
        folder.mkdir(exist_ok=True)
        installerFolder.mkdir(exist_ok=True)
        toolsFolder.mkdir(exist_ok=True)
        betterLeakFolder.mkdir(exist_ok=True)
        jadxFolder.mkdir(exist_ok=True)
        return True
     except Exception as e:
        print(f"{fn} An error occured : {e}")
        return False

def setupTools():
    # setup better leaks 
    if blSanityCheck() and blDownload() and blSetup():
        print(f"{fn} Installed better leaks.")
    else:
        print(f"{fn} An erro occured in installing better leaks " )
            return False
    
    # setup jadx
    
    
    
    
    
    
    
    
    
    