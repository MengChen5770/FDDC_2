def parse_ZJC(text,fileid):
    #text is the original string
    html = etree.HTML(text)
    t = pre_process(text)
    tbody_list = html.xpath('//tbody')
    result = []
    if tbody_list:
        for tbody in tbody_list:
            th = tp.get_tablehead(tbody)
            if match_tablehead(th,ZJC_T1,0.7):
                tp.parse(tbody)
                t1 = tp.table
                if tp.rows > 1:
                    for i in range(1,tp.rows):
                        if not ('合计' in t1[i]):
                            dataline = ['']*7
                            dataline[0] = fileid
                            if is_orgname(t1[i][0]):
                                dataline[1] = t1[i][0]
                            dataline[2] = ShortOrgMatch(RE_ZJC_SHORT_ORG,t)
                            dataline[3] = DateMatch(RE_DATE,t1[i][2])
                            dataline[4] = PriceMatch(RE_NUMBER,t1[i][3])
                            if ('万' in t1[0][4]) or ('万' in t1[i][4]):
                                multiplier = 10000
                            else:
                                multiplier = 1
                            dataline[5] = AmountMatch(RE_NUMBER,t1[i][4])*multiplier
                            result.append(dataline)
                    break
                else:
                    continue
            else:
                continue
        '''            
        for tbody in tbody_list:
            th = tp.get_tablehead(tbody)
            if match_tablehead(th,ZJC_T2,0.7):
                tp.parse(tbody)
                t2 = tp.table
                
                break
        '''
        return result
    else:
        pass
        #用正则提取，还没搞定
        
def pre_process(text):
    text_maker = html2text.HTML2Text()
    text_maker.ignore_tables = True
    t = text_maker.handle(text)
    t = t.replace('\n','')
    t = t.replace(' ','')
    t = t.replace('(','（')
    t = t.replace(')','）')
    return t

def string_similar(s1,s2):
    matcher = difflib.SequenceMatcher(None,s1,s2)
    return matcher.ratio()

def match_tablehead(th,s_list,threshold):
    ratio_list = [string_similar(th,s) for s in s_list]
    if max(ratio_list) > threshold:
        return 1
    else:
        return 0
    
def is_orgname(s):
    #判断为公司全称还是简称，还没搞定
    return 1

def AmountMatch(pattern,text):
    matchlist = pattern.findall(text)
    if len(matchlist) == 0:
        return ""
    else:
        m = ''.join(matchlist)
        return float(m)

def PriceMatch(pattern,text):
    matchlist = pattern.findall(text)
    if len(matchlist) == 0:
        return ""
    elif len(matchlist) == 1:
        return float(matchlist[0])
    else:
        m = [float(x) for x in matchlist]
        return np.mean(m)
    
def DateMatch(patternlist,text):
    matchlist = []
    for pattern in patternlist:
        matchlist.extend(pattern.findall(text))
    if len(matchlist) == 0:
        return ""
    else:
        return matchlist[-1]
    
def OrgMatch(patternlist,text):
    matchlist = []
    for pattern in patternlist:
        matchlist.extend(pattern.findall(text))
    if len(matchlist) == 0:
        return ""
    Cpattern = re.compile(r'[^：“”:"——]+')
    matchlist = [Cpattern.findall(x)[0] for x in matchlist]
    
    if len(matchlist) >= 1:
        return matchlist[0]

def ShortOrgMatch(patternlist,text):
    matchlist = []
    for pattern in patternlist:
        matchlist.extend(pattern.findall(text))
    if len(matchlist) == 0:
        return ""
    Cpattern = re.compile(r'[^：“”:"——]+')
    matchlist = [Cpattern.findall(x)[0] for x in matchlist]
    if len(matchlist) == 1:
        return matchlist[0]
    if len(matchlist) > 1:
        #
        return matchlist[-1]
