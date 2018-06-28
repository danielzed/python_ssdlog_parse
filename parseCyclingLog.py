
# coding: utf-8

# In[179]:


import pandas as pd
from pandas import DataFrame,Series
import re
import os
import csv


# In[180]:


logName="summary"
logPath=logName+".log"
excelDir="excels/"
mixedExcelDir="mixedExcels/"

pathToEraseExcel=logName+"/"+excelDir+"erase.csv"
pathToProgramExcel=logName+"/"+excelDir+"program.csv"
pathToReadExcel=logName+"/"+excelDir+"read.csv"
pathToEccDistributionExcel=logName+"/"+excelDir+"eccDistribution.csv"

pathToMixedEraseExcel=logName+"/"+mixedExcelDir+"erase.csv"
pathToMixedProgramExcel=logName+"/"+mixedExcelDir+"program.csv"
pathToMixedReadExcel=logName+"/"+mixedExcelDir+"read.csv"
pattFlag=re.compile("-{5,}([^-]*)") 
pattErase=re.compile("\[\s*([0-9]+)\s*-([0-9]+)\s*-C([0-9]+)\s*-D([0-9]+)\s*-B([0-9]+)\s*\]\[\s*([0-9]+)\]")
pattProgram=re.compile("\[([0-9]+)\s*-([0-9]+)\s*-C([0-9]+)\s*-D([0-9]+)\s*-B([0-9]+)\s*-P([0-9]+)\s*-\s*([^\s]*?)\]\[\s*([0-9]+)\]")
pattRead=re.compile("\[\s*([0-9]+)\s*-([0-9]+)\s*-C([0-9]+)\s*-D([0-9]+)\s*-B([0-9]+)\s*-P([0-9]+)\s*-\s*([^\s]*?)\]\[\s*([0-9]+)\s*\]\[\s*([0-9]+)\s*\]\[\s*([0-9]+)/\s*([0-9]+)/\s*([0-9]+)/\s*([0-9]+)/\s*([0-9]+)/\s*([0-9]+)/\s*([0-9]+)/\s*([0-9]+)/\s*([0-9]+)/\s*([0-9]+)/\s*([0-9]+)/\s*([0-9]+)/\s*([0-9]+)/\s*([0-9]+)/\s*([0-9]+)/\s*([0-9]+)\]")
pattEccDis=re.compile("^([0-9]+)\s*([0-9]+)\s*([0-9]+)\s*([0-9]+)\s*")
printflag=0
groupInfo={}
pattCycleGroup=re.compile("Cycle group:[[^0-9]*([0-9]+)]+")


# In[181]:


def generateEraseExcel():
    with open(pathToEraseExcel,'w',newline='') as csvfile:
        fieldnames=["Group","PE_cnt","CE","Die","Block","tBERS" ]
        writer=csv.DictWriter(csvfile,fieldnames)
        writer.writeheader()
        flag=False
        with open(logPath,'r') as datain:
            line=datain.readline()
            while(line):
                result=pattFlag.match(line)
                if(result):
                    if(result.group(1)=="tb_Block_Erase_Operation"):
                        flag=True
                    else:
                        flag=False
                    
                if(flag):
                    result1=pattErase.match(line)
                    if(result1):
                        eraseline={}
                        for i in range(len(fieldnames)):
                            if(fieldnames[i]=='Group'):
                                eraseline[fieldnames[i]]=groupInfo[(int)(result1.group(i+1))]
                                continue
                            eraseline[fieldnames[i]]=result1.group(i+1)
                        if(printflag):
                            print(eraseline)
                        writer.writerow(eraseline)
                line=datain.readline()


# In[182]:


def generateProgramExcel():
    with open(pathToProgramExcel,'w',newline='') as csvfile:
        fieldnames=["Group","PE_cnt","CE","Die","Block","Page","Pagetype","tPROG" ]
        writer=csv.DictWriter(csvfile,fieldnames)
        writer.writeheader()
        flag=False
        with open(logPath,'r') as datain:
            line=datain.readline()
            while(line):
                result=pattFlag.match(line)
                if(result):
                    if(result.group(1)=="tb_Page_Programe_Operation"):
                        flag=True
                    else:
                        flag=False
                    
                if(flag):
                    result1=pattProgram.match(line)
                    if(result1):
                        programline={}
                        for i in range(len(fieldnames)):
                            if(fieldnames[i]=='Group'):
                                programline[fieldnames[i]]=groupInfo[(int)(result1.group(i+1))]
                                continue
                            programline[fieldnames[i]]=result1.group(i+1)
                        if(printflag):
                            print(programline)
                        writer.writerow(programline)
                line=datain.readline()


# In[183]:


def generateReadExcel():
    with open(pathToReadExcel,'w',newline='') as csvfile:
        fieldnames=["Group","PE_cnt","CE","Die","Block","Page","Pagetype","tR","Pg_err","F[0]","F[1]","F[2]","F[3]","F[4]","F[5]","F[6]","F[7]","F[8]","F[9]","F[10]","F[11]","F[12]","F[13]","F[14]","F[15]"]
        writer=csv.DictWriter(csvfile,fieldnames)
        writer.writeheader()
        flag=False
        with open(logPath,'r') as datain:
            line=datain.readline()
            while(line):
                result=pattFlag.match(line)
                if(result):
                    if(result.group(1)=="tb_Page_Read_Operation"):
                        flag=True
                    else:
                        flag=False
                    
                if(flag):
                    result1=pattRead.match(line)
                    if(result1):
                        readline={}
                        for i in range(len(fieldnames)):
                            if(fieldnames[i]=='Group'):
                                readline[fieldnames[i]]=groupInfo[(int)(result1.group(i+1))]
                                continue
                            readline[fieldnames[i]]=result1.group(i+1)
                        if(printflag):
                            print(readline)
                        writer.writerow(readline)
                line=datain.readline()


# In[184]:


def generateEccDistributionExcel():
    datamap={}
    ecclist=[]
    framecntlist=[]
    now_group_pe=""
    fieldnames=["Group","PE_cnt","ECC","Frame_Cnt"]
    flag=False
    with open(logPath,'r') as datain:
        line=datain.readline()
        while(line):
            result=pattFlag.match(line)
            if(result):
                if(result.group(1)=="ECC 1k distribution"):
                    flag=True
                else:
                    flag=False
                
            if(flag):
                result1=pattEccDis.match(line)
                
                if(result1):
                    if(now_group_pe==groupInfo[int(result1.group(1))]+'%'+result1.group(2)):
                        ecclist.append((int)(result1.group(3)))
                        framecntlist.append(result1.group(4))
                    else:
                        if(len(framecntlist)>0):
                            datamap[now_group_pe]=Series(framecntlist,index=ecclist)
                        ecclist=[]
                        framecntlist=[]
                        now_group_pe=groupInfo[int(result1.group(1))]+'%'+result1.group(2)
                        ecclist.append((int)(result1.group(3)))
                        framecntlist.append(result1.group(4))
            line=datain.readline()
        if(len(framecntlist)>0):
            datamap[now_group_pe]=Series(framecntlist,index=ecclist)
        for key in datamap.keys():
            datamap[key].name=key
        data=DataFrame(datamap)
        data.index.name='ecc_count'
        
        data.to_csv(pathToEccDistributionExcel)


# In[185]:


def generateMixedEraseExcel():
    eraseResult={}
    eraseMap={}
    now_group_pe=""
    linecnt=0
    linesum=0
    linemax=0
    fieldnames=["Group","PE_cnt","CE","Die","Block","tBERS" ]
    flag=False
    with open(logPath,'r') as datain:
        line=datain.readline()
        while(line):
            result=pattFlag.match(line)
            if(result):
                if(result.group(1)=="tb_Block_Erase_Operation"):
                    flag=True
                else:
                    flag=False

            if(flag):
                result1=pattErase.match(line)
                if(result1):
                    if(now_group_pe==result1.group(1)+'%'+result1.group(2)):
                        linesum+=(int)(result1.group(6))
                        linecnt+=1
                        linemax=max(linemax,(int)(result1.group(6)))
                    else:
                        if(linecnt>0):
                            eraseMap[now_group_pe]=Series({"Group":now_group_pe.split('%')[0],"PE_cnt":(int)(now_group_pe.split('%')[1]),"tBERS-ave":linesum/linecnt,"tBERS-max":linemax})
                        linesum=0
                        linecnt=0
                        linemax=0
                        now_group_pe=result1.group(1)+'%'+result1.group(2)
                        linesum+=(int)(result1.group(6))
                        linecnt+=1
                        linemax=max(linemax,(int)(result1.group(6)))

            line=datain.readline()
    data=DataFrame(eraseMap).T
    data.sort_values(by=['Group','PE_cnt'],inplace=True)
    data['Group']=[groupInfo[int(i)] for i in data['Group']]
    data.to_csv(pathToMixedEraseExcel)
    


# In[186]:




def generateMixedProgramExcel():
    programResult={}
    programMap={}
    now_group_pe_page_type=""
    linecnt={}
    linesum={}
    linemax={}
    fieldnames=["Group","PE_cnt","CE","Die","Block","Page","PageType","tPROG" ]
    flag=False
    with open(logPath,'r') as datain:
        line=datain.readline()
        while(line):
            result=pattFlag.match(line)
            if(result):
                if(result.group(1)=="tb_Page_Programe_Operation"):
                    flag=True
                else:
                    flag=False

            if(flag):
                result1=pattProgram.match(line)
                if(result1):
                    now_group_pe_page_pagetype=result1.group(1)+'%'+result1.group(2)+'%'+result1.group(6)+'%'+result1.group(7)
                    if(now_group_pe_page_pagetype not in linecnt.keys()):
                        linecnt[now_group_pe_page_pagetype]=1
                        linesum[now_group_pe_page_pagetype]=(int)(result1.group(8))
                        linemax[now_group_pe_page_pagetype]=(int)(result1.group(8))
                    else:
                        linecnt[now_group_pe_page_pagetype]+=1
                        linesum[now_group_pe_page_pagetype]+=(int)(result1.group(8))
                        linemax[now_group_pe_page_pagetype]=max(linemax[now_group_pe_page_pagetype],(int)(result1.group(8)))
        
            line=datain.readline()
    for key in linecnt.keys():
        programMap[key]=Series({"Group":key.split('%')[0],"PE_cnt":key.split('%')[1],"page":(int)(key.split('%')[2]),"pagetype":key.split('%')[3],"tPROG-ave":linesum[key]/linecnt[key],"tPROG-max":linemax[key]})
    data=DataFrame(programMap).T
    data.sort_values(by=['Group','PE_cnt','page'],inplace=True)
    data['Group']=[groupInfo[int(i)] for i in data['Group']]
    data.to_csv(pathToMixedProgramExcel)


# In[187]:


def generateMixedReadExcel():
    readResult={}
    readMap={}
    now_group_pe_page_pagetype=""
    linecnt={}
    linesum={}
    linemax={}
    lineerrsum={}
    lineerrmax={}
    fieldnames=["Group","PE_cnt","CE","Die","Block","Page","Pagetype","tR","Pg_err","F[0]","F[1]","F[2]","F[3]","F[4]","F[5]","F[6]","F[7]","F[8]","F[9]","F[10]","F[11]","F[12]","F[13]","F[14]","F[15]"]
    flag=False
    with open(logPath,'r') as datain:
        line=datain.readline()
        while(line):
            result=pattFlag.match(line)
            if(result):
                if(result.group(1)=="tb_Page_Read_Operation"):
                    flag=True
                else:
                    flag=False

            if(flag):
                result1=pattRead.match(line)
                if(result1):
                    now_group_pe_page_pagetype=result1.group(1)+'%'+result1.group(2)+'%'+result1.group(6)+'%'+result1.group(7)
                    if(now_group_pe_page_pagetype not in linecnt.keys()):
                        linecnt[now_group_pe_page_pagetype]=1
                        linesum[now_group_pe_page_pagetype]=(int)(result1.group(8))
                        linemax[now_group_pe_page_pagetype]=(int)(result1.group(8))
                        lineerrsum[now_group_pe_page_pagetype]=(int)(result1.group(9))
                        lineerrmax[now_group_pe_page_pagetype]=(int)(result1.group(9))
                    else:
                        linecnt[now_group_pe_page_pagetype]+=1
                        linesum[now_group_pe_page_pagetype]+=(int)(result1.group(8))
                        linemax[now_group_pe_page_pagetype]=max((int)(result1.group(8)),linemax[now_group_pe_page_pagetype])
                        lineerrsum[now_group_pe_page_pagetype]+=(int)(result1.group(9))
                        lineerrmax[now_group_pe_page_pagetype]=max((int)(result1.group(9)),lineerrmax[now_group_pe_page_pagetype])
            line=datain.readline()
    for key in linecnt.keys():
        readMap[key]=Series({"Group":key.split('%')[0],"PE_cnt":key.split('%')[1],"page":(int)(key.split('%')[2]),
                             "Pagetype":key.split('%')[3],"tR-ave":linesum[key]/linecnt[key],"tR-max":linemax[key],
                             "pg_err-ave":lineerrsum[key]/linecnt[key],"pg_err-max":lineerrmax[key]})
    data=DataFrame(dict(readMap)).T
    data.sort_values(by=["Group","PE_cnt","page"],inplace=True)
    data['Group']=[groupInfo[int(i)] for i in data['Group']]
    data.to_csv(pathToMixedReadExcel)


# In[188]:



def fetchGroupInfo():
    with open(logPath,'r') as datain:
        line=datain.readline()
        while(line):
            findstr="Cycle group:"
            startidx=line.find(findstr)
            if(startidx>-1):
                result=line[startidx+len(findstr):]
                groupList=[i.strip() for i in result.split('-')]
                for i in range(len(groupList)):
                    cyclecnt=(int)(groupList[i])
                    cycletext=""
                    if(cyclecnt>=1000):
                        cycletext=(str)(cyclecnt/1000)+'k'
                    else:
                        cycletext=(str)(cyclecnt)
                    groupInfo[i]=cycletext
                break;
            line=datain.readline()
    print(groupInfo)
            


# In[189]:


if __name__=='__main__':
    if not os.path.exists(logName):
        os.mkdir(logName)
        os.mkdir(logName+'/'+excelDir)
        os.mkdir(logName+'/'+mixedExcelDir)
    fetchGroupInfo()#must execute first before any generate operation
    generateEraseExcel()
    generateProgramExcel()
    generateReadExcel()
    generateEccDistributionExcel()
    generateMixedEraseExcel()
    generateMixedProgramExcel()
    generateMixedReadExcel()

