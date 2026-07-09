import dash_mantine_components as dmc
from dash import Dash, dcc, html, Input, State, Output, callback, ALL, ctx
import plotly.express as px
import pandas as pd
import io
import base64

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = dmc.MantineProvider(
    html.Div([
        dmc.Alert(
            title="Automatic DMC graph creator",
            color="cyan"
        ),
        html.Div([
            dcc.Upload(
                #accept=".csv",
                id="graphSource",
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '100px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px',
                    'padding-top': '20px'
                },
                multiple=False,
            
            ),
            dcc.Store(id="stored-data"),
            dcc.Store(id="stored-filename"),
            dcc.Store(id="selected-column"),
            html.Div(id='output')
        ])
    ])
)

cont = ""

def parseContent(contents, filename):
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
        html.H5(filename)
    ])

def createGraph(df, filename, selected_col=None, sort_order="asc"):
    cols = df.columns.tolist()

    if len(cols) == 0:
        return html.Div([
            html.H5(filename),
            html.Div("No columns found.")
        ])

    if selected_col is None or selected_col not in cols:
        numeric_cols = df.select_dtypes(include='number').columns.tolist()
        if len(numeric_cols) > 0:
            selected_col = numeric_cols[0]
        else:
            selected_col = cols[0]

    ascending = sort_order == "asc"
    plot_df = df.copy()

    try:
        plot_df = plot_df.sort_values(by=selected_col, ascending=ascending)
    except Exception:
        pass

    x_col = None
    for col in cols:
        if col != selected_col:
            x_col = col
            break

    numeric_cols = df.select_dtypes(include='number').columns.tolist()

    if selected_col in numeric_cols:
        if x_col is not None:
            fig = px.bar(plot_df, x=x_col, y=selected_col, title=selected_col)
        else:
            plot_df = plot_df.reset_index()
            fig = px.bar(plot_df, x="index", y=selected_col, title=selected_col)
    else:
        value_counts = plot_df[selected_col].value_counts().reset_index()
        value_counts.columns = [selected_col, "count"]
        fig = px.bar(value_counts, x=selected_col, y="count", title=selected_col)

    buttons = [
        html.Button(
            col,
            id={"type": "col-button", "index": col},
            n_clicks=0,
            style={"margin": "4px"}
        )
        for col in cols
    ]

    return html.Div([
        html.H5(filename),
        dcc.Graph(figure=fig),
        html.Div(buttons),
        dcc.RadioItems(
            id="sort-order",
            options=[
                {"label": "Ascending", "value": "asc"},
                {"label": "Descending", "value": "desc"}
            ],
            value=sort_order,
            inline=True
        )
    ])

@callback(
    Output("stored-data", "data"),
    Output("stored-filename", "data"),
    Output("selected-column", "data"),
    Output("output", "children"),
    Input("graphSource", "contents"),
    State("graphSource", "filename")
)
def update_output(contents, filename):
    if contents is None:
        return None, None, None, ""

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            df = pd.read_excel(io.BytesIO(decoded))
        else:
            return None, None, None, html.Div([
                'There was an error processing this file.'
            ])
    except Exception as e:
        print(e)
        return None, None, None, html.Div([
            'There was an error processing this file.'
        ])

    cols = df.columns.tolist()
    numeric_cols = df.select_dtypes(include='number').columns.tolist()

    if len(numeric_cols) > 0:
        default_col = numeric_cols[0]
    elif len(cols) > 0:
        default_col = cols[0]
    else:
        default_col = None

    return (
        df.to_dict("records"),
        filename,
        default_col,
        createGraph(df, filename, default_col, "asc")
    )

@callback(
    Output("output", "children", allow_duplicate=True),
    Output("selected-column", "data", allow_duplicate=True),
    Input({"type": "col-button", "index": ALL}, "n_clicks"),
    Input("sort-order", "value"),
    State("stored-data", "data"),
    State("stored-filename", "data"),
    State("selected-column", "data"),
    prevent_initial_call=True
)
def update_graph(button_clicks, sort_order, data, filename, current_col):
    if data is None:
        return "", current_col

    df = pd.DataFrame(data)
    selected_col = current_col

    if isinstance(ctx.triggered_id, dict) and ctx.triggered_id.get("type") == "col-button":
        selected_col = ctx.triggered_id["index"]

    return createGraph(df, filename, selected_col, sort_order), selected_col

if __name__ == "__main__":
    app.run(debug=True)
