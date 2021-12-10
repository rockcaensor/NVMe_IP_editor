import os

from locations import PCIeBlockLocation

def PathMaker(pathVar):
    NVMe_list = []
    CurrentPath = pathVar
    DirList = os.listdir(CurrentPath)
    
    for i in DirList:
        if i.rfind(".") == -1:
            continue
        else:
            if (i.split('.')[1]) != "srcs":
                continue
            else:
                CurrentPath = CurrentPath + "\\" + i + \
                "\\sources_1\\bd" 
        
    DirList = os.listdir(CurrentPath)
    
    for i in DirList:
        for dirs in (os.listdir((CurrentPath + "\\" + i))):
            if dirs == "hw_handoff":
                CurrentPath = CurrentPath + "\\" + i + "\\ip"
                exit
            else:
                continue

    DirList = os.listdir(CurrentPath)

    for i in DirList:
        if i.find("_NVMe_IP") == -1:
            continue
        else:  
            FolderName = i       
            StartOfName = i.find("_NVMe_IP") + 1 
            i = (i[StartOfName:len(FolderName)])
            IP_path = CurrentPath + "\\" + FolderName + "\\src\\NVMe_IP_xdma_0_0\\NVMe_IP_xdma_0_0.xci"
            NVMe_list.append([i, IP_path])
            print(NVMe_list)
    return(NVMe_list)



 