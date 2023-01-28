# -*- coding: utf-8 -*-

#This is a simple test for transferIntoAiml.py and aiml_02.py
import sys

def test_transfer():
    import transferIntoAiml
    print ("--This is a simple test for transferIntoAiml.py--")
    transferIntoAiml.transAiml(dataSetDir='./dialoguesInput/',dest_file="./aimlOutput/aimlOutput.aiml")
    transferIntoAiml.modifyWrongData(dataSetDir='./aimlOutput/')
    transferIntoAiml.capitalPattern(dataSetDir='./aimlOutput/')
    transferIntoAiml.replaceDirtyWords(dataSetDir='./aimlOutput/')
    return


def test_interact(  ):
    from chatbot import  aimlchat
    import os
    mychatbot   = aimlchat(dest_dir="./saved_model/",reloadBrain=False,name='Aria' )
    # mychatbot.aimlInitialize(reloadBrain=False,name='Aria' )
    mychatbot.aimlUserName('霍元甲')
    testStr="你好","你叫什么","骗线","S股",'*ST股票','B股转出','IPO','一级市场','不能申购新股','个人所得税','人工','修改资料','分红扣税失败','密码重置',"你好"
    for word in testStr:
        print('Your input: '+ word)
        print( 'chatbot:',mychatbot.aimlResponse(word)  )

    for i in range(10):
        message =  input('input:')
        print( 'chatbot:',mychatbot.aimlResponse(message)  )

if __name__ == '__main__':
    test_transfer()
    test_interact(  )










#import thulac #THU Lexical Analyzer for Chinese  Used to split the sentence into words   http://thulac.thunlp.org/
#thu1 = thulac.thulac(seg_only=True)