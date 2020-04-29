import argparse
import os
import hashlib
parser = argparse.ArgumentParser(prog = 'dene')
parser.add_argument("-d", action="store_true", default = False)
parser.add_argument("-f", action="store_true",default= False)
parser.add_argument("-c",action="store_true",default= False)
parser.add_argument("-n",action="store_true",default=False)
parser.add_argument("-s",action="store_true",default=False)
parser.add_argument("strings",nargs = '*',default="./")
args = parser.parse_args()

if args.d and args.f is True:
    print("cannot call both -d and -f")
    exit()
    
    
isDir = 0
isFile = 1
if args.d is True:
    isDir=1
    isFile=0
    
    
print("isdir",isDir)
print("isfile",isFile) 
