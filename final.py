import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load data
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize Dash app
app = dash.Dash(__name__)

# Dropdown options
year_list = sorted(data['Year'].unique())

app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard",
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': '24px'}),

    html.Div([
        html.Label("Select Report Type:"),
        dcc.Dropdown(
            id='report-type',
            options=[
                {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
            ],
            value='Yearly Statistics',
            placeholder='Select Report Type'
        )
    ], style={'marginTop': '10px'}),

    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': i, 'value': i} for i in year_list],
            value=year_list[0]
        )
    ], style={'marginTop': '10px'}),

    html.Div(id='output-container', className='output-container', style={'marginTop': '20px'})
])

# Enable/disable year dropdown
@app.callback(
    Output('select-year', 'disabled'),
    Input('report-type', 'value')
)
def toggle_year(report_type):
    return report_type != 'Yearly Statistics'

# Graph rendering callback
@app.callback(
    Output('output-container', 'children'),
    [Input('report-type', 'value'),
     Input('select-year', 'value')]
)
def update_output(selected_statistics, input_year):
    if selected_statistics == 'Recession Period Statistics':
        recession_data = data[data['Recession'] == 1]

        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(figure=px.line(yearly_rec, x='Year', y='Automobile_Sales',
                                            title="Average Automobile Sales fluctuation over Recession Period"))

        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales',
                                           title="Average Number of Vehicles Sold by Vehicle Type"))

        exp_rec = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(figure=px.pie(exp_rec, names='Vehicle_Type', values='Advertising_Expenditure',
                                           title="Total Expenditure Share by Vehicle Type During Recession"))

        unemp_data = recession_data.groupby(['unemployment_rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()
        R_chart4 = dcc.Graph(figure=px.bar(unemp_data, x='unemployment_rate', y='Automobile_Sales', color='Vehicle_Type',
                                           labels={'unemployment_rate': 'Unemployment Rate',
                                                   'Automobile_Sales': 'Average Automobile Sales'},
                                           title='Effect of Unemployment Rate on Vehicle Type and Sales'))

        return [
            html.Div(className='chart-item', children=[R_chart1, R_chart2], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[R_chart3, R_chart4], style={'display': 'flex'})
        ]

    elif selected_statistics == 'Yearly Statistics' and input_year:
        yearly_data = data[data['Year'] == input_year]

        yas = data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales',
                                            title='Average Automobile Sales (1980–2013)'))

        mas = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(figure=px.line(mas, x='Month', y='Automobile_Sales',
                                            title=f'Total Monthly Automobile Sales in {input_year}'))

        avr_vdata = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(figure=px.bar(avr_vdata, x='Vehicle_Type', y='Automobile_Sales',
                                           title=f'Average Vehicles Sold by Vehicle Type in {input_year}'))

        exp_data = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(figure=px.pie(exp_data, names='Vehicle_Type', values='Advertising_Expenditure',
                                           title=f'Total Advertisement Expenditure in {input_year}'))

        return [
            html.Div(className='chart-item', children=[Y_chart1, Y_chart2], style={'display': 'flex'}),
            html.Div(className='chart-item', children=[Y_chart3, Y_chart4], style={'display': 'flex'})
        ]

    else:
        return None

# Run the app
if __name__ == '__main__':
    app.run(debug=True)


        


