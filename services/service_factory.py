import streamlit as st
from services.data_loader_service import DataLoaderService
from services.ploter_service import PloterService


class ServiceFactory:

    @st.cache_data
    def create_data_loader_service(_self):
        return DataLoaderService()

    @st.cache_data
    def create_ploter_service(_self):
        return PloterService()


@st.cache_data
def get_ServiceFactory():
    return ServiceFactory()
