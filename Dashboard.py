import streamlit as st
from services.service_factory import get_ServiceFactory

########################################################################################################################
# Settings and configurations
########################################################################################################################
st.set_page_config(page_title='Dashboard', page_icon='🇨🇦', layout='wide')

service_factory = get_ServiceFactory()
data_loader_service = service_factory.create_data_loader_service()
ploter_service = service_factory.create_ploter_service()

df = data_loader_service.load_data()


########################################################################################################################
# Dashboard Screen
########################################################################################################################
with st.container():
    st.header('Canada Data Jobs 2024')
    st.write('*Author: Leonardo Simões*')

    metrics_line = ploter_service.create_metrics_line(df)
    metrics_cols = st.columns(ploter_service.create_metrics_cols_size(metrics_line))

    for i in range(len(metrics_line)):
        with metrics_cols[i]:
            st.metric(label=metrics_line[i][0], value=metrics_line[i][1])

    # First Line
    st_col_1, st_col_2, st_col_3 = st.columns(3)

    with st_col_1:
        # Plot bar
        fig_1 = ploter_service.plot_bar(df, 'title')
        st.plotly_chart(fig_1, theme="streamlit", use_container_width=True)

    with st_col_2:
        # Plot pizza
        fig_2 = ploter_service.plot_pie(df, 'contractType')
        st.plotly_chart(fig_2, theme="streamlit", use_container_width=True)

    with st_col_3:
        # Plot barra
        fig_3 = ploter_service.plot_bar(df, 'sector', is_reversed=True)
        st.plotly_chart(fig_3, theme="streamlit", use_container_width=True)

    # Second Line
    st_col_4, st_col_5 = st.columns([2, 1])

    with st_col_4:
        # Plot area
        fig_4 = ploter_service.plot_area(df, 'publishedAt')
        st.plotly_chart(fig_4, theme="streamlit", use_container_width=True)

    with st_col_5:
        # Plot funil
        fig_5 = ploter_service.plot_funnel(df, 'experienceLevel')
        st.plotly_chart(fig_5, theme="streamlit", use_container_width=True)
