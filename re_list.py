import re
#去符号
RE_DE_SYMBOL = re.compile(r'[^：“”:"——]+')

#增减持公司全称
RE_ZJC_ORG = [re.compile(x) for x in 
              [r'接到.*?股东(.+?)（',
               r'收到.*?股东(.+?)（']]
               
#增减持公司简称
RE_ZJC_SHORT_ORG = re.compile(r'（.*?简称(.+?)）')

#日期
RE_DATE = [re.compile(x) for x in 
           [r'([0-9]+年[0-9]+月[0-9]+日)',
            r'([0-9]+\.[0-9]+\.[0-9]+)']]
