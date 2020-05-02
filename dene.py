import argparse
import os
import hashlib

def pair_finder(map, index):
    keys = map.keys()
    final = []
    list = []
    for x in keys:
        list.append(x)
    n = len(list)
    for i in range(0,n-2):
        for j in range(i+1,n-1):
            if map.get(list[i])[index] == map.get(list[j])[index]:
                final.append([list[i],list[j]])
                
    
    return final
def ult_pair_finder(map):
    keys = map.keys()
    final = []
    list = []
    for x in keys:
        list.append(x)
    n = len(list)
    for i in range(0,n-2):
        for j in range(i+1,n-1):
            if map.get(list[i])[0] == map.get(list[j])[0] and map.get(list[i])[1] == map.get(list[j])[1]:
                final.append([list[i],list[j]])
                
    
    return final   
    

parser = argparse.ArgumentParser(prog = 'dene')
parser.add_argument("-d", action="store_true", default = False)
parser.add_argument("-f", action="store_true",default= False)
parser.add_argument("-c",action="store_true",default= False)
parser.add_argument("-n",action="store_true",default=False)
parser.add_argument("-cn", action="store_true",default=False)
parser.add_argument("-s",action="store_true",default=False)
parser.add_argument("strings",nargs = '*',default="./")
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

for root, dirs, files in os.walk(".",topdown = False):
    alist = root.split('\\')# take care of this
    dirName = alist.pop()
    hashList = []
    dirSize = 0
    if dirs == [] and files == []:
        hashList.append(hashlib.sha256("".encode()).hexdigest())
        
    for direct in dirs:
        x = os.path.join(root, direct)
        hashList.append(dirMap.get(x)[0])
        dirSize += dirMap.get(x)[2]
        
    for file in files:
        content = open(os.path.join(root,file)).read()
        sHash = hashlib.sha256(content.encode()).hexdigest()
        size = os.path.getsize(os.path.join(root,file))
        fileMap[os.path.join(root,file)] = [sHash, file, size]
        hashList.append(sHash)
        dirSize += size
        
    hashList.sort()
    str = ""
    for hshs in hashList:
        str += hshs
        
    dirHash = hashlib.sha256(str.encode()).hexdigest()
    dirMap[root] = [dirHash, dirName,dirSize]

#now processing part
#choosing the map
finalMap = {}
if isDir:
    finalMap = dirMap
else:
    finalMap = fileMap
theList = []
if isContent and isName:
    theList = ult_pair_finder(finalMap)
elif isContent:
    theList = pair_finder(finalMap,0)
else:
    theList = pair_finder(finalMap,1)


    
    






