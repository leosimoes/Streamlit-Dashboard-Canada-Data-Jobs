import streamlit as st
import pandas as pd


class DataLoaderService:

    @st.cache_data
    def load_data(_self):
        df = pd.read_csv('data/dataset.csv')
        df['publishedAt'] = pd.to_datetime(df['publishedAt'], format='%Y-%m-%d')
        df.sort_values(by='publishedAt', inplace=True)
        return df
