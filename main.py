import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import altair as alt
import matplotlib.pyplot as plt
from streamlit_extras.dataframe_explorer import dataframe_explorer


st.set_page_config(page_title="Home", page_icon="", layout="wide")

df = pd.read_csv('/Users/adebolaorogun/Documents/GitHub/BA py/Python-Business-analytics-dashboard-/data.csv')

#st.dataframe(df,use_container_width=True)
#st.sidebar.image("")
with st.sidebar:
    st.title("Select Date Range")
    start_date = st.date_input(label="Start date")

with st.sidebar:
    end_date = st.date_input(label="End date")
    
st.error("you have chosen analytics from: "+str(start_date) + "to" + str(end_date))

df2 = df[(df["OrderDate"]>=str(start_date)) & (df["OrderDate"]<=str(end_date))]
st.dataframe(df2)

with st.expander("filter Data"):
    filtered_df = dataframe_explorer(df2, case=False)
    st.dataframe(filtered_df, use_container_width=True)

a1, a2 = st.columns(2)

with a1:
    st.subheader('Product & Quantities')
    source = pd.DataFrame({
        "Quantity ($)" : df2['Quantity'],
        "Product" : df2["Product"]
    })
    bar_chart = alt.Chart(source).mark_bar().encode(
        x="sum(Quantity ($)):Q",
        y = alt.Y("Product:N", sort="-x")
    )
    st.altair_chart(bar_chart, use_container_width=True)

with a2:
    st.subheader('Data Metrics')
    from streamlit_extras.metric_cards import style_metric_cards
    col1, col2 = st.columns(2)
    col1.metric("Number of Items", value=df2["Product"].count(), delta="All Items")
    col2.metric("Sum of product USD", value=f"{df2['TotalPrice'].sum():,.0f}", delta=df2["TotalPrice"].median())

    c11, c22, c33 = st.columns(3)
    c11.metric("Max Price", value=f"{df2['TotalPrice'].max():,.0f}", delta="High price")
    c22.metric("Min Price", value=f"{df2['TotalPrice'].min():,.0f}", delta="Low Price")
    c33.metric("Price Range", value=f"{df2['TotalPrice'].max() - df2['TotalPrice'].min():,.0f}", delta="Range")

    style_metric_cards(background_color="#ede5ce", border_left_color="#8a6606", border_color="#e8b527")

b1,b2 = st.columns(2)
with b1:
    st.subheader("Product & Total price")
    source = df2
    chart = alt.Chart(source).mark_circle().encode(
        x="Product",
        y="TotalPrice",
        color="Category"
    ).interactive()
    st.altair_chart(chart, theme="streamlit", use_container_width=True)

with b2:
   st.subheader("Product & Unit price")
   bar_chart = alt.Chart(df2).mark_bar().encode(
    x="month(OrderDate):O",
    y="sum(UnitPrice):Q",
    color="Product:N"
    )
   st.altair_chart(bar_chart, use_container_width=True)

