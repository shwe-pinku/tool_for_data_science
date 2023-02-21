# Import required libraries
import pandas as pd
import plotly.graph_objects as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_data =  pd.read_csv('spacex_launch_dash.csv')
max_payload=spacex_data['Payload Mass (kg)'].max()
min_payload=spacex_data['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Build dash app layout
app.layout = html.Div(children=[ html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36',
                                'font-size': 30}),
                                dcc.Dropdown(id='site-dropdown',
                                options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}],
                                value='ALL',
                                placeholder="place holder here",
                                searchable=True),
                                #html.Div(["Input Year: ", dcc.Input()],
                                #style={'font-size': 30}),
                                html.Br(),

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(), 
                                html.P("Payload range (Kg):"),

                                dcc.RangeSlider(
                                        id='payload-slider',
                                        min=0, max=10000, step=1000,
                                        marks={0: '0',
                                                2500: '2500',
                                                5000: '5000',
                                                7500: '7500',
                                                10000: '10000'},
                                        value=[min_payload, max_payload]
                                    ),

                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),                             
                                ])


# Function decorator to specify function input and output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(site_dropdown):
    if site_dropdown == 'ALL':
        fig = px.pie(spacex_data[['Launch Site', 'class']], values='class', names='Launch Site', 
        title=f'Total Success Launches for Site {site_dropdown}')        
        return fig
    else:        
        filtered_drop = spacex_data[spacex_data['Launch Site']==site_dropdown]
        filtered_launch=filtered_drop.groupby(['Launch Site', 'class']).size().reset_index(name='class count')
        fig = px.pie(filtered_launch, values='class count', names='class',
        title=f'Total Success Launches for Site {site_dropdown}')
        return fig

# Function decorator to specify function input and output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload-slider', component_property='value')])
def get_scatter_graph(entered_site, slider):
    filtered_df = spacex_data
    if entered_site == 'ALL':
        data = spacex_data[(spacex_data['Payload Mass (kg)']>= slider[0])&(spacex_data['Payload Mass (kg)']<=slider[1])]
        plot = px.scatter(data, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return plot
    else:
        selected_site=spacex_data.loc[spacex_data['Launch Site']==entered_site]
        data=selected_site[(selected_site['Payload Mass (kg)']>=slider[0])&(spacex_data['Payload Mass (kg)']<=slider[1])]
        plot = px.scatter(data, x='Payload Mass (kg)', y='class', color='Booster Version Category')
        return plot
if __name__ == '__main__':
    app.run_server()