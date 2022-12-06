import streamlit as st
import yfinance as yf

st.set_page_config(
    page_title="주식 차트",
    layout="centered"
)


periods = "1mo"
intervals = "5d"

menu = st.form("list", clear_on_submit=True)
info = st.container()
major = st.container()
minor = st.columns(2)


def get_names():
    name_list = []
    for i in stock_code_ls:
        name_list.append(yf.Ticker(i).info['shortName'])
    return name_list


def get_codes():
    code_list = []
    for i in stock_name_ls:
        code_list.append(yf.Ticker(i).info['shortName'])
    return code_list


def rendering():
    print("Periods", periods)
    print("Intervals", intervals)

    # Major Stock option ==============
    major_info = yf.Ticker(stock_code_ls[0]).info
    major.subheader(major_info['longName'] + "  (" + major_info['symbol'] + ")")
    major.write("#### " + major_info['currentPrice'] + "~K~R~W")
    major.line_chart(yf.download(stock_code_ls[0], period=periods, interval=intervals))

    # Minor Stock options =============
    for i in range(1, len(stock_code_ls)):
        j = i + 1
        minor_info = yf.Ticker(stock_code_ls[i]).info
        minor[j % 2].subheader(minor_info['shortName'] + "\n(" + minor_info['symbol'] + ")")
        minor[j % 2].line_chart(yf.download(stock_code_ls[i], period=periods, interval=intervals))


stock_code_ls = ["005930.KS", "035720.KS", "051910.KS", "005380.KS", "207940.KS", "035420.KS", "034220.KS", "000660.KS", "016360.KS"]
stock_name_ls = get_names()


with menu:
    stock_code = st.text_input(
        label="stock code", label_visibility="collapsed",
        placeholder="Type Stock code here")

    st.empty()
    sort_type = st.selectbox(
        label="정렬 옵션",
        options=("이름 오름차순", "이름 내림차순", "사용자 정의"))
    custom_sort = st.multiselect(
        label="custom sort",
        label_visibility="collapsed",
        options=stock_name_ls,
        default=stock_name_ls)

    st.empty()
    stock_period = st.selectbox(
        label="차트 기간 변경",
        options=("1d", "5d", "1mo", "3mo", "6mo", "1y"))
    stock_interval = st.selectbox(
        label="차트 간격 변경",
        options=("5m", "15m", "30m", "60m", "90m", "1h", "1d", "5d", "1wk","1mo", "3mo"))

    submitted = st.form_submit_button(label="Submit", type="primary")
    if  submitted:
        stock_code_ls.append(stock_code)
        stock_name_ls = get_names()

        if  sort_type == "이름 오름차순":
            stock_name_ls.sort()
            stock_code_ls = get_codes()
        elif sort_type == "이름 내림차순":
            stock_name_ls.sort()
            stock_name_ls.reverse()
            stock_code_ls = get_codes()
        elif sort_type == "사용자 정의":
            stock_name_ls = custom_sort
            stock_code_ls = get_codes()

        periods = stock_period
        intervals = stock_interval

        with info:
            with st.spinner('Wait for rendering'):
                rendering()
            st.success('Done!')
