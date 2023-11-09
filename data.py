from vnstock import *
import numpy as np
import pandas as pd
class DataGenerate:
    def __init__(self):
        self.data = pd.read_csv("title.csv")
        self.domain = {'Steel & Manufacturing ': ['Tài nguyên Cơ bản'],
                        'Transportation': ['Du lịch và Giải trí','Hàng & Dịch vụ Công nghiệp'],
                        'Technology & Retail Trade': ['Bán lẻ','Công nghệ Thông tin',],
                        'Bank': ['Ngân hàng'],
                        'Construction and Real Estate': ['Xây dựng và Vật liệu','Bất động sản'],
                         }
    def getStockCode(self):    
        return self.data['ticker'].values
    def getDomain(self):
        return self.domain.keys()

    def getDatanalyst(self,val,todate):
       #vl = ["Phần mềm","Bất động sản"]
        
        #val = [self.domain[_] for _ in val]
        
        checklist = []
        for i in val:
            check = self.domain[i]
            checklist.append({f"{i}":self.data.query('industry == @check')['ticker'].values})
        #to_date = datetime.datetime.now().strftime('%Y-%m-%d')
        #from_date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
      
        todate = str(todate)
        frames = pd.DataFrame()
        for _ in checklist:
            for __ in _.keys(): 
                a = pd.DataFrame({'_':[__], "time":[""],"open":[""],"high":[""],"low":[""],"close":[""],"volume":[""],"ticker":[""]})
                frames = pd.concat([frames,a], axis=0)
                for a in _[__]:
                    frame = stock_historical_data(a,todate,todate)
                    frame.insert(loc=0, column='_', value="")
                    #frame.insert(loc=1, column="check", value=f"st.button({frame.ticker.values[0]})")
                    frames = pd.concat([frames,frame], axis=0)



        return frames