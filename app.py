import streamlit as st
from data import *
import pandas as pd
import datetime




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
    with st.sidebar:
        add_selectbox = st.selectbox(
        "What type of code do you want to predict today?",
        data.getStockCode(),
        index=None,
        placeholder="Select your Stock Code...",
    )
        btn_predict = st.button("Predict",on_click=toggle_expand(add_selectbox))
    with st.expander("Sector & Industry",expanded=True):
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
            if field_name != "ticker" and field_name != '_':
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
                col2.button(i['ticker'],use_container_width=True)

    with st.expander("Overview & Predict",expanded=True):
        st.code(st.session_state.code)
