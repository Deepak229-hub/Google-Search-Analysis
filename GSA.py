import time
from pytrends.request import TrendReq
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from PIL import Image
import random

st.title("Google Search Analysis 📈")
st.caption("This application is designed to get insights of a trend. You'll get to know the interest by sub-region and the rate of the interest over time.")
st.markdown("---")
key = st.text_input("Enter a keyword: ")


pytrends = TrendReq(hl="en-US", tz=360) 

def fetch_trends(keyword):
    try:
        pytrends.build_payload([keyword], geo="IN", timeframe="today 1-m")

        
        time.sleep(5)  

        df = pytrends.interest_by_region().head(10)
        df1 = pytrends.interest_over_time().head(10)
        return df.sort_values(by=keyword, ascending=False), df1.sort_values(by=keyword, ascending=False)
    except Exception as e:
        st.write("Couldn't fulfill your request. Try again after some time!", e)
        return None


if key:
    with st.spinner("Fetching Data..."):
        df, df1 = fetch_trends(key)
    st.markdown("### Interest by Sub-Region")

    col1, col2 = st.columns(2)

    with col1:

        if df is not None:
            st.dataframe(df.head(10))

    with col2:
        fig, ax = plt.subplots()
        df.plot(kind="bar", ax=ax)
        ax.set_xlabel("Region")
        ax.set_ylabel("Search Interest")
        ax.tick_params(axis='x', rotation=90, labelsize=8)
        st.pyplot(fig)

    if df1 is not None:
        df1 = df1.head(10)

        st.markdown("### Interest Over Time")

        fig1, ax1 = plt.subplots()
        df1.plot(kind="barh", ax=ax1, legend=False)
        ax1.set_ylabel("Date")
        ax1.set_xlabel("Search Interest")
        st.pyplot(fig1)

    next_data = st.text_input("Enter the keyword to compare with!")
    if next_data:
        with st.spinner("Fetching Data..."):
            df2, df3 = fetch_trends(next_data)

        if df2 is not None and df3 is not None:
            col4, col5 = st.columns(2)
            with col4:
                st.markdown("##### Comparison with Interest by Sub-region:")
                fig2, ax2 = plt.subplots()
                df.plot(kind="bar", ax=ax2, position=0, width=0.4, alpha=0.7)
                df2.plot(kind="bar", ax=ax2, color='orange', position=1, width=0.4, alpha=0.7)
                ax2.set_xlabel("Region")
                ax2.set_ylabel("Search Interest")
                ax2.tick_params(axis='x', rotation=90, labelsize=8)
                st.pyplot(fig2)

            with col5:
                st.markdown("##### Comparison with Interest Over Time: ")
                fig3, ax3 = plt.subplots()
                df1.plot(kind="barh", ax=ax3, position=0, width=0.4, alpha=0.7)
                df3.plot(kind="barh", ax=ax3, position=1, width=0.4, alpha=0.7, color="orange")
                ax3.set_ylabel("Date")
                ax3.set_xlabel("Search Interest")
                # yticks = ax3.get_yticks()
                # ax3.set_yticks(yticks[0], yticks[-1])
                # ax3.set_yticklabels([int(yticks[0]), int(yticks[-1])])
                st.pyplot(fig3)
        else:
            st.warning("Couldn't fetch data! Try again later!")
    else:
        st.markdown("***Please enter a keyword to Compare with!***")
else:
    st.markdown("***Please enter a keyword to search!***")

