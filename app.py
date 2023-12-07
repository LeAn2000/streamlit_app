import streamlit as st
from data import *
from streamlit.components.v1 import html
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import plotly.express as px
from vnstock import *  # import all functions, including functions that provide OHLC data for charting
from vnstock.chart import *
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


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


def reset_index(df):
    df.index = np.arange(1, len(df) + 1)


def draw(dataset, ti):
    plt.figure(figsize=(8, 2))
    plt.title(f"{ti} Stock Closing Price Trending Prediction", fontsize=8)
    plt.xlabel("Trading Date", fontsize=8)
    plt.ylabel("Closing Price (VND)", fontsize=8)
    # y = dataset['close'].to_list()
    # index = list(dataset.index)

    for i in range(len(dataset)):
        plt.plot(
            dataset.loc[i : i + 1, "time"],
            dataset.loc[i : i + 1, "close"],
            "bo-",
            color=("C1" if dataset.loc[i:i, "condition"][i] == 1 else "C0"),
        )

    plt.grid(which="major", color="k", linestyle="-.", linewidth=0.5)
    red_patch = mpatches.Patch(color="C0", label="Actual Price")
    blue_patch = mpatches.Patch(color="C1", label="Predicted Price")
    plt.legend(handles=[red_patch, blue_patch], fontsize=5)

    # after plotting the data, format the labels
    current_values = plt.gca().get_yticks()
    plt.gca().set_yticklabels(["{:,.0f}".format(x) for x in current_values])
    plt.xticks(fontsize=4, weight="bold")
    plt.yticks(fontsize=5, weight="bold")
    # current_x = plt.gca().get_xticks()
    # plt.gca().set_xticklabels([f'{x+1}' for x in current_x])

    # for x,y in zip(index,y):
    #     label = "{:.2f}".format(y)
    #     plt.annotate(label, # this is the text
    #              (x,y), # these are the coordinates to position the label
    #              textcoords="offset points", # how to position the text
    #              xytext=(0,10), # distance from text to points (x,y)
    #             fontsize=5,
    #              ha='right') # horizontal alignment can be left, right or center

    return plt


if __name__ == "__main__":
    data = DataGenerate()
    st.set_page_config(
        page_title="Stock Prediction",
        page_icon=None,
        layout="wide",
        initial_sidebar_state="auto",
        menu_items=None,
    )
    if "predict" not in st.session_state:
        st.session_state.predict = False
    if "code" not in st.session_state:
        st.session_state.code = "FPT"
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Sector & Industry", "Overview & Predict"])
    with tab1:
        domain_multi_selectbox = st.multiselect(
            "Choose your domain name to analyst data",
            data.getDomain(),
            default="Technology & Retail Trade",
            placeholder="Select your domain name ...",
            max_selections=5,
        )
        d = st.date_input("Choose trading date", value=get_previous_weekday())

        colms = st.columns((1, 1, 1, 1, 1, 1, 1, 1))
        fields = ["Domain", "Ticker", "Time", "Open", "High", "Low", "Close", "Volume"]
        for col, field_name in zip(colms, fields):
            if field_name != "Ticker" and field_name != "Domain":
                col.markdown(
                    f"<p class='header bold'>{field_name}</p>", unsafe_allow_html=True
                )
            else:
                col.markdown(
                    f"<p class='bold'>{field_name}</p>", unsafe_allow_html=True
                )
        st.markdown(
            """<hr style="height:1px;border:none;color:#333;background-color:#333;" /> """,
            unsafe_allow_html=True,
        )
        df = data.getDatanalyst(domain_multi_selectbox, d).to_dict("records")
        for i in df:
            col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(
                (1, 1, 1, 1, 1, 1, 1, 1)
            )
            col1.write(i["_"])
            col3.markdown(custommarkdown(i["time"]), unsafe_allow_html=True)
            col4.markdown(custommarkdown(i["open"]), unsafe_allow_html=True)
            col5.markdown(custommarkdown(i["high"]), unsafe_allow_html=True)
            col6.markdown(custommarkdown(i["low"]), unsafe_allow_html=True)
            col7.markdown(custommarkdown(i["close"]), unsafe_allow_html=True)
            col8.markdown(custommarkdown(i["volume"]), unsafe_allow_html=True)
            if i["ticker"] != "":
                if col2.button(i["ticker"], use_container_width=True):
                    st.session_state.code = i["ticker"]

    with tab2:
        with st.expander("Overview", True):
            with st.form("form"):
                filterr = list(data.getStockCode())
                col1, col2, col3 = st.columns([0.3, 1, 1])
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
            col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
            spacetime = relativedelta(months=12)
            todate = datetime.today()
            fromdate = todate - spacetime
            radio = st.radio(
                "Choose Trading Time 👇",
                [
                    "1 Week",
                    "1 Month",
                    "3 Months",
                    "6 Months",
                    "9 Months",
                    "12 Months",
                    "All Time",
                ],
                horizontal=True,
                index=5,
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
                fromdate = date(2013, 1, 1)
            fromdate = fromdate.strftime("%Y-%m-%d")
            todate = todate.strftime("%Y-%m-%d")
            if st.session_state.code != None:
                chart_data = data.getdateOverview(
                    st.session_state.code, fromdate, todate
                )
                fig = candlestick_chart(
                    chart_data,
                    show_volume=True,
                    figure_size=(12, 6),
                    title=f"View {st.session_state.code} Stock Closing Price based on Historical Data",
                    x_label="Date",
                    y_label="Price",
                    colors=("green", "red"),
                )

                st.plotly_chart(fig, use_container_width=True)
        with st.expander("Prediction", True):
            radio_predict = st.radio(
                "Choose Predict Next Day 👇",
                ["1 Day", "2 Days", "3 Days", "4 Days", "5 Days", "6 Days", "7 Days"],
                horizontal=True,
            )
            col1, col2 = st.columns(2)
            data_before_origin = data.get_before_data(st.session_state.code).tail(7)
            lastdate_price = data_before_origin["close"].values[-1]
            print(type(lastdate_price))
            lastdate = data_before_origin["time"].values[-1]
            data_before = data_before_origin
            data_before.set_index("time")
            data_before["condition"] = False
            # data_before["condition"].iloc[-1] = True
            data_before = data_before[["time", "close", "condition"]]
            data_before["time"] = data_before["time"].astype(str)
            step = {
                "1 Day": 1,
                "2 Days": 2,
                "3 Days": 3,
                "4 Days": 4,
                "5 Days": 5,
                "6 Days": 6,
                "7 Days": 7,
            }


            predict = data.Predict(step[radio_predict], st.session_state.code)
            meanPrice = predict["Predicted Price (VND)"].mean()
            reset_index(predict)
            for i in range(step[radio_predict]):
                data_before.loc[len(data_before.index)] = [
                    predict["The Next Day"].values[i],
                    predict["Predicted Price (VND)"].values[i],
                    True,
                ]
            predict["Predicted Price (VND)"] = predict["Predicted Price (VND)"].map(
                "{0:,.0f}".format
            )
            # predict['Predict with Indicator'] = predict['Predict with Indicator'].map("{0:,.2f}".format)
            data_before = data_before.reset_index(drop=True)
            s1 = data_before_origin[["time", "close"]]
            reset_index(s1)
            newframe = pd.concat([s1, predict], axis=1).reset_index(drop=True)
            reset_index(newframe)
            newframe = newframe.rename(
                columns={"time": "Trading Date", "close": "Actual Price (VND)"}
            ).fillna("")

            newframe.insert(loc=0, column="No.", value=newframe.index)
            newframe["Actual Price (VND)"] = newframe["Actual Price (VND)"].map(
                "{0:,.0f}".format
            )
            with col1:
                st.dataframe(
                    newframe,
                    use_container_width=True,
                    hide_index=True,
                )
            with col2:
                st.code(f"Last date is {lastdate} with price: {lastdate_price:,} VND")
                st.code(f"Mean of {step[radio_predict]} day(s) predict price: {meanPrice:,.0f} VND")
                if lastdate_price > meanPrice:
                    st.code("Trend will be Downtrend ")
                else:
                    st.code("Trend will be UpTrend")
            print("I'm here to listen update ")
            st.pyplot(
                draw(data_before, st.session_state.code), use_container_width=True
            )
        with st.expander("Check Predicted Result", True):
            st.code(2)
######