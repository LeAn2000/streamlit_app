from vnstock import *
import numpy as np
import pandas as pd
from keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime, date


class ModelPredict:
    # predictDate: 1,2,3,4,5,6,7
    # data as a List prices: [91000,92000,93000]
    def __init__(self, predictDate, data):
        self.predictDate = predictDate
        self.data = data

    def to_dict(self):
        return {str(self.predictDate): self.data}


class PredictStockPrice:
    def __init__(self, code):
        self.code = code
        self.model = None
        self.modelPath = {
            1: "model_1.hdf5",
            2: "model_2.hdf5",
            3: "model_3.hdf5",
            4: "model_4.hdf5",
            5: "model_5.hdf5",
            6: "model_6.hdf5",
            7: "model_7.hdf5",
        }
        self.indicator = 100

    def initModel(self, predictDate):
        self.model = load_model(self.modelPath[predictDate])

    def get_before_data(self):
        current_date = datetime.now().date()
        return stock_historical_data(
            self.code, date(2013, 1, 1).strftime("%Y-%m-%d"), str(current_date)
        ).tail(60)

    def CT(self, a, b):
        return ((self.indicator + 1) * b) - (self.indicator * a)

    def PredictwithCT(self, a):
        a = np.array(a)
        a = a.reshape(1, -1)[0]
        count = len(a)
        new_array = []
        new_array.append(a[0])
        for i in range(count):
            if i != count - 1:
                d = self.CT(a[i], a[i + 1])
                new_array.append(d)
        return new_array

    def Predict(self, day):
        scaler = MinMaxScaler(feature_range=(0, 1))
        self.initModel(day)
        input_data = self.get_before_data()
        inputs = input_data[["close", "volume"]].to_numpy()
        inputs = inputs.reshape(-1, 2)
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
            new_predicted_stock_price = predicted_stock_price[:, i].reshape(-1, 1)
            new_predicted_stock_price = np.c_[new_predicted_stock_price, np.ones(1)]
            new_predicted_stock_price = scaler.inverse_transform(
                new_predicted_stock_price
            )
            future_data_predicted.append(new_predicted_stock_price[:, 0])

        return self.PredictwithCT(future_data_predicted)
