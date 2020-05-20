import argparse
import os
import hashlib

def get_hash(file):
    blockSize = 65536
    fileHash = hashlib.sha256()
    with open(file, "rb") as f:
        fBytes = f.read(blockSize)
        while len(fBytes) >0:
            fileHash.update(fBytes)
            fBytes = f.read(blockSize)
        
    return fileHash.hexdigest()
#pair_finder is for -n and -c options seperately
#find the duplicates for one type
def pair_finder(map, index):
    keys = map.keys()
    final = []
    list = []
    for x in keys:
        list.append(x)
    n = len(list)
    for i in range(0,n):
        if final == []:
            final.append([(list[i],map.get(list[i])[2])])
            continue
        for j in final:
            if map.get(list[i])[index] == map.get(j[0][0])[index]:
                j.append((list[i],map.get(list[i])[2]))
                break
        else:
            final.append([(list[i],map.get(list[i])[2])])
    
    result = []
    for y in final:
        if len(y) > 1:
            result.append(sorted(y, key = lambda x : x[0]))
                
    
    return result
#ult_pair_finder is for -cn options
#looks for two type of hashes at the same time
def ult_pair_finder(map):
    keys = map.keys()
    final = []
    list = []
    for x in keys:
        list.append(x)
    n = len(list)
    for i in range(0,n):
        if final == []:
            final.append([(list[i],map.get(list[i])[2])])
            continue
        for j in final:
            if map.get(list[i])[0] == map.get(j[0][0])[0] and map.get(list[i])[1] == map.get(j[0][0])[1]:
                j.append((list[i],map.get(list[i])[2]))
                break
        else:
            final.append([(list[i],map.get(list[i])[2])])
    
    result = []
    for y in final:
        if len(y) > 1:
            result.append(sorted(y, key = lambda x : x[0]))
                
    
    return result    
#the part parses the arguments controls conditions    
parser = argparse.ArgumentParser(prog = 'dene')
parser.add_argument("-d", action="store_true", default = False)
parser.add_argument("-f", action="store_true",default= False)
parser.add_argument("-c",action="store_true",default= False)
parser.add_argument("-n",action="store_true",default=False)
parser.add_argument("-cn", action="store_true",default=False)
parser.add_argument("-s",action="store_true",default=False)
parser.add_argument("strings",nargs = '*',default=["."])
args = parser.parse_args()

if args.d and args.f is True:
    print("cannot call both -d and -f")
    exit()
   
isDir = False
isFile = True
if args.d is True:
    isDir= True
    isFile= False
isContent = True
isName = False
isSize = args.s
if args.n is True:
    if args.c or args.cn is True:
        print("error")
        exit()
    isName = True
    isContent = False
    isSize = False
elif args.cn is True:
    if args.c or args.n is True:
        print("error")
        exit()
    isName = True
    isContent = True
    
dirMap = dict()
fileMap = dict()
#loop for finding all of the hashes of all directories and files
#for the given directories
for currPath in args.strings:

    for root, dirs, files in os.walk(currPath,topdown = False):
        dirName = os.path.split(root)[1]
        hashList = []
        nameHashList=[]
        marker = hashlib.sha256("directory".encode()).hexdigest()
        dirSize = 0
        rootPath = os.path.abspath(root)
        nameHash = hashlib.sha256(dirName.encode()).hexdigest()
         
        for direct in dirs:
            x = os.path.join(rootPath, direct)
            hashList.append(dirMap.get(x)[0])
            nameHashList.append(dirMap.get(x)[1])
            dirSize += dirMap.get(x)[2]
            
        for file in files:
            y = os.path.join(rootPath,file)
            sHash = get_hash(y)
            size = os.path.getsize(y)
            fnameHash = hashlib.sha256(file.encode()).hexdigest()
            fileMap[y] = [sHash, fnameHash, size]
            hashList.append(sHash)
            nameHashList.append(fnameHash)
            dirSize += size
            
        hashList.sort()
        nameHashList.sort()
        str = ""
        nameStr = nameHash
        for hshs in hashList:
            str += hshs
        for kmkm in nameHashList:
            nameStr += kmkm
        str+= marker
        nameStr += marker
        dirHash = hashlib.sha256(str.encode()).hexdigest()
        dirNameHash = hashlib.sha256(nameStr.encode()).hexdigest()
        dirMap[rootPath] = [dirHash, dirNameHash,dirSize] 

#now processing part
#choosing the map
finalMap = dict()
if isDir:
    finalMap = dirMap
else:
    finalMap = fileMap
#elimination part    
theList = []
if isContent and isName:
    theList = ult_pair_finder(finalMap)
elif isContent:
    theList = pair_finder(finalMap,0)
else:
    theList = pair_finder(finalMap,1)
theList= sorted(theList, key = lambda x : x[0][0])
if isSize:
    theList = sorted(theList, key = lambda x : x[0][1], reverse = True) 
#after elimination and sorting here is the printing part
for paths in theList:
    ch = ""
    for x in paths:
        if isSize:
            ch = x[1]
        print(x[0] , "\t", ch)
    print()    
    
