# -*- coding: utf-8 -*-
"""
Created on Tue Sep 05 15:19:34 2017
@author: Edward

This file is used to transfer the dialogues files in a folder into an aiml file
*Attention: Please make sure all of the files in the folder are encoded with UTF-8
*Attention: Please replace all of the "\" with "/" in the folder address

The orginal data should be in the format of:    
Pattern
Templates
\\n

Example:
下象棋
那当然，我可是个象棋高手.中国象棋和国际象棋都一流！
\\n

Three additional functions are provided:
transferIntoAiml.capitalPattern()
transferIntoAiml.replaceDirtyWords()
transferIntoAiml.modifyWrongData()

"""

import os
import sys
import types
import random

#print sys.getdefaultencoding()
def request_answer_to_aiml(patterns,templates,dest_file="aimlOutput.aiml"):
    '''
    Function to to print out the aiml file
    
    Receive two lists: patterns[] and templates[]
    and print it out to the dest_file in aiml format
    '''
    #Print into another txt file
    print( "---Printing Data---"   )
    theOutput = open(dest_file, "w+")   
    theOutput.write("<aiml version=\"1.0.1\" encoding=\"UTF-8\">\n\n")
    
    j=0
    while (j<len(patterns)-1):
        theOutput.write("\n\n\t<category>")
        theOutput.write("\n\t\t<pattern>"+patterns[j]+"</pattern>")
        theOutput.write("\n\t\t<template>")
        if (patterns[j]!=patterns[j+1]):  
            theOutput.write("\n\t\t\t"+templates[j])
            j=j+1
            if (j==len(patterns)):
                break
        else:#Dealing with multiple templates: Using <random />
            theOutput.write("\n\t\t\t<random>") 
            if (templates[j][-1]=="\n"):
                theOutput.write("\n\t\t\t\t<li>"+templates[j][:-1]+"</li>")
            else:
                theOutput.write("\n\t\t\t\t<li>"+templates[j][:]+"</li>")
            duplicate=1
            while (patterns[j]==patterns[j+duplicate]):             
                if (templates[j+duplicate][-1]=="\n"):
                    theOutput.write("\n\t\t\t\t<li>"+templates[j+duplicate][:-1]+"</li>")                 
                else:
                    theOutput.write("\n\t\t\t\t<li>"+templates[j+duplicate][:]+"</li>")
                duplicate=duplicate+1
                if (j+duplicate==len(patterns)):
                    break
            theOutput.write("\n\t\t\t</random>\n") 
            j=j+duplicate
            
        theOutput.write("\t\t</template>")
        theOutput.write("\n\t</category>")
      
    if (j!=len(patterns)):  #Seperated the last one cuz I wanted to use "patterns[j]!=patterns[j+1]" above in line 156
        theOutput.write("\n\n\t<category>")
        theOutput.write("\n\t\t<pattern>"+patterns[j]+"</pattern>")
        theOutput.write("\n\t\t<template>")
        theOutput.write("\n\t\t\t"+templates[j])
        theOutput.write("\t\t</template>")
        theOutput.write("\n\t</category>")
        
    theOutput.write("\n\n</aiml>")
        
    theOutput.close() 

def transAiml(dataSetDir='./dialoguesInput/',dest_file="./aimlOutput/aimlOutput.aiml"):
    '''
    Function to transfer the dialogues files in a folder into an aiml file
    *Attention: Please make sure all of the files in the folder are encoded with UTF-8
    *Attention: Please replace all of the "\" with "/" in the folder address
    '''
    #Getting set  
    print("\n------------Transfer the dialogues files into an aiml file----------------\n"  )
    print( "---Getting Data---"   )
    trainingFileList = os.listdir(dataSetDir)  
    numSamples = len(trainingFileList)   ; print('trainingFileList:',trainingFileList)
    reContent=[]
    for filename in trainingFileList:
        content=[]
        print( 'filename:',filename  )
        theInput = open(dataSetDir + filename,"r")  
        lines = theInput.readlines()  
        content+=lines
        theInput.close()    
        #Rewrite in '*** ||| ***' format
        j=0
        while (j < len(content)):
            tempContent=""
            if (content[j]!="\n"):
                #Patterns part
                if ("[cqname]" in content[j]):
                    content[j]=content[j].replace('[cqname]','你')
                if ("[name]" in content[j]):
                    content[j]=content[j].replace('[name]','我')    
                tempContent = tempContent + content[j].split("\n")[0] + "\t|||\t"
                j+=1
                #Templates part
                if ("[cqname]" in content[j]):
                    content[j]=content[j].replace('[cqname]','<get name="cqname"/>')
                    
                if ("[name]" in content[j]):
                    content[j]=content[j].replace('[name]','<get name="usrname"/>')
                tempContent = tempContent + content[j]
                j+=1  
                #Check whether there are multiple lines in templates part
                if (j < len(content)):
                    while (content[j]!="\n"):
                        if tempContent[-1]=="\n":   #To make sure every <li/> in the same row
                            tempContent=tempContent[:-1]
                        if ("[cqname]" in content[j]):
                            content[j]=content[j].replace('[cqname]','<get name="cqname"/>')
                        if ("[name]" in content[j]):
                            content[j]=content[j].replace('[name]','<get name="usrname"/>')
                        tempContent = tempContent + content[j]
                        j+=1 
                        if (j >= len(content)):
                            break
                reContent.append(tempContent)
            else:
                j+=1
    print('reContent:',reContent[:6])
    print( "---Handling Data---"  )
    reContent = list(set(reContent))    #Build an unordered collection of unique elements.
    reContent.sort()    #Sort
    while "" in reContent:  #Delete the empty data
        reContent.remove("")
        
    #Modify the wrong data
    reContent_new=[]
    for r_a in reContent:
        #[bq***]
        if "[bq" in r_a:   
            r_a=r_a.split("[")[0]+"(微笑)"+r_a.split("]")[1]   
        #illegal symbol
        if "\\r" in r_a:   
            r_a=r_a.replace('\\r','')
        if "<<" in r_a:
            r_a=r_a.replace('<<','《')
        if ">>" in r_a:
            r_a=r_a.replace('>>','》')  
        
        reContent_new.append(r_a)
    reContent=reContent_new
    print('reContent2:',len( reContent ), reContent[:6])
    #Split the contents into two lists
    patterns=[]
    templates=[]
    unRegularData=0
    for i_content in reContent: #for i in range(len(reContent)):

        if ("[\"face\"" in i_content.split("\t|||")[0] or ",[face\"" in i_content.split("\t|||")[0] or i_content.split("\t|||")[0]==""): #Ignore the meaningless data
            continue
        if  "|||" in i_content :
            arg_list=i_content.replace('\t','').split("|||")
            patterns.append(  arg_list[0]  )
            templates.append( arg_list[1] ) 
        else:
            unRegularData+=1

    print('len patterns:', len(patterns) )
    patterns_tmp=[]
    tempContent_tmp=[]
    for i in range( len(patterns) ):
        # try:
        # except:
        #     continue
        x=patterns[i]
        y=templates[i]

        patterns_tmp.append(x); tempContent_tmp.append(y)

    print(  'The amount of content without illegal symbol is:',len(tempContent_tmp)   )
    if len(tempContent_tmp)==0:
        print( "No entries. Please make sure all of the files in the folder are encoded with UTF-8")
    
    #Output
    request_answer_to_aiml(patterns_tmp[0:], tempContent_tmp[0:],dest_file)
    print ("---Finished---")


def coreValue():
    '''
    To generate one level of the core values
    '''
    return '学习社会主义核心价值观：'+ random.choice ( ['富强 民主 文明 和谐', '自由 平等 公正 法治', '爱国 敬业 诚信 友善'])

def capitalPattern(dataSetDir= './aimlOutput/' ):
    '''
    Function to capitalize the patterns for every file in a folder
    Need the location of a folder as the arguement
    *Attention: the orginal aiml files must be the files generated by the transferIntoAiml.py or transferIntoXml.py
    '''
    print("\n------------Capitalize the patterns for every file----------------\n")
    print( "---Getting Data---"   )
    trainingFileList = os.listdir(dataSetDir)  
    numSamples = len(trainingFileList)  
    
    for filename in trainingFileList:
        print( filename  )
        with open(dataSetDir + filename,"r") as f:
            lines = f.readlines()     
        with open(dataSetDir + filename,"w") as theFile:
            for line in lines:
                if "<pattern>" in line:
                    tmpLine=line.split("<pattern>")[1]
                    tmpLine=tmpLine.split("</pattern>")[0]
                    line="\t\t<pattern>"+tmpLine.upper()+"</pattern>\n"
                theFile.write(line) 
                
    print ("---Finished---")

def checkDirtyWords(line):
    '''
    To check the words and return the frequency of them in a line
    '''
    dirtyWords=['那根蒜','揍','你Y','傻','残废','说你','脑残','搞你','自身问题','睡你','脑袋','被夹','笨','吵你','呆','痿','你妹','插插','法克油',\
    '强奸','你才','老子','SB','不孝','玩死','祖宗','**','流氓','鄙视','犯贱','干掉','充气娃娃','你丫','吓哭','骂','大巫','操你','草你','尼玛','不懂事',\
    '二弟','回民','二师兄','有病','粪','不要脸','叫爸爸','儿子是你','射在','你爷爷','连你','讨厌','无赖','滚','你妈','他妈','你娘','你姐','操我','撞死',\
    '王八','千年兽','妈的','屁','JJ','鸡鸡','人妖','狼心','病猫','彼此','淫','别笑八两','切你','去你的','爆你菊','爆菊','老母','靠，','吃屎','撸管','A片','猪',\
    '大爷','哥说你','你打','德行','fuck','鬼子','色色','丫的','比你','jb','人品','武藤兰','av','gv','很二','S和B','一B','好二','恶心','好丑','2b','2B',\
    '垃圾','鼻屎','阴道','贱人','JB','搞基','衮','FUCK'] 
    dirtyCount=0
    for word in dirtyWords:
        if word in line:
            dirtyCount+=1
    return dirtyCount
                    
def replaceDirtyWords(dataSetDir= './aimlOutput/' ):
    '''
    Function to replace the dirty words in templates with the core values of Chinese socialism
    Need the address of folder as the arguement
    '''
    print("\n------------Replace the dirty words with the core values of Chinese socialism----------------\n" )
    print( "---Getting Data---"   )
    trainingFileList = os.listdir(dataSetDir)  
    numSamples = len(trainingFileList)  
    dirtyDetected=0
    for filename in trainingFileList:
        print( filename  )
        with open(dataSetDir + filename,"r") as f:
            lines = f.readlines()     
        with open(dataSetDir + filename,"w") as theFile:
            for line in lines:
                if "<category>" in line or "<pattern>" in line or \
                "<template>" in line or "</template>" in line or "</category>" in line or "aiml" in line: #Only check the template part
                    theFile.write(line)
                    continue
                else:
                    if checkDirtyWords(line)>0:     #Check dirty words
                        if "<li>" in line:                           
                            line="\t\t\t\t<li>"+ coreValue() +"</li>\n"
                        else:
                            line="\t\t\t"+ coreValue() +"\n"
                        dirtyDetected+=1
                    theFile.write(line)
    print ("---Finished---")
    print ("dirtyDetected:"+str(dirtyDetected))
      
def modifyWrongData(dataSetDir='./aimlOutput/'):
    '''
    This function is used to modify the wrong data in orginal txt file
    Specific to "dialogue" folder
    '''
    #Getting set  
    print("\n------------Modify the wrong data in orginal txt files----------------\n")
    print( "---Getting Data---"  )
    trainingFileList = os.listdir(dataSetDir)  
    numSamples = len(trainingFileList)
    for filename in trainingFileList:
        print( filename  )
    with open(dataSetDir + filename,"r") as f:
        lines = f.readlines()
    with open(dataSetDir + filename,"w") as theFile:

        for line in lines:
            if "\\(^o^)/" in line:
                line=line.replace('\\(^o^)/','')
            if '>_<' in line:
                line=line.replace('>_<','0_0')
            if "<:" in line:
                line=line.replace('<:','(:')
            if "(&)" in line:
                line=line.replace('(&)','苟')
            if "%%$^$^*(&(&(%&%&$" in line:
                line=line.replace('%%$^$^*(&(&(%&%&$','南无、喝啰怛那、哆啰夜耶，南无、阿唎耶，婆卢羯帝、烁钵啰耶，菩提萨埵婆耶')
            #Names and addresss
            if "酷玩" in line:
                line=line.replace('酷玩','小九')
            if "小爱" in line:
                line=line.replace('小爱','小九')
            if "bbs.kuwans.com" in line:
                line=line.replace('bbs.kuwans.com','http://www.guosen.com.cn')
            if "qqjqr.ayy111.com" in line:
                line=line.replace('qqjqr.ayy111.com','www.guosen.com.cn')
            if "青云" in line:
                line=line.replace('青云','小九')
            if "QQ285584" in line:
                line=line.replace('QQ285584','微博@国信证券泰然九路营业部')
            if "WWW.YunSafe.COM" in line:
                line=line.replace('WWW.YunSafe.COM','http://www.guosen.com.cn')
            if "yunsafe.com" in line:
                line=line.replace('yunsafe.com','guosen.com.cn')
            if "t.qq.com/fhcmail" in line:
                line=line.replace('t.qq.com/fhcmail','http://weibo.com/tjnc?refer_flag=1001030102')
            if "http://bbs.kuwans.com/thread-23136-1-1.html" in line:
                line=line.replace('http://bbs.kuwans.com/thread-23136-1-1.html','')
            if "www.lichengyang.com" in line:
                line=line.replace('www.lichengyang.com','http://www.guosen.com.cn/')
            if "树离" in line:
                line=line.replace('树离','小九')
            if "kuwans.com" in line:
                line=line.replace('kuwans.com','http://www.guosen.com.cn/')
            if "fhcmail@qq.com" in line:
                line=line.replace('fhcmail@qq.com','。。。你自己猜啊')
            if "【YunSafe.COM】" in line:
                line=line.replace('【YunSafe.COM】','http://www.guosen.com.cn/')
            if "734482228@qq.com" in line:
                line=line.replace('734482228@qq.com','...不告诉你')
            if "http://q.coxxs.com" in line:
                line=line.replace('http://q.coxxs.com','http://www.guosen.com.cn/')
            if "酷Q" in line:
                line=line.replace('酷Q','小九')
            if "VV团队" in line:
                line=line.replace('VV团队','小九')
            if "酷Q" in line:
                line=line.replace('酷Q','小九')
            if "weibo.com/shuaiman8" in line:
                line=line.replace('weibo.com/shuaiman8','http://weibo.com/tjnc?refer_flag=1001030102')
            if "http://yunsafe.com/thread-531-1-1.html" in line:
                line=line.replace('http://yunsafe.com/thread-531-1-1.html','http://www.guosen.com.cn/')
            if "和帅男社区bbs.shuaiman.net" in line:
                line=line.replace('和帅男社区bbs.shuaiman.net','')
            if "qq机器人" in line:
                line=line.replace('qq机器人','小九机器人')
            if "rom团队" in line:
                line=line.replace('rom团队','')
            if "vv rom" in line:
                line=line.replace('vv rom','')
            if "qq机器人" in line:
                line=line.replace('qq机器人','小九机器人')
            if "QQ908816490" in line:
                line=line.replace('QQ908816490','')
            if "http://lightds.com" in line:
                line=line.replace('http://lightds.com','http://www.guosen.com.cn/')
            if "www.tcxj.net" in line:
                line=line.replace('www.tcxj.net','http://www.guosen.com.cn/')
            if "332343176@qq.com" in line:
                line=line.replace('332343176@qq.com','http://www.guosen.com.cn/')
            if "www.xpsec.com" in line:
                line=line.replace('www.xpsec.com','www.guosen.com.cn/')
            if "小P" in line:
                line=line.replace('小P','小九')
            if "www.atimg.com" in line:
                line=line.replace('www.atimg.com','http://www.guosen.com.cn/')
            if "xmxy0@live.com" in line:
                line=line.replace('xmxy0@live.com','19007@guosen.com.cn')
            theFile.write(line)
    print ("---Finished---")

def test():
    return

if __name__ == '__main__':
    test()