from lxml import etree
class TableParser:
    def __init__(self):
        self.rows = 0
        self.columns = 0
        self.tablehead = ''
        self.table = []
        self.tabletype = 0
        
    def parse(self,tbody):
        r = tbody.xpath('tr')
        self.rows = len(r)
        c = [len(r[i].xpath('td')) for i in range(self.rows)]
        self.columns = max(c)
        table = np.empty((self.rows,self.columns),dtype='<U100')
        
        for i in range(self.rows):
            c = r[i].xpath('td')
            for j in range(len(c)):
                rowspan = c[j].xpath('@rowspan')
                colspan = c[j].xpath('@colspan')
                text = ''.join(c[j].xpath('text()'))
                t = self.clean(text)
                
                if (not rowspan and not colspan):
                    for k in range(self.columns):
                        if not table[i][k]:
                            table[i][k] = t
                            break
                if rowspan:
                    span = int(rowspan[0])
                    for k in range(self.columns):
                        if not table[i][k]:
                            for m in range(span):
                                table[i+m][k] = t
                            break
                if colspan:
                    span = int(colspan[0])
                    count = 0
                    for k in range(self.columns):
                        if not table[i][k]:
                            table[i][k] = t
                            count += 1
                            if count == span:
                                break
        self.table = table
    
    def get_tablehead(self,tbody):
        s = tbody.xpath('tr[1]/td//text()')
        s = ''.join(s)
        s = self.clean(s)
        self.tablehead = s
        return s
    
    def clean(self,s):
        s = s.replace('\n','')
        s = s.replace(' ','')
        return s
