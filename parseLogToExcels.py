
# coding: utf-8

# In[16]:


from __future__ import unicode_literals
import csv
import re
import os
import numpy as np
import pandas as pd

pathToLogDir='./logs/'
logName='retention_0' 
pathToLog=pathToLogDir+logName+'.log' 
#logname is the name of the directory of everytime's report
pathToEraseChart=logName+"/excels/erase.csv"
pathToProgramChart=logName+"/excels/program.csv"
pathToReadChart=logName+"/excels/read.csv"
pathToEccChart=logName+"/excels/ecc.csv"
pathToFrameEccCount=logName+"/excels/frameEccCount.csv"
pathToPecntFramecnt=logName+'/excels/PecntFramecnt.csv'

pattNandAddr=re.compile("nand addr (.*):(.*)")
pattEras=re.compile("Pe_cnt:(\d*).*erase_time_us:(\d*)")
pattProg=re.compile("PageIndex:(\d*).*prog_time:(\d*)")
pattRead=re.compile(".*page index :(\d*).*mismatch cnt:(\d*).*time_ll:(\d*)")
pattFrameEccCount=re.compile(".*page_index:\s+(\d+)\s+frame_ecc_count:\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+).*")
pattEcc=re.compile("^(\d+)$")
pattPecnt=re.compile("Pe_cnt:(\d*)")
def generateEraseExcel():
    with open(pathToEraseChart,'w',newline='') as csvfile:
        fieldnames=['u8PackageIdx','u8CEIdx','u8DieIdx','u8PlaneIdx','u16BlockIdx','Pe_cnt','erase_time_us']
        writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        with open(pathToLog,'r') as datain:
            line=datain.readline()
            while(line):
                result=pattNandAddr.match(line)
                if(result):
                    locals()[result.group(1)]=result.group(2)
                result=pattEras.match(line)
                if(result):
                    eraseline={}
                    for field in fieldnames:
                        if(field=='Pe_cnt'):
                            eraseline[field]=result.group(1)
                        elif(field=='erase_time_us'):
                            eraseline[field]=result.group(2)
                        else:
                            eraseline[field]=locals()[field]
                    writer.writerow(eraseline)
                line=datain.readline()

                
#remove program log text 5.21
def generateProgExcel():
    with open(pathToProgramChart,'w',newline='') as csvfile:
        fieldnames=['u8PackageIdx','u8CEIdx','u8DieIdx','u8PlaneIdx','u16BlockIdx','PageIndex','Pe_cnt','prog_time']
        writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        with open(pathToLog,'r') as datain:
            line=datain.readline()
            while(line):
                result=pattNandAddr.match(line)
                if(result):
                    locals()[result.group(1)]=result.group(2)

                result=pattEras.match(line)
                if(result):
                    locals()['Pe_cnt']=result.group(1)


                result=pattProg.match(line)
                if(result):
                    if(int(locals()['Pe_cnt']) % 100 == 0): #this is strange。i can't remember why %100
                        progline={}
                        for field in fieldnames:
                            if(field=='PageIndex'):
                                progline[field]=result.group(1)
                            elif (field=='prog_time'):
                                progline[field]=result.group(2)
                            else:
                                progline[field]=locals()[field]
                        writer.writerow(progline)
                line=datain.readline()

def generateReadExcel():
    with open(pathToReadChart,'w',newline='') as csvfile:
        fieldnames=['u8PackageIdx','u8CEIdx','u8DieIdx','u8PlaneIdx','u16BlockIdx','u16PageIdx','Pe_cnt','mismatchCnt','time_ll']
        writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        with open(pathToLog,'r') as datain:
            line=datain.readline()
            while(line):

                result=pattNandAddr.match(line)
                if(result):
                    locals()[result.group(1)]=result.group(2)

                result=pattEras.match(line)
                if(result):
                    locals()['Pe_cnt']=result.group(1)

                result=pattRead.match(line)
                if(result):
                    if(int(locals()['Pe_cnt']) % 100 == 0):
                        readline={}
                        for field in fieldnames:
                            if(field=='u16PageIdx'):
                                readline[field]=result.group(1)
                            elif(field=='mismatchCnt'):
                                readline[field]=result.group(2)
                            elif (field=='time_ll'):
                                readline[field]=result.group(3)
                            else:
                                readline[field]=locals()[field]
                        writer.writerow(readline)
                line=datain.readline()

def generateEccExcel():
    ECCMAX=1024  #this is not certain.should pay more attention to this arg
    with open(pathToEccChart,'w',newline='') as csvfile:
        fieldnames=['u8PackageIdx','u8CEIdx','u8DieIdx','u8PlaneIdx','u16BlockIdx','u16PageIdx','u4PageSequence']
        for i in range(ECCMAX):
            fieldnames.append('ECC'+str(i))
        writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()

        with open(pathToLog,'r') as datain:
            line=datain.readline()
            index=0  #mean the eccindex in the log file,till 1024,one row required
            eccline={}
            while(line):
                result=pattNandAddr.match(line)
                if(result):
                    locals()[result.group(1)]=result.group(2)
                result=pattEcc.match(line)
                if(result):
                    if(index==0): #mean its the initialization
                        for field in fieldnames:
                            if(field.find('ECC')>=0):
                                break
                            eccline[field]=locals()[field]
                    eccline['ECC'+str(index)]=result.group(1)
                    index=index+1
                    if(index==ECCMAX):
                        writer.writerow(eccline)
                        index=0
                        eccline={}
                line=datain.readline()

def generateFrameEccCountExcel():
    with open(pathToFrameEccCount,'w',newline='') as csvfile:
        fieldnames=['u8PackageIdx','u8CEIdx','u8DieIdx','u8PlaneIdx','u16BlockIdx','u16PageIdx','Pe_cnt']
        for i in range(16):
            fieldnames.append('Frame'+str(i)+'Ecc')
        writer=csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        with open(pathToLog,'r') as datain:
            line=datain.readline()
            while(line):
                result=pattNandAddr.match(line)
                if(result):
                    locals()[result.group(1)]=result.group(2)

                result=pattEras.match(line)
                if(result):
                    locals()['Pe_cnt']=result.group(1)

                result=pattFrameEccCount.match(line)
                if(result):
                    readline={}
                    for field in fieldnames:
                        index=field.find('Frame')
                        if(field=='u16PageIdx'):
                            readline[field]=result.group(1)
                        elif(field.find("Frame")>=0):
                            break;
                        else:
                            readline[field]=locals()[field]
#                     add the frame0-15ecc to the readline map,group(2)will be frame0ecc
                    for i in range(16):
                        readline['Frame'+str(i)+'Ecc']=result.group(i+2)
                    writer.writerow(readline)
                line=datain.readline()
                


# In[92]:




def generatePecntFramecntExcel():
    data={}  # key is pecnt,value is ecc distribution,ecc distribution's key is ecccnt,value is framecnt
    eccCount=0 # indicates ecccount
    locals()['Pecnt']=-1
    with open(pathToLog,'r') as datain:
        line=datain.readline()
        while(line):
            result=pattPecnt.match(line)
            if(result):
                if (locals()['Pecnt']!=result.group(1)):
                    locals()['Pecnt']=int(result.group(1))
                    data[locals()['Pecnt']]={}
                    eccCount=0
                
            result=pattEcc.match(line)
            if(result):
                data[locals()['Pecnt']][eccCount] =result.group(1)
                eccCount=eccCount+1
            
            line=datain.readline()
    data=pd.DataFrame(data)
    data=data.dropna(axis=1,how='all')
    data.to_csv(pathToPecntFramecnt)
    
if(__name__=='__main__'):
    if not os.path.exists(logName):
        os.mkdir(logName)
        os.mkdir(logName+'/excels')
#         os.mkdir(logName+'/charts') #no need,now,the charts are stored in main directory.
    generatePecntFramecntExcel()
    generateEraseExcel()
    
    generateReadExcel()
    generateFrameEccCountExcel()
    
#     generateEccExcel() translate to pecnt_ecccount excel  5.17
# generateProgExcel() remove the program log text 5.21

