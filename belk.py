import os
import hashlib

dirMap = dict()
fileMap = dict()

for root, dirs, files in os.walk(".",topdown = False):
    alist = root.split('\\')# take care of this
    dirName = alist.pop()
    hashList = []
    if dirs == [] and files == []:
        hashList.append(hashlib.sha256("".encode()).hexdigest())
        
    for direct in dirs:
        x = os.path.join(root, direct)
        hashList.append(dirMap.get(x)[0])
        
    for file in files:
        content = open(os.path.join(root,file)).read()
        sHash = hashlib.sha256(content.encode()).hexdigest()
        size = os.path.getsize(os.path.join(root,file))
        fileMap[os.path.join(root,file)] = [sHash, file, size]
        hashList.append(sHash)
        
    hashList.sort()
    str = ""
    for hshs in hashList:
        str += hshs
        
    dirHash = hashlib.sha256(str.encode()).hexdigest()
    dirMap[root] = [dirHash, dirName]
    
