

"""
utils/betterleaks.py

Sets up the the better leaks folder

"""

from config import betterLeaksUrl
import tarfile
import requests

fn = "utils/betterleaks.py"
print(f"{fn}")    

def blSanityCheck():
    try:
        from pathlib import Path
        folder = Path.home() /  ".apkbully"
        if folder.is_dir():
            print(f"{fn} : Base folder exists")
            return True
        else:
            print(f"{fn} : Failed to find the base folder.")
            print("Presuming error in previosu workflow. Safetly exiting....")
            return False      
    except Exception as e:
        print(f"{fn} Caught an exception {e}")
        return False  

def blDownload():
    try:
        installerPath = Path.home() / ".apkbully" / "installers" / "betterleaks.tar.xz"
        response = request.get(betterLeaksUrl , timeout = 30)
        with open(installerPath , "wb") as f:
            f.write(response.content)
    except Exception as e:
        print(f"{fn} Caught an exception {e}")
        return False

def blSetup():
    try: 
        source = Path.home() / ".apkbully" / "installers" / "betterleaks.tar.xz"
        destination = Path.home() / ".apkbully" / "tools" / "betterleaks-bin"
        with tarfile.open(source, "r:xz") as tar:
            tar.extractall(path=destination)
    except Exception as e:
        catch expceiotn and print 
         return False
        
    