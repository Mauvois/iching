import dash
from dash import html, dcc, Input, Output, State

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Input(id='input-box', type='text', debounce=True,
              placeholder='Enter a value', value=''),
    html.Button('Submit', id='button', n_clicks=0),
    html.Div(id='output')
])


@app.callback(
    Output('output', 'children'),
    Input('button', 'n_clicks'),
    Input('input-box', 'n_submit'),
    State('input-box', 'value')
)
def update_output(n_clicks, n_submit, value):
    print("Callback triggered")
    print(f"n_clicks: {n_clicks}, n_submit: {n_submit}, value: {value}")

    n_clicks = n_clicks or 0
    n_submit = n_submit or 0

    if (n_clicks > 0 or n_submit > 0) and value:
        return f'Input submitted: {value}'
    return 'No input submitted'


if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
