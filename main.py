import pandas as pd
from lxml import etree
import os
import html2text
import re
import numpy as np
import difflib


rootdir = r'C:\Users\chenmeng\Documents\FDDC_2\zengjianchi_test'
filelist = os.listdir(rootdir)
data = []
for i in range(len(filelist)):
    path = os.path.join(rootdir,filelist[i])
    f = open(path,'r',encoding='utf-8')
    text = f.read()
    f.close()
    fileid = int(filelist[i])
    try:
        result = parse_ZJC(text,fileid)
        if result:
            data.extend(result)
        else:
            pass
    except:
        pass
        
df = pd.DataFrame(data,columns=['id','股东全称','股东简称','变动截止日期','变动价格','变动数量','变动后持股数'])
