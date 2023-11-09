from vnstock import *
import numpy as np
class DataGenerate:
    def __init__(self):
        self.a = 1
    
    def getStockCode(self):
        return listing_companies()['ticker'].values
    def getDomain(self):
        return np.sort(listing_companies()['icbName'].unique())

    def getDatanalyst(self,val,todate):
       #vl = ["Phần mềm","Bất động sản"]
        df=listing_companies()
        checklist = []
        for i in val:
            checklist.append({f"{i}":df.query('icbName == @i')['ticker'].head(5).values})
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