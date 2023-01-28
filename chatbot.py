# -*- coding: utf-8 -*-
"""
Edward
7/9/2017

Three functions are defined:
aimlInitialize(reloadBrain=0)
aimlUserName(userName)
aimlResponse(message)

"""

import aiml
import os
import sys, locale
import jieba
from jieba import analyse

class aimlchat(object):
    def __init__(self, dest_dir='./saved_model/',xml_path='aiml',reloadBrain=0,name='小小'):
        self.dest_dir = dest_dir
        self.kernel   = aiml.Kernel()
        self.xml_path = xml_path

        self.kernel.setPredicate('cqname', name)
        self.load_save()

    def load_save(self,reloadBrain=0):
        '''
        Function to initialize and try to load the brain file.
        Remember to call this function before using other functions
        If the "reloadBrain" variable not equals to zero or there is no brain file in the root directory,
        it will learn the aiml files according to "./aiml/std-startup.xml"
        '''
        #Check the Brain file
        if (reloadBrain==True and os.path.isfile(self.dest_dir+"aiml_brain.brn")):
            self.kernel.bootstrap(brainFile = self.dest_dir+"aiml_brain.brn")
        else:
            listdirs = os.listdir("./aiml");              print('listdirs:',listdirs)
            for f in listdirs:
                print(':',f)
                if f[-4:] in ['.xml','aiml'] :
                    print('load ',f )
                    #self.kernel.bootstrap( learnFiles = "./aiml/std-startup.xml", commands = "load aiml b")
                    self.kernel.bootstrap(learnFiles="./aiml/%s"%f, commands="load aiml %s"%f)


        self.kernel.saveBrain( self.dest_dir+"aiml_brain.brn" )
        #print( self.kernel.respond("你叫 %s"%name)  )

    def aimlUserName(self,userName,sessionId='1234'):
        '''
        Function to set the user's name.
        It would be better to call this function before using the "aimlResponse" function
        Actually the other functions can still works well without setting user's name,
        but it would leave the "usrname" variable blank result in some responses a little bit strange.
        '''
        print(  self.kernel.respond("我叫 "+userName)  )

    def aimlResponse( self,message,dest_dir='./',sessionId='1234' ):
        '''
        Function to get the aiml response
        the argument should be coded in utf-8
        '''
        if message == "saveaimlbrain":
            self.kernel.saveBrain(dest_dir+"aiml_brain.brn")
        else:

            sessionData = self.kernel.getSessionData(sessionId)

            bot_response = self.kernel.respond(message)
            if bot_response!='unknown':
                return bot_response
            else:
                return None
                #If the message is not matched, use Jieba to get 3 keywords and try these three keywords
                #findKey=0
                #if len(message.decode('utf8'))>2:    #It is meaningless to get the keywords from a two-character word
                    #keywords=jieba.analyse.extract_tags(message,3)
                    #for key in keywords:
                        #key_response= kernel.respond(key).decode( 'utf8' )
                        #if key_response!='unknown':
                            #findKey=1
                            #break
                #if findKey!=0:
                    #return key_response
                #else:
                    #return ('未检测到结果').decode( 'utf8' )
                
                
                
                
                
                
            
            
    

