import streamlit as st
from data import *
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta 
import plotly.express as px
from vnstock import * #import all functions, including functions that provide OHLC data for charting
from vnstock.chart import * 
def custommarkdown(field_name):
    return f'<p class="tablefield">{field_name}<p>'

def toggle_expand(code):
    st.session_state.code = code  

if __name__ == "__main__":
    data = DataGenerate()
    st.set_page_config(page_title="Stock Prediction", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
    if "predict" not in st.session_state:
        st.session_state.predict = False
    if "code" not in st.session_state:
        st.session_state.code = None
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)
        
    
    tab1, tab2 = st.tabs(["Sector & Industry","Overview & Predict"])
    with tab1:
        domain_multi_selectbox = st.multiselect(
        "Choose your domain name to analyst data",
        data.getDomain(),
        placeholder="Select your domain name ...",
        max_selections = 5
        )
        d = st.date_input("Choose trading date", value="today")
        colms = st.columns((1, 1, 1, 1, 1,1,1,1))
        fields = ["Domain","Ticker","Time","Open","High","Low","Close","Volume"]
        for col, field_name in zip(colms, fields):
            if field_name != "Ticker" and field_name != 'Domain':
                col.markdown(f"<p class='header'>{field_name}</p>",unsafe_allow_html=True)
            else:
                col.markdown(field_name)
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
                col1,col2,col3= st.columns([0.3,1,1])
                col1.write("Input Stock Code:")
                add_selectbox = col2.selectbox(
                "a",   
                data.getStockCode(),
                index=None,
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
            
            with col1:
                if st.button("1 Week"):
                    
                    fromdate = todate - spacetime
                    
            with col2:
                if st.button("1 Month"):
                    spacetime = relativedelta(months=1)
                    fromdate = todate - spacetime
                    
            with col3:
                if st.button("3 Months"):
                    spacetime = relativedelta(months=3)
                    fromdate = todate - spacetime
                
            with col4:
                if st.button("6 Months"):
                    spacetime = relativedelta(months=6)
                    fromdate = todate - spacetime
                
            with col5:
                if st.button("9 Months"):
                    spacetime = relativedelta(months=9)
                    fromdate = todate - spacetime
                
            with col6:
                if st.button("12 Months"):
                    spacetime = relativedelta(months=12)
                    fromdate = todate - spacetime
            with col7:
                if st.button("All Time"):
                    fromdate  = date(2013,1,1)
            fromdate = fromdate.strftime('%Y-%m-%d')
            todate = todate.strftime('%Y-%m-%d')
            if st.session_state.code != None:
                chart_data = data.getdateOverview(st.session_state.code, fromdate, todate)
                fig = candlestick_chart(chart_data, show_volume=True, figure_size=(12, 6), 
                                        title=f'View {st.session_state.code} Stock Closing Price based on Historical Data', x_label='Date', y_label='Price', 
                                        colors=('lightgray', 'gray'), reference_colors=('black', 'blue'))
                st.plotly_chart(fig)