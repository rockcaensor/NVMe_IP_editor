
#this function returns number of line with searching string value


from locations import PCIeBlockLocation


PCIeBlockLocationValues = {"X0Y0": "0",
                           "X0Y1": "1",
                           "X0Y2": "2",
                           "X0Y3": "3",
                           "X0Y4": "4",
                           "X0Y5": "5",
                           "X1Y0": "6",
                           "X1Y1": "7",
                           "X1Y2": "8",
                           "X1Y3": "9",
                           "X1Y4": "10",
                           "X1Y5": "11"                       
                            }

def FindString(StrLst, string):    
    count = 0
    for line in StrLst:
        count += 1
        if (line.find(string) == -1):
            continue
        else:           
            return count-1;


def Set_pcie_blk_locn(filename, pcie_blc_locn_val):
    FindingPart = 'pcie_blk_locn">X'
    file = open(filename)    # export file to object "file"
    lines = file.readlines() # export lines to list "lines"
    file.close()
    StringNumber = FindString(lines, FindingPart)               # finding number of string
    SymbolNumber = lines[StringNumber].find(FindingPart)        # finding position in string
    FirstPositionOfValue = SymbolNumber+len(FindingPart) - 1    # finding position of value
    
    TempList = list(lines[StringNumber])                        #lines to list format
    
    #changing value
    for i in range(4):
        TempList[FirstPositionOfValue+i] = pcie_blc_locn_val[i]

    TempLine = ''.join(TempList) #join separated elements to string 
    
    lines[StringNumber] = TempLine

    
    FindingPart = '"MODELPARAM_VALUE.PCIE_BLK_LOCN">'      
    
    StringNumber = FindString(lines, FindingPart) 
    SymbolNumber = lines[StringNumber].find(FindingPart)        # finding position in string
    FirstPositionOfValue = SymbolNumber+len(FindingPart) 
    TempList = list(lines[StringNumber])                  
    TempList[FirstPositionOfValue] = PCIeBlockLocationValues[pcie_blc_locn_val]
    TempLine = ''.join(TempList) #join separated elements to string
    lines[StringNumber] = TempLine

    file = open(filename, 'w')
    for index in lines:
        file.write(index)

    file.close() 


def Set_quad(filename, quad):
    FindingPart = ['select_quad">', 'SELECT_QUAD">']
    file = open(filename)    # export file to object "file"
    lines = file.readlines() # export lines to list "lines"
    file.close()
    
    for parts in range(2):
        StringNumber = FindString(lines, FindingPart[parts])                       # finding number of string
        SymbolNumber = lines[StringNumber].find(FindingPart[parts])                # finding position in string
        FirstPositionOfValue = SymbolNumber+len(FindingPart[parts])            # finding position of value
        
        TempList = list(lines[StringNumber]) #lines to list format        
        
        #changing value
        for i in range(12):
            TempList[FirstPositionOfValue+i] = quad[i]

        TempLine = ''.join(TempList) #join separated elements to string         
    
        lines[StringNumber] = TempLine

    file = open(filename, 'w')
    for index in lines:
        file.write(index)

    file.close()     


def GetValues(filename):
    ValueList = []
    FindingPart = 'pcie_blk_locn">X'
    file = open(filename)    # export file to object "file"
    lines = file.readlines() # export lines to list "lines"
    file.close() 

    StringNumber = FindString(lines, FindingPart)               # finding number of string
    SymbolNumber = lines[StringNumber].find(FindingPart)        # finding position in string
    FirstPositionOfValue = SymbolNumber+len(FindingPart) - 1    # finding position of value
    ValueList.append(lines[StringNumber][FirstPositionOfValue:FirstPositionOfValue+4])

    FindingPart = 'select_quad">'    
    StringNumber = FindString(lines, FindingPart)               # finding number of string    
    SymbolNumber = lines[StringNumber].find(FindingPart)        # finding position in string    
    FirstPositionOfValue = SymbolNumber+len(FindingPart)        # finding position of value
    ValueList.append(lines[StringNumber][FirstPositionOfValue:FirstPositionOfValue+12])

    return ValueList