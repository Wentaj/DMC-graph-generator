import dash_mantine_components as dmc 
from dash import Dash, dcc, html, Input, State, Output, callback
import plotly.express as px
import pandas as pd
import io
import base64

app = Dash()

"""file = input("Choose your source file")
while True:
    if not os.path.exists(file): 
        break
    if pathlib.Path(file).suffix != csv:
        break
def loadFile():
    data = csv.load(open('dirs.csv', 'r'))
"""
app.layout = [
    dmc.MantineProvider(
        dmc.Alert(
            title="Automatic DMC graph creator",
            color="cyan"
        ),
    ),
    html.Div([
        dcc.Upload(
            #accept=".csv",
            id="graphSource",
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            multiple=False
        ),
        html.Div(id='output')
    ])
]
# @callback(
#     Output(component_id='output', component_property='children'),
#     Input(component_id='graphSource', component_property='contents')
#)
def createGraph(content, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date))
    ])


if __name__ == "__main__":
    app.run(debug=True)