from vnstock import *
import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, date
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
            1: "model_1.hdf5",
            2: "model_2.hdf5",
            3: "model_3.hdf5",
            4: "model_4.hdf5",
            5: "model_5.hdf5",
            6: "model_6.hdf5",
            7: "model_7.hdf5",
        }
        self.indicator = 100
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
        
    
    def InitModel(self, filepath):  
        self.model = load_model(filepath)
        
    def get_before_data(self,code):
        current_date = datetime.now().date()
        return stock_historical_data(code, date(2013,1,1).strftime('%Y-%m-%d'),str(current_date)).tail(60)
    
    def CT(self,a, b):
        return ((self.indicator+1)*b)-(self.indicator*a)
    
    def PredictwithCT(self,a):
        a = np.array(a)
        a = a.reshape(1,-1)[0]
        count = len(a)
        new_array = []
        new_array.append(a[0])
        for i in range(count):
            if i != count - 1:
                d = self.CT(a[i],a[i+1])
                new_array.append(d) 
        return new_array 


    def Predict(self, day, code):  
        scaler = MinMaxScaler(feature_range = (0,1))
        self.InitModel(self.predictDate[day])

        input_data = self.get_before_data(code)
        inputs = input_data[['close', 'volume']].to_numpy()
        inputs = inputs.reshape(-1,2)
        inputs = scaler.fit_transform(inputs)
        #
        X_test = []
        X_test.append(inputs)
        X_test = np.array(X_test)
        X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 2))
        predicted_stock_price = self.model.predict(X_test)
        future_data_predicted = []
        ###########
        for i in range(0, day):
            new_predicted_stock_price = predicted_stock_price[:,i].reshape(-1,1)
            new_predicted_stock_price = np.c_[new_predicted_stock_price, np.ones(1)]
            new_predicted_stock_price = scaler.inverse_transform(new_predicted_stock_price)
            future_data_predicted.append(new_predicted_stock_price[:,0])


        predict_to_draw = self.PredictwithCT(future_data_predicted)

        prices = []
        days = []
        for i in range(0,day):
            prices.append(future_data_predicted[i][0])
            if i == 0:
                days.append('Next day')
            else:
                days.append(f'Next {i+1} days')
            
        # df =  pd.DataFrame({"The next day":days, "Predict Price": prices, "Predict with Indicator": predict_to_draw})
        df =  pd.DataFrame({"The next day":days, "Predicted Price": predict_to_draw})
        return df