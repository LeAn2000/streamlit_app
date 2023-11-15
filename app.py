import streamlit as st
from data import *
from streamlit.components.v1 import html
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta 
import plotly.express as px
from vnstock import * #import all functions, including functions that provide OHLC data for charting
from vnstock.chart import * 
import matplotlib.pyplot as plt
def custommarkdown(field_name):
    return f'<p class="tablefield">{field_name}<p>'

def toggle_expand(code):
    st.session_state.code = code 


def get_previous_weekday():
    current_date = datetime.now().date()
    # Subtract one day from the current date
    previous_date = current_date - timedelta(days=1)

    # Check if the resulting date is a Saturday (5) or Sunday (6)
    while previous_date.weekday() in {5, 6}:
        previous_date -= timedelta(days=1)

    return previous_date


def draw(dataset):
    plt.figure(figsize=(10,6))
    plt.title(f'Stock Price Trending Prediction')
    plt.xlabel('Trading Date')
    plt.ylabel('Closing Price (VND)')
    plt.plot(dataset['close'])
    plt.plot(dataset['predict'],color='red')
    plt.grid(which="major", color='k', linestyle='-.', linewidth=0.5)
    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(['{:,.0f}'.format(x) for x in current_values])
    return plt

if __name__ == "__main__":
    data = DataGenerate()
    st.set_page_config(page_title="Stock Prediction", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
    if "predict" not in st.session_state:
        st.session_state.predict = False
    if "code" not in st.session_state:
        st.session_state.code = "FPT"
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["Sector & Industry","Overview & Predict"])
    with tab1:
        domain_multi_selectbox = st.multiselect(
        "Choose your domain name to analyst data",
        data.getDomain(),
        default = 'Technology & Retail Trade',
        placeholder="Select your domain name ...",
        max_selections = 5
        )
        d = st.date_input("Choose trading date", value=get_previous_weekday())

        colms = st.columns((1, 1, 1, 1, 1,1,1,1))
        fields = ["Domain","Ticker","Time","Open","High","Low","Close","Volume"]
        for col, field_name in zip(colms, fields):
            if field_name != "Ticker" and field_name != 'Domain':
                col.markdown(f"<p class='header bold'>{field_name}</p>",unsafe_allow_html=True)
            else:
                col.markdown(f"<p class='bold'>{field_name}</p>",unsafe_allow_html=True)
        st.markdown("""<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True)
        df = data.getDatanalyst(domain_multi_selectbox, d).to_dict("records")
        for i in df:
            col1, col2, col3, col4, col5, col6, col7, col8 = st.columns((1,1, 1, 1, 1, 1, 1, 1))
            col1.write(i["_"])
            col3.markdown(custommarkdown(i["time"]),unsafe_allow_html=True)
            col4.markdown(custommarkdown(i["open"]),unsafe_allow_html=True)
            col5.markdown(custommarkdown(i["high"]),unsafe_allow_html=True)
            col6.markdown(custommarkdown(i["low"]),unsafe_allow_html=True)
            col7.markdown(custommarkdown(i["close"]),unsafe_allow_html=True)
            col8.markdown(custommarkdown(i["volume"]),unsafe_allow_html=True)
            if i["ticker"] != "":
                if col2.button(i['ticker'],use_container_width=True):
                    st.session_state.code = i['ticker']
                    
    with tab2:
        with st.expander("Overview", True):
            with st.form("form"):
                filterr = list(data.getStockCode())
                col1,col2,col3= st.columns([0.3,1,1])
                col1.write("Input Stock Code:")
                add_selectbox = col2.selectbox(
                "a",   
                filterr,
                index=filterr.index(st.session_state.code),
                placeholder="Select your Stock Code...",
            )
                
                submitted = col3.form_submit_button("Search")
                if submitted:
                    st.session_state.code = add_selectbox
            # st.markdown('<p class="hihead">View Stock Closing Price based on Historical Data</p>',unsafe_allow_html=True)
            col1,col2,col3,col4,col5,col6,col7 = st.columns(7)
            spacetime = relativedelta(months=12)
            todate = datetime.today()
            fromdate = todate - spacetime
            radio = st.radio(
                "Choose Trading Time 👇",
                ["1 Week", "1 Month", "3 Months","6 Months", "9 Months", "12 Months", "All Time"],
                horizontal=True,
                index = 5
            )
            if radio == "1 Week":
                    spacetime = relativedelta(days=7)
                    fromdate = todate - spacetime
                    
            if radio == "1 Month":
                    spacetime = relativedelta(months=1)
                    fromdate = todate - spacetime
                    
            if radio == "3 Months":
                    spacetime = relativedelta(months=3)
                    fromdate = todate - spacetime
                
            if radio == "6 Months":
                    spacetime = relativedelta(months=6)
                    fromdate = todate - spacetime
                
            if radio == "9 Months":
                    spacetime = relativedelta(months=9)
                    fromdate = todate - spacetime
                
            if radio == "12 Months":
                    spacetime = relativedelta(months=12)
                    fromdate = todate - spacetime
            if radio == "All Time":
                    fromdate  = date(2013,1,1)
            fromdate = fromdate.strftime('%Y-%m-%d')
            todate = todate.strftime('%Y-%m-%d')
            if st.session_state.code != None:
                chart_data = data.getdateOverview(st.session_state.code, fromdate, todate)
                fig = candlestick_chart(chart_data, show_volume=True, figure_size=(12, 6), 
                                        title=f'View {st.session_state.code} Stock Closing Price based on Historical Data', x_label='Date', y_label='Price', 
                                        colors=('green', 'red'))
                
                st.plotly_chart(fig, use_container_width=True)
        with st.expander("Prediction", True):    
            radio_predict = st.radio(
                "Choose Predict Next Day 👇",
                ["1 Day", "2 Days","3 Days","4 Days","5 Days","6 Days","7 Days"],
                horizontal=True,
            )
            data_before = data.get_before_data(st.session_state.code)
            data_before.set_index("time")
            data_before["predict"] = data_before['close']
            data_before = data_before[['close','predict']]
            col1, col2 = st.columns([3, 4])
            if radio_predict == "1 Day":
                x = data.Predict(1, st.session_state.code)
                x.index = np.arange(1, len(x) + 1)
                
                data_before.loc[len(data_before.index)] = [None,x['Predict Price'].values[0]]
                x['Predict Price'] = x['Predict Price'].map("{:,}".format)
              
                col1.table(x)
                col2.pyplot(draw(data_before),use_container_width=True)