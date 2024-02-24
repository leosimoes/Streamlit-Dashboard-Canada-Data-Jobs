import streamlit as st
import plotly.express as px


class PloterService:

    _FIGURE_TITLE_LAYOUT = {'y': 0.9, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'}
    _FIGURE_TITLE_LAYOUT_v2 = {'y': 0.9, 'x': 0.54, 'xanchor': 'center', 'yanchor': 'top'}
    _FIGURE_LEGEND = {'y': 1, 'x': 1, 'xanchor': 'right', 'yanchor': 'top'}
    _FIGURE_LEGEND_V2 = {'orientation': 'h', 'y': -0.2, 'x': 0.5, 'yanchor': 'bottom', 'xanchor': 'center'}
    _FIGURE_HEIGHT = 330
    _TITLE_BY_COLUMN = {
        'title': 'Roles',
        'contractType': 'Type of Contract',
        'sector': 'Sectors',
        'experienceLevel': 'Experience Level',
        'publishedAt': 'Publication dates'
    }

    @st.cache_data
    def create_metrics_line(_self, df):
        """
        Returns a tuple of label and value pairs.

        Arguments:
        df -- DataFrame
        """
        return (
            ('Job Openings', df.shape[0]),
            ('Roles', df['title'].nunique()),
            ('Work Types', df['workType'].nunique()),
            ('Sectors', df['sector'].nunique()),
            ('Earliest Date', str(df['publishedAt'].min()).split()[0].replace('-', '/')),
            ('Most Recent Date', str(df['publishedAt'].max()).split()[0].replace('-', '/'))
        )

    @st.cache_data
    def create_metrics_cols_size(_self, metrics_line):
        """
        Returns a list of column widths.

        Arguments:
        metrics_line -- tuple
        """
        return [1] * len(metrics_line[:-2]) + [2, 2]

    def _count_grouping(_self, df, grouped_columns, counted_column='id', sorted_column='Quantity', is_ascending=False):
        """
        Returns a dataframe with absolute and percentage counts by column group.

        Arguments:
        df -- DataFrame
        grouped_columns -- list
        counted_column -- string
        sorted_column -- string
        is_ascending -- bool
        """
        df_clustered = df.groupby(grouped_columns, as_index=False, observed=False)
        df_counted = df_clustered[counted_column].count()
        df_counted = df_counted.rename(columns={counted_column: 'Quantity'})
        df_counted = df_counted.sort_values(by=sorted_column, ascending=is_ascending)

        df_counted['Percentage'] = df_counted['Quantity'] / df_counted['Quantity'].sum()
        df_counted['Percentage'] = (df_counted['Percentage'] * 100).round(2)
        df_counted['Percentage'] = df_counted['Percentage'].astype(str) + '%'

        df_counted.reset_index(drop=True, inplace=True)
        df_counted.index = df_counted.index + 1

        return df_counted

    @st.cache_data
    def plot_bar(_self, df, col, is_reversed=False):
        """
        Plots a bar chart.

        Arguments:
        df -- DataFrame
        col -- string
        is_reversed -- bool (Optional - Default value is False)
        """
        df_count = _self._count_grouping(df, [col])
        extra_data = ('Percentage')
        colors_list = ['white'] * df_count.shape[0]
        title = PloterService._TITLE_BY_COLUMN.get(col)

        fig = px.bar(df_count,
                     x='Quantity',
                     y=col,
                     color=col,
                     color_discrete_sequence=colors_list,
                     hover_data=extra_data,
                     text='Quantity',
                     title=title,
                     height=PloterService._FIGURE_HEIGHT)

        fig.update_layout(showlegend=False)
        fig.update_layout(title=PloterService._FIGURE_TITLE_LAYOUT)
        fig.update_traces(textposition='inside')
        fig.update_xaxes(title=None)
        fig.update_yaxes(title=None)

        if is_reversed:
            fig.update_layout(xaxis=dict(autorange='reversed'), yaxis=dict(side='right'))

        return fig

    @st.cache_data
    def plot_pie(_self, df, col):
        """
        Plots a pie chart.

        Arguments:
        df -- DataFrame
        col -- string
        """
        df_count = _self._count_grouping(df, [col])
        colors_list = ['white', 'silver', 'skyblue']
        title = PloterService._TITLE_BY_COLUMN.get(col)

        fig = px.pie(df_count,
                     names=col,
                     values='Quantity',
                     color=col,
                     color_discrete_sequence=colors_list,
                     title=title,
                     height=PloterService._FIGURE_HEIGHT)

        fig.update_layout(title=PloterService._FIGURE_TITLE_LAYOUT, legend=PloterService._FIGURE_LEGEND_V2)
        fig.update_xaxes(title=None)
        fig.update_yaxes(title=None)

        return fig

    @st.cache_data
    def plot_funnel(_self, df, col):
        """
        Plots a funnel chart.

        Arguments:
        df -- DataFrame
        col -- string
        """
        df_count = _self._count_grouping(df, [col])
        extra_data = ('Percentage')
        color_list = ['white'] * df_count.shape[0]
        title = PloterService._TITLE_BY_COLUMN.get(col)

        fig = px.funnel(df_count,
                        x='Quantity',
                        y=col,
                        hover_data=extra_data,
                        title=title,
                        #category_orders=order,
                        color=col,
                        color_discrete_sequence=color_list,
                        height=PloterService._FIGURE_HEIGHT)

        fig.update_layout(title=PloterService._FIGURE_TITLE_LAYOUT_v2)
        # fig.update_layout(funnelgap=0.5)
        fig.update_layout(showlegend=False)
        fig.update_traces(marker_line_color='white', marker_line_width=0.5)
        fig.update_xaxes(title=None)
        fig.update_yaxes(title=None)

        return fig

    #@st.cache_data
    def plot_area(_self, df, col):
        """
        Plots an area graph.

        Arguments:
        df -- DataFrame
        col -- string
        """
        df_count = _self._count_grouping(df, [col], sorted_column=col)
        extra_data = ('Percentage')
        df_count['color'] = 'white'
        color_list = ['white']
        title = PloterService._TITLE_BY_COLUMN.get(col)

        fig = px.area(df_count,
                      x=col,
                      y='Quantity',
                      color='color',
                      hover_data=extra_data,
                      color_discrete_sequence=color_list,
                      title=title,
                      height=PloterService._FIGURE_HEIGHT,
                      markers=True)

        fig.update_layout(title=PloterService._FIGURE_TITLE_LAYOUT)
        fig.update_layout(showlegend=False)
        fig.update_layout(barmode='overlay')
        fig.update_traces(stackgroup=None, fill='tozeroy')
        fig.update_xaxes(title=None)
        fig.update_yaxes(title=None)

        return fig
