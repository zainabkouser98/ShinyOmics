#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Install Dash, Dash Core Components, Dash HTML Components, and Scanpy
get_ipython().system('pip install dash dash-core-components dash-html-components scanpy')


# In[3]:


get_ipython().system('pip install dash dash-core-components dash-html-components dash-bootstrap-components plotly pandas')


# In[4]:


pip install jupyter-dash


# In[5]:


get_ipython().system('pip uninstall pandas -y')
get_ipython().system('pip install pandas')


# In[6]:


get_ipython().system('pip install --upgrade pandas')


# In[7]:


pip install dash --upgrade


# In[8]:


pip install dash-bootstrap-components


# In[10]:


conda install -c conda-forge dash-download-components


# In[11]:


pip install -U kaleido


# In[12]:


pip install --upgrade plotly


# In[22]:


pip install --upgrade numpy scipy seaborn


# In[1]:


pip install numpy==1.23.0 scipy==1.9.0 seaborn==0.11.2


# In[1]:


pip install numpy scipy seaborn matplotlib pandas plotly dash dash-bootstrap-components


# In[15]:


# Import necessary libraries
import pandas as pd
import plotly.express as px
import base64
import io
from dash import dcc, html, Input, Output, Dash, State
import dash_bootstrap_components as dbc
import numpy as np
import plotly.graph_objects as go

# Initialize the Dash app with Bootstrap
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout of the app
app.layout = dbc.Container(
    fluid=True,
    children=[
        dbc.Row(
            [
                # White portion with header text
                dbc.Col(
                    html.Div([
                        html.H1("ShinyOmics", style={'color': '#000000', 'text-align': 'center'}),
                        html.P("Welcome to ShinyOmics! This is where you can visualize your single-cell data.", style={'color': '#000000', 'text-align': 'center'}),
                    ],
                        style={'background-color': '#FFFFFF', 'height': '20vh', 'padding': '20px'}),
                    width=12,
                    style={'padding': '0px'}
                ),

                # Black portion on the left
                dbc.Col(
                    html.Div([
                        dcc.Upload(
                            id='upload-data',
                            children=[
                                dbc.Button(['Upload CSV File'], id='upload-button', color='primary', className='mb-3', style={'border-radius': '12px'}),
                            ],
                            multiple=False
                        ),
                        dcc.Dropdown(
                            id='plot-type',
                            options=[
                                {'label': 'Histogram', 'value': 'histogram'},
                                {'label': 'Violin Plot', 'value': 'violin'},
                                {'label': 'Pie Chart', 'value': 'pie'},
                                {'label': 'Box Plot', 'value': 'box'},
                                {'label': 'Line Plot', 'value': 'line'},
                                {'label': 'Bar Plot', 'value': 'bar'},
                                {'label': 'Scatter Plot', 'value': 'scatter'},
                                {'label': '3D Scatter Plot', 'value': 'scatter_3d'},
                                {'label': 'Hexbin Plot', 'value': 'hexbin'}
                            ],
                            value='histogram',
                            style={'width': '100%', 'margin-bottom': '10px', 'border-radius': '12px'}
                        ),

                        dcc.Dropdown(
                            id='multi-column-dropdown',
                            options=[],
                            multi=True,
                            style={'width': '100%', 'margin-bottom': '10px', 'border-radius': '12px'}
                        ),

                        html.Button('Generate Plot', id='plot-button', className='mb-3', style={'border-radius': '12px', 'background-color': 'yellow'}),

                        dcc.Input(id='graph-title-input', type='text', placeholder='Enter Graph Title', className='mb-3', style={'border-radius': '12px'}),
                        dcc.Input(id='num-rows', type='number', placeholder='Number of Sample Rows', className='mb-3', style={'border-radius': '12px'}),

                        html.A(
                            'Export as Image',
                            id='export-button',
                            download='graph.png',
                            href='',
                            target='_blank',
                            style={'display': 'none', 'border-radius': '12px'},
                            className='mb-3'
                        ),
                    ],
                        style={'background': 'linear-gradient(to right, #282c34, #3d4852)', 'height': '100vh', 'padding': '20px', 'position': 'relative'},
                    ),
                    width=3,  # Adjust the width of the black portion
                ),

                # Content on the right
                dbc.Col(
                    html.Div([
                        dcc.Graph(id='graph-output'),
                    ],
                        style={'background-color': '#FFFFFF', 'padding': '20px'}),
                ),
            ],
        ),
    ]
)

# Callback to update the dropdown options based on the uploaded data
@app.callback(
    Output('multi-column-dropdown', 'options'),
    Input('upload-data', 'contents')
)
def update_dropdown(contents):
    if contents is None:
        return []

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    options = [{'label': col, 'value': col} for col in df.columns]
    return options

# Callback to show/hide the customization options
@app.callback(
    Output('export-button', 'style'),
    Input('plot-type', 'value')
)
def show_hide_customization_options(plot_type):
    export_button_style = {'display': 'none'}

    if plot_type in ['scatter', 'scatter_3d', 'hexbin']:
        export_button_style = {'display': 'block'}

    return export_button_style

# Callback to update the graph based on user selection
@app.callback(
    Output('graph-output', 'figure'),
    [
        Input('plot-button', 'n_clicks'),
        Input('plot-type', 'value'),
        Input('upload-data', 'contents'),
        Input('graph-title-input', 'value'),
        Input('num-rows', 'value'),
        Input('multi-column-dropdown', 'value'),
    ]
)
def update_graph(n_clicks, plot_type, contents, graph_title, num_rows, selected_columns):
    if n_clicks is None or contents is None:
        return go.Figure()

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    if not selected_columns:
        selected_columns = df.columns.tolist()

    figure = None
    color_discrete_sequence = px.colors.qualitative.Set1

    # Define specific handling for each plot type
    if plot_type == 'line':
        if len(selected_columns) < 1:
            return go.Figure()
        x_axis = df.index if len(selected_columns) == 1 else selected_columns[0]
        y_axis = selected_columns[0] if len(selected_columns) == 1 else selected_columns[1]
        figure = px.line(df, x=x_axis, y=y_axis, title=graph_title or 'Line Plot', color_discrete_sequence=color_discrete_sequence)

    elif plot_type == 'histogram':
        if len(selected_columns) < 1:
            return go.Figure()
        x_axis = selected_columns[0]
        figure = px.histogram(df, x=x_axis, marginal='box', nbins=47, color='celltype' if 'celltype' in df.columns else None, title=graph_title or f'Distribution of {x_axis}')
        figure.update_layout(bargap=0.1)

    elif plot_type == 'bar':
        if len(selected_columns) < 2:
            return go.Figure()
        x_axis = selected_columns[0]
        y_axis = selected_columns[1]
        df_sample = df.sample(10) if num_rows is None else df.head(num_rows)
        figure = px.bar(df_sample, x=x_axis, y=y_axis, color='celltype' if 'celltype' in df.columns else None, title=graph_title or f'Distribution of {x_axis} and {y_axis}', barmode='group')
        figure.update_traces(width=0.8)

    elif plot_type == 'scatter':
        if len(selected_columns) < 2:
            return go.Figure()
        x_axis = selected_columns[0]
        y_axis = selected_columns[1]
        color_column = selected_columns[2] if len(selected_columns) > 2 else None
        figure = px.scatter(df, x=x_axis, y=y_axis, color=color_column, opacity=0.8, hover_data=['celltype'] if 'celltype' in df.columns else None, title=graph_title or f'{x_axis} vs. {y_axis}')
        figure.update_traces(marker_size=5)

    elif plot_type == 'scatter_3d':
        if len(selected_columns) < 3:
            return go.Figure()
        x_axis = selected_columns[0]
        y_axis = selected_columns[1]
        z_axis = selected_columns[2]
        color_column = selected_columns[3] if len(selected_columns) > 3 else None
        figure = px.scatter_3d(df, x=x_axis, y=y_axis, z=z_axis, color=color_column, opacity=0.8, hover_data=['celltype'] if 'celltype' in df.columns else None, title=graph_title or f'{x_axis} vs. {y_axis} vs. {z_axis}')
        figure.update_traces(marker_size=5)

    elif plot_type == 'violin':
        if len(selected_columns) < 1:
            return go.Figure()
        y_axis = selected_columns[0]
        figure = px.violin(df, y=y_axis, color='celltype' if 'celltype' in df.columns else None, title=graph_title or f'Distribution of {y_axis}', orientation='v', box=True, points='all')
        figure.update_layout(bargap=0.1)

    elif plot_type == 'pie':
        if len(selected_columns) < 1:
            return go.Figure()
        names = selected_columns[0]
        figure = px.pie(df, names=names, title=graph_title or f'Distribution of {names}')

    elif plot_type == 'box':
        if len(selected_columns) < 1:
            return go.Figure()
        y_axis = selected_columns[0]
        figure = px.box(df, y=y_axis, color='celltype' if 'celltype' in df.columns else None, title=graph_title or f'Distribution of {y_axis}', orientation='v')
        figure.update_layout(bargap=0.1)

    elif plot_type == 'hexbin':
        if len(selected_columns) < 2:
            return go.Figure()
        x_axis = selected_columns[0]
        y_axis = selected_columns[1]
        df_sample = df.head(num_rows) if num_rows else df
        figure = px.density_heatmap(df_sample, x=x_axis, y=y_axis, marginal_x='histogram', marginal_y='histogram', title=graph_title or f'Hexbin Plot: {x_axis} vs. {y_axis}')

    return figure

# Main function
if __name__ == '__main__':
    app.run_server(debug=True)


# In[ ]:




