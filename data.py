from vnstock import *
import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
class DataGenerate:
    def __init__(self):
        self.data = pd.read_csv("title.csv")
        self.domain = {'Steel & Manufacturing ': ['Tài nguyên Cơ bản'],
                        'Transportation': ['Du lịch và Giải trí','Hàng & Dịch vụ Công nghiệp'],
                        'Technology & Retail Trade': ['Bán lẻ','Công nghệ Thông tin',],
                        'Bank': ['Ngân hàng'],
                        'Construction and Real Estate': ['Xây dựng và Vật liệu','Bất động sản'],
                         }
        self.model = None
        self.predictDate = {
            1: "my_modelcheckpoint.hdf5"
        }
    def getStockCode(self):    
        return np.sort(self.data['ticker'].values)
    def getDomain(self):
        
        return sorted(self.domain.keys())
    
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
                    frame['open'] = frame['open'].map("{:,}".format)
                    frame['high'] = frame['high'].map("{:,}".format)
                    frame['low'] = frame['low'].map("{:,}".format)
                    frame['close'] = frame['close'].map("{:,}".format)
                    frame['volume'] = frame['volume'].map("{:,}".format)
                    frame.insert(loc=0, column='_', value="")
                    #frame.insert(loc=1, column="check", value=f"st.button({frame.ticker.values[0]})")
                    frames = pd.concat([frames,frame], axis=0)



        return frames
    
    def getdateOverview(self,code, fromdate, todate):
        if code != None:
            df = stock_historical_data(code,fromdate,todate,"1D", "stock")
            return df
        
    
    def get_previous_business_day(self,current_date, days):
        for _ in range(days):
            current_date -= timedelta(days=1)
            # Skip Saturday (5) and Sunday (6)
            while current_date.weekday() in {5, 6}:
                current_date -= timedelta(days=1)
        return current_date
    
    def InitModel(self, filepath):  
        self.model = load_model(filepath)
        
    def get_before_data(self,code):
        current_date = datetime.now().date()
        # Get the date 60 business days before the current date
        previous_date = self.get_previous_business_day(current_date, 61)
        return stock_historical_data(code,str(previous_date),str(current_date))
    

    def Predict(self, day, code):  
        scaler = MinMaxScaler(feature_range = (0,1))
        self.InitModel(self.predictDate[day])
        print(self.model)
        input_data = self.get_before_data(code)
        inputs = input_data['close'].to_numpy()
        inputs = inputs.reshape(-1,1)
        inputs = scaler.fit_transform(inputs)
        X_test = []
        X_test.append(inputs)
        X_test = np.array(X_test)
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        predicted_stock_price = self.model.predict(X_test)
        predicted_stock_price = scaler.inverse_transform(predicted_stock_price)
        prices = []
        days = []
        for i in range(0,day):
            prices.append(predicted_stock_price[i][0])
            if i == 0:
                days.append('In the next day')
            else:
                days.append(f'In the next {i+1} days')
            
        df =  pd.DataFrame({"The next day":days, "Predict Price": prices})
       
        return df