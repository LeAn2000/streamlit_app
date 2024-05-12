import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.metrics import mean_squared_error, mean_absolute_error, mean_absolute_percentage_error

from vnstock import *
def CT(indicator, a, b):
        return ((indicator + 1) * b) - (indicator * a)

def PredictwithCT(indicator,a):
    a = np.array(a)
    a = a.reshape(1, -1)[0]
    count = len(a)
    new_array = []
    new_array.append(a[0])
    for i in range(count):
        if i != count - 1:
            d = CT(indicator,a[i], a[i + 1])
            new_array.append(d)
    return new_array

def PredictArima(day,code, days):
    from_date  = '2013-01-01'
    to_date    = datetime.now().strftime("%Y-%m-%d")   # get data to Today (Now)

    fpt3 = stock_historical_data(code,from_date,to_date).set_index('time')
    # Create a new dataframe with the 'close' and 'volume' columns
    new_dataset = fpt3.filter(['close', 'volume'])

    # Convert the dataframe to a numpy array
    new_dataset_processed = new_dataset.values

    # Create a differenced series for both 'close' and 'volume'
    def difference(dataset, interval=1):
        diff = list()
        for i in range(interval, len(dataset)):
            value = dataset[i] - dataset[i - interval]
            diff.append(value)
        return diff

    # Invert differenced value
    def inverse_difference(history, yhat, interval=1):
        return yhat + history[-interval]

    # Seasonal difference
    X = new_dataset_processed
    days_in_year = 365
    differenced_close  = difference(X[:, 0], days_in_year)
    differenced_volume = difference(X[:, 1], days_in_year)

    # Fit model for close price
    model_close = ARIMA(differenced_close, order=(1, 1, 1), exog=differenced_volume)
    model_fit_close = model_close.fit()

    # Forecast close price for 7 days ahead
    forecast_steps = day
    forecast_close = model_fit_close.forecast(steps=forecast_steps, exog=differenced_volume[-forecast_steps:])

    # Invert the differenced close forecast
    history_close = [x[0] for x in X]
    data_draw = []
    day = 1
    for yhat_close in forecast_close:
        inverted_close = inverse_difference(history_close, yhat_close, days_in_year)
        print(f'Next Day {day}: Predicted Close = {inverted_close:.3f}')
        history_close.append(inverted_close)
        data_draw.append(inverted_close)
        day += 1
    
    df = pd.DataFrame(
            {"The Next Day": days, "Predicted Price (VND)": PredictwithCT(1,data_draw)}
            #{"The Next Day": days, "Predicted Price (VND)": data_draw}
        )
    return df


