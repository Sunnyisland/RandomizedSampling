#Written by May McIntosh (Van Do0 on 17 Apr 2015
def ReadWellLayout():
        #Read Layout of wells
        #       B        C       D       E
        #1.    'Worst' 'Bad'  'Good'    0
        #2.     'Good'   0    'Bad'    'Bad'
        #3.    'Worst'   'Bad'  0     0
        
        filename = askopenfilename()
        #print filename
        Data=csv.reader(open(filename))
        #Data=csv.reader(open('WellLayoutRealTest.csv'))
        global ColName, RowName,Wlayout
        FirstLine=Data.next()
        #print FirstLine
        ColName=FirstLine[1:] #Colum name is the first row except the first column
        #print ColName
        Wlayout.append(FirstLine)
        for row in Data:
                RowName.append(row[0])
                Wlayout.append(row[0:])
        #print(Wlayout)#,'\n',RowName,"\n",ColName)
        #print ColName
        
def ReadDistDrug():
        #Read Distribution of Drug
        #       DrugA   DrugB   DrugC
        #Worst     2      2      1
        #Bad       1      1      2
        #Good      1      2      3
        filenameDist = askopenfilename()
        DistData=csv.reader(open(filenameDist))#Read Distributaion of drugs in
        #DistData=csv.reader(open('DrugDistRealTest.csv'))#Read Distributaion of drugs in
        global Drug
        Drug=()
        Drug=tuple(DistData.next()[1:])#Make drug name tuple Drug=['DrugA','DrugB','DrugC'...]
        global DictCon
        DictCon={} #Make a dictionary with key is the condition of CMW (Good, Bad, Average)
                 #Values are drugs tested i.e. {Good}: DrugA,DrugA,DrugB,DrugC
        for condlist in DistData: #For each condition of CMW (Good,Bad,Average
                condition=condlist[0] #First element is name of condition
                
                condlist=[int(x) for x in condlist[1:]]
                #print(condlist)
                templist=[]#Temporary list hold the drugs for each condition/values of keys
                for i in range(0,len(condlist)):# For each of element in the list [1 2 3], the first element is condition name
                        for j in range(0,condlist[i]):
                               templist.append(Drug[i])
               #print(templist)
                DictCon[condition]=templist
                #print DictCon
                


def CreateNewLayout():
        global DictDrug
        DictDrug ={}#{'DrugA':['B1','C2','D8','DrugB':['B6','D9']}
        norow=len(Wlayout)#number of lists in Wlaout is row number
        for row in range(1,norow):
                nocol=len(Wlayout[1])#number of element in each list is col number
                for col in range(1,nocol):
                        condition=Wlayout[row][col]
                        if condition in DictCon.keys():#If the value in a well is not one of the conditions 'G','Bad','Worse', ignore
                                TempDrugList=DictCon[Wlayout[row][col]]
                                ChosenDrug=ChooseADrug(row,col,nocol,TempDrugList)#Choose a Drug
                                NewLayout[row][col]=ChosenDrug #Add the chosen drug to New Well Layout
                                TempDrugList.remove(ChosenDrug) #Remove the chosen drug from the list of drugs to be choosen from
                                wellposition=WellPosition(row, col) #Find out the position of the well of chosen drug given row and column
                                ListWellPositionDrug(ChosenDrug,wellposition) #Populate the dictionary contain list wells for each drug
                        

def WellPosition(row, col): #Return well position given row, column, RowName and ColName
        #print('row is ', row, 'colum is ', col)
        return str(RowName[row-1])+str(ColName[col-1])

def ListWellPositionDrug(ChosenDrug, wellposition): #Populate a dictionary of keys as drug names, and values as corresponding wells
        if ChosenDrug not in DictDrug.keys():
                DictDrug[ChosenDrug]=[wellposition]
        else:
                DictDrug[ChosenDrug].append(wellposition)

                                
def ChooseADrug(row,col,nocol,DrugList):#Choose a drug from DrugList given row, col. Need to try to avoid drugs chosen for neighbouring wells
        #print row, col
        global tempAvoidList, PossibleDrugs
        tempAvoidList=set()#Look around an find a list of nearby drugs
        if NewLayout[row][col] in DictCon.keys():
                if row>1 and col>1 and col!=nocol-1:
                        # print(col,nocol,row)
                        tempAvoidList.update([NewLayout[row-1][col-1],NewLayout[row-1][col],NewLayout[row-1][col+1],NewLayout[row][col-1]])
                        #print('[NewLayout[row][col-1]]', [NewLayout[row][col-1]])
                        #print('tempAvoidList',tempAvoidList)
                if row==1 and col >1:
                        tempAvoidList.update([NewLayout[row][col-1]])
                if row>1 and col==1:
                        tempAvoidList.update([NewLayout[row-1][col],NewLayout[row-1][col+1]])
                if row>1 and col==nocol-1:
                        tempAvoidList.update([NewLayout[row-1][col-1],NewLayout[row-1][col],NewLayout[row][col-1]])
                PossibleDrugs=[x for x in DrugList if x not in tempAvoidList] #Possible Drugs to consider is from druglist minus list to avoid
                #print('PossibleDrugs',PossibleDrugs)
                #print('tempAvoidList',tempAvoidList)
                #print('DrugList',DrugList)
                if PossibleDrugs:
                        ChosenDrug=random.choice(PossibleDrugs)
                else:
                        ChosenDrug=random.choice(DrugList)
                #print('ChosenDrug',ChosenDrug)
                return ChosenDrug
        return 0

import os
import random
import csv

global Data, Wlayout, RowName, ColName, NewLayout
Wlayout=[]
RowName=[]
ColName=[]

#Ask for directory for home folder
import Tkinter, tkFileDialog
root=Tkinter.Tk()
dirname=tkFileDialog.askdirectory(parent=root, initialdir="/",title="Please select your folder")
os.chdir(dirname)
#os.chdir("C:/Users/mmcintosh/Desktop/RandDrug/Python")

#Read in WellLayout RealTest
from tkFileDialog import askopenfilename
ReadWellLayout()

#Read in Drug Distribution 
ReadDistDrug()
#DrugList=['A', 'A', 'B', 'B', 'C', 'C', 'I', 'I', 'L', 'L', 'D', 'W', 'E', 'E','A', 'A', 'B', 'B', 'C', 'C', 'I', 'I', 'L', 'L', 'D', 'W', 'E', 'E','A', 'A', 'B', 'B', 'C', 'C', 'I', 'I', 'L', 'L', 'D', 'W', 'E', 'E']
#DrugList=DictCon{'Worst'}


#print Wlayout
NewLayout=list(Wlayout) #Clone a copy of the Well layout
#print('NewLayout')
#print(NewLayout)

#print ColName
CreateNewLayout()
#print NewLayout

with open("RandomizedLayout.csv","wb") as f:
        writer=csv.writer(f)
        writer.writerows(NewLayout)
        
        
        writer.writerow('\n')
        for key, value in DictDrug.items():
                writer.writerow([key])
                writer.writerows([value])
