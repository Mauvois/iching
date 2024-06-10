# Import necessary libraries
import dash
from dash import html, dcc, Input, Output, State, callback_context
import requests
import time
import re

# Initialize the Dash app with a theme and custom font
app = dash.Dash(__name__, external_stylesheets=[
    'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css',
    'https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap'
])

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>I Ching</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                font-family: 'Lato', sans-serif;
            }
            .hexagram-line {
                height: 10px;
                margin: 5px 0;
            }
            .hexagram-line.solid {
                background-color: black;
            }
            .hexagram-line.broken {
                background: linear-gradient(to right, black 40%, white 40%, white 60%, black 60%);
            }
        </style>
    </head>
    <body>
        <nav class="navbar navbar-expand-lg navbar-light bg-primary">
            <a class="navbar-brand text-white" href="#">I Ching</a>
        </nav>
        {%app_entry%}
        <footer class="text-center mt-4">
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div([

    html.Div([
        html.Div([
            # html.H3("Step 1: Initialize Toss", className="mt-5 text-primary"),
            dcc.Input(id='question-input', type='text', placeholder='Enter your question:', className='form-control my-3'),
            html.Button('Initialize Toss', id='init-toss-btn', n_clicks=0, className='btn btn-success my-3'),
            html.Div(id='random-state-output', className='alert alert-info')
        ], className="container mb-4"),

        html.Div([
            html.H3("Generate 6 Lines", className="mt-5 text-primary"),
            html.Button('Start Timer', id='start-timer-btn', n_clicks=0, className='btn btn-success my-3'),
            html.Div(id='timer-output', className='alert alert-info'),
            html.Div([
                html.Button('Stop Timer 1', id='stop-timer1-btn', n_clicks=0, className='btn btn-danger mr-2'),
                html.Button('Stop Timer 2', id='stop-timer2-btn', n_clicks=0, className='btn btn-danger mr-2'),
                html.Button('Stop Timer 3', id='stop-timer3-btn', n_clicks=0, className='btn btn-danger')
            ], className='my-3'),
            html.Div(id='line-output', className='alert alert-info'),
            html.Button('Clear', id='clear-btn', n_clicks=0, className='btn btn-primary my-3')
        ], className="container mb-4")
    ], className="container"),

    html.Div(id='hexagram-output', className="container my-5")
])

# Define the base URL of your API
BASE_URL = "http://localhost:8000"

# Define global variables
start_time = None
stop_times = []
lines = []
random_state = None

# Helper functions
def start_timer():
    global start_time, stop_times
    start_time = time.time()
    stop_times = []

def stop_timer(index):
    global start_time, stop_times
    if start_time is not None:
        elapsed_time = int((time.time() - start_time) * 1000)
        if len(stop_times) < index + 1:
            stop_times.append(elapsed_time)
        else:
            stop_times[index] = elapsed_time
        return elapsed_time

def process_line(random_state):
    global stop_times, lines
    response = requests.post(
        f"{BASE_URL}/generate-line",
        json={"times": stop_times, "random_state": random_state}
    )
    if response.status_code == 200:
        result = response.json()
        lines.append(result['line_sum'])
        return f"Line Type: {result['line_type']}, Line Sum: {result['line_sum']}"
    else:
        return f"Error: {response.json().get('detail')}"

def get_hexagram():
    response = requests.post(
        f"{BASE_URL}/get-hexagram", json={"line_values": lines}
    )
    if response.status_code == 200:
        hexagram = response.json().get("hexagram")
        return hexagram
    else:
        return None

def render_hexagram_line(line_value):
    if line_value % 2 == 0:  # Yin line (broken)
        return html.Div(className='hexagram-line broken')
    else:  # Yang line (solid)
        return html.Div(className='hexagram-line solid')

# Callbacks
@app.callback(
    Output('random-state-output', 'children'),
    Input('init-toss-btn', 'n_clicks'),
    State('question-input', 'value')
)
def initialize_toss(n_clicks, question):
    global random_state
    if n_clicks > 0 and question:
        response = requests.post(f"{BASE_URL}/initialize-toss", json={"text": question})
        if response.status_code == 200:
            random_state = response.json().get("random_state")
            lines.clear()  # Reset lines
            return f"Random State: {random_state}"
        else:
            return f"Error: {response.json().get('detail')}"
    return ""

@app.callback(
    Output('timer-output', 'children'),
    [Input('start-timer-btn', 'n_clicks'),
     Input('stop-timer1-btn', 'n_clicks'),
     Input('stop-timer2-btn', 'n_clicks'),
     Input('stop-timer3-btn', 'n_clicks')],
    State('random-state-output', 'children')
)
def manage_timers(start_clicks, stop1_clicks, stop2_clicks, stop3_clicks, random_state_text):
    global stop_times
    ctx = callback_context

    if not ctx.triggered:
        return ""

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if button_id == 'start-timer-btn':
        start_timer()
        return "Timer started"

    if 'stop-timer' in button_id:
        try:
            match = re.search(r'stop-timer(\d+)-btn', button_id)
            if match:
                index = int(match.group(1)) - 1
                elapsed_time = stop_timer(index)
                if elapsed_time is not None:
                    if len(stop_times) == 3:
                        random_state_value = int(random_state_text.split(":")[1].strip())
                        result = process_line(random_state_value)
                        stop_times.clear()  # Clear stop_times after processing the line
                        return result
                    return f"Timer stopped {index + 1} times: {elapsed_time} ms"
            else:
                return "Error processing timer: Invalid button ID format"
        except (IndexError, ValueError) as e:
            return f"Error processing timer: {str(e)}"

    return ""

@app.callback(
    [Output('line-output', 'children'),
     Output('hexagram-output', 'children')],
    [Input('clear-btn', 'n_clicks'),
     Input('timer-output', 'children')],
    State('random-state-output', 'children')
)
def update_display(clear_clicks, timer_output, random_state_text):
    global lines
    ctx = callback_context

    if ctx.triggered and ctx.triggered[0]['prop_id'].split('.')[0] == 'clear-btn':
        lines = []
        return "State cleared, ready for new session.", ""

    line_recap = ""
    hexagram_output = ""
    hexagram_lines = []

    if len(lines) > 0:
        hexagram_lines = [render_hexagram_line(line) for line in lines[::-1]]
        line_recap = html.Div(children=[html.Div(f"{i+1}: {line}") for i, line in enumerate(lines)], className='my-3')

    hexagram_details = []
    if len(lines) == 6:
        hexagram = get_hexagram()
        if hexagram:
            hexagram_details = [
                html.Div(className='hexagram-title text-danger', children=hexagram[1]),
                html.Div(className='hexagram-detail', children=f"Hexagram Number: {hexagram[0]}"),
                html.Div(className='hexagram-detail', children=f"Name: {hexagram[1]}"),
                html.Div(className='hexagram-detail', children=f"Upper Trigram: {hexagram[2]}"),
                html.Div(className='hexagram-detail', children=f"Lower Trigram: {hexagram[3]}"),
                html.Div(className='hexagram-section bg-light', children=f"Judgment: {hexagram[4]}"),
                *[html.Div(className='hexagram-section bg-light', children=f"{detail}") for detail in hexagram[5:]]
            ]
            hexagram_output = html.Div(children=hexagram_lines + hexagram_details, className='container hexagram-details')
        else:
            hexagram_output = html.Div("Error fetching hexagram details", className='alert alert-danger')

    return line_recap, hexagram_output

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
