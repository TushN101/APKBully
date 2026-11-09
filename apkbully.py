
import argparse
from utils.setup import setupFolders , setupTools
import os 


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="APKBully scanner.")
    parser.add_argument("option", help="Your option to run setup/scan/direct-scan")
    parser.add_argument("-i", "--input", help="Point to *.apk file or decompiled code base")
    parser.add_argument("-o", "--output", default=os.getcwd() , help="Point to *.apk file or decompiled code base")
    args = parser.parse_args()
    if args.option == "setup":
        if setupFolders() and setupTools()
            pass
        else:
            print("[err] A error occured")
            exit(-1)
    elif args.option == "scan" or args.option == "direct-scan":
        pass
    else:
        print("[err] Unknown option was passed. Check --help menu")
        exit(-1)
    
