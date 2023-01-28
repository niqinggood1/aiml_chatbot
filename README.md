# aiml_chatbot是基于人工智能标记语言，基于知识库和规则做的聊天机器人系统  
chatbot 内部定义了聊天机器人的类  
test_chatbot 有两个函数test_interact创建聊天机器人，输入对话进行测试;test_transfer将语料转化为aiml格式数据  
目录aimlOutput：transferIntoAiml.py     输出文件夹，输出aiml文件  
目录dialoguesInput：transferIntoAiml.py 输入文件夹，存储原本的txt文档  

依赖的的aiml库,由于版本问题在python3.8中time.clock()中已经不支持，可以自己安装后修改或者参考  
