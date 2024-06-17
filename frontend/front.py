import os
import dash
from dash import html, dcc, Input, Output, State, callback_context
import requests
import time
import re

# Backend API URL (Update this URL after deploying the backend)
BACKEND_API_URL = "https://backend-5ols2im5la-ew.a.run.app"
INTERPRETATION_API_URL = "https://interpretation-5ols2im5la-ew.a.run.app"

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
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                background-image: url('/assets/felipe-santana--e_njRV9hRE-unsplash.jpg');
                background-size: cover;
                background-position: center;
                color: white; /* Turn body text white */
            }
            .container {
                background-color: rgba(255, 255, 255, 0);
                padding: 20px;
                border-radius: 8px;
                max-width: 600px;
                text-align: center;
                box-shadow: 0 0px 8px rgba(0, 0, 0, 0);
                color: white; /* Turn container text white */
            }
            .hexagram-line {
                height: 10px;
                margin: 5px 0;
            }
            .hexagram-line.solid {
                background-color: black;
            }
            .hexagram-line.broken {
                background: linear-gradient(to right, black 40%, transparent 40%, transparent 60%, black 60%);
            }
            .alert-info, .alert-warning, .alert-danger {
                background-color: rgba(255, 255, 255, 0);
                border: none;
                color: white; /* Turn alert text white */
            }
            .text-primary {
                color: white !important; /* Change primary text to white */
            }
            .text-center {
                text-align: center !important;
                color: white; /* Turn text center text white */
            }
            .btn {
                margin: 5px;
            }
            .btn-transparent {
                background-color: transparent;
                border: none;
                color: white; /* Change button text to white */
            }
            .question-label {
                color: white;
                font-size: 1.5em;
                margin-bottom: 10px;
            }
            .form-control::placeholder {
                color: white;
                opacity: 1;
            }
            .form-control {
                background-color: rgba(255, 255, 255, 0);
                color: white;
                border: 1px solid white;
                transition: border-color 0.3s;
            }
            .form-control:focus {
                background-color: rgba(255, 255, 255, 0);
                color: white;
                border: 2px solid white;
                outline: none;
            }
            .question-display {
                color: white;
                font-size: 2em;
                margin-top: 20px;
                text-align: center;
            }
            .hexagram-title {
                color: white; /* Turn hexagram title text white */
            }
            .hexagram-detail {
                color: white; /* Turn hexagram detail text white */
            }
            .hexagram-section {
                color: white; /* Turn hexagram section text white */
            }
        </style>
    </head>
    <body>
        <div class="container">
            {%app_entry%}
            <footer class="text-center mt-4">
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </div>
    </body>
</html>
'''

app.layout = html.Div([

    # Part 1: Ask Question
    html.Div(id='part-1', children=[
        html.Div('Quelle est votre question pour l\'Oracle?',
                 className='question-label'),
        dcc.Input(id='question-input', type='text', debounce=True,
                  placeholder='', className='form-control my-3'),
        html.Button('', id='submit-question-btn',
                    n_clicks=0, className='btn btn-transparent my-3')  #
    ], className="container"),


    # Part 2: Initialize Toss and Generate Lines (Initially Hidden)
    html.Div(id='part-2', children=[
        # Updated className
        html.Div(id='question-display', className='question-display my-3'),
        html.H3("Generate 6 Lines", className="mt-5 text-primary"),
        html.Button('Start Timer', id='start-timer-btn',
                    n_clicks=0, className='btn btn-success my-3'),
        html.Div(id='timer-output', className='alert alert-info'),
        html.Div([
            html.Button('Stop Timer 1', id='stop-timer1-btn',
                        n_clicks=0, className='btn btn-danger mr-2'),
            html.Button('Stop Timer 2', id='stop-timer2-btn',
                        n_clicks=0, className='btn btn-danger mr-2'),
            html.Button('Stop Timer 3', id='stop-timer3-btn',
                        n_clicks=0, className='btn btn-danger')
        ], className='my-3'),
        html.Div(id='line-output', className='alert alert-info'),
        html.Button('Clear', id='clear-btn', n_clicks=0,
                    className='btn btn-primary my-3')
    ], className="container", style={'display': 'none'}),

    # Part 3: Display Hexagram and Interpretation (Initially Hidden)
    html.Div(id='part-3', children=[
        # Added for part 3
        html.Div(id='question-display-3', className='question-display my-3'),
        html.Div(id='hexagram-output', className="container my-5"),
        html.H3("Interpretation", className="mt-5 text-primary"),
        html.Button('Get Interpretation', id='get-interpretation-btn',
                    n_clicks=0, className='btn btn-info my-3'),
        html.Div(id='interpretation-output', className='alert alert-warning')
    ], className="container", style={'display': 'none'})

])


# Define the base URL of your API
BASE_URL = BACKEND_API_URL

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


def get_interpretation(question, iching_response):
    response = requests.post(
        f"{INTERPRETATION_API_URL}/interpret",
        json={"question": question, "iching_response": iching_response}
    )
    if response.status_code == 200:
        interpretation = response.json().get("interpretation")
        return interpretation
    else:
        return f"Error: {response.json().get('detail')}"


# Callbacks
@app.callback(
    Output('part-1', 'style'),
    Output('part-2', 'style'),
    Output('part-3', 'style'),  # Added to toggle part-3
    Output('question-display', 'children'),
    Output('question-display-3', 'children'),  # Added for part 3
    Input('submit-question-btn', 'n_clicks'),
    Input('question-input', 'n_submit'),  # Added n_submit input
    State('question-input', 'value')
)
def submit_question(n_clicks, n_submit, question):
    global random_state
    n_clicks = n_clicks or 0
    n_submit = n_submit or 0
    if (n_clicks > 0 or n_submit > 0) and question:
        response = requests.post(
            f"{BASE_URL}/initialize-toss", json={"text": question})
        if response.status_code == 200:
            random_state = response.json().get("random_state")
            lines.clear()  # Reset lines
            return {'display': 'none'}, {'display': 'block'}, {'display': 'none'}, f"{question}", f"Question: {question}"
        else:
            return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}, f"Error: {response.json().get('detail')}", ""
    return {'display': 'block'}, {'display': 'none'}, {'display': 'none'}, "", ""


@app.callback(
    Output('timer-output', 'children'),
    [Input('start-timer-btn', 'n_clicks'),
     Input('stop-timer1-btn', 'n_clicks'),
     Input('stop-timer2-btn', 'n_clicks'),
     Input('stop-timer3-btn', 'n_clicks')]
)
def manage_timers(start_clicks, stop1_clicks, stop2_clicks, stop3_clicks):
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
                        result = process_line(random_state)
                        stop_times.clear()  # Clear stop_times after processing the line
                        if len(lines) == 6:  # Check if 6 lines are drawn
                            hexagram = get_hexagram()
                            hexagram_lines = [render_hexagram_line(
                                line) for line in lines[::-1]]
                            hexagram_details = [
                                html.Div(
                                    className='hexagram-title text-danger', children=hexagram[1]),
                                html.Div(className='hexagram-detail',
                                         children=f"Hexagram Number: {hexagram[0]}"),
                                html.Div(className='hexagram-detail',
                                         children=f"Name: {hexagram[1]}"),
                                html.Div(className='hexagram-detail',
                                         children=f"Upper Trigram: {hexagram[2]}"),
                                html.Div(className='hexagram-detail',
                                         children=f"Lower Trigram: {hexagram[3]}"),
                                html.Div(className='hexagram-section',
                                         children=f"Judgment: {hexagram[4]}"),
                                *[html.Div(className='hexagram-section', children=f"{detail}") for detail in hexagram[5:]]
                            ]
                            hexagram_output = html.Div(
                                children=hexagram_lines + hexagram_details, className='container hexagram-details')
                            return result, hexagram_output
                        return result, ""
                    return f"Timer stopped {index + 1} times: {elapsed_time} ms", ""
            else:
                return "Error processing timer: Invalid button ID format", ""
        except (IndexError, ValueError) as e:
            return f"Error processing timer: {str(e)}", ""

    return "", ""


@app.callback(
    [Output('line-output', 'children'),
     Output('hexagram-output', 'children')],
    [Input('clear-btn', 'n_clicks'),
     Input('timer-output', 'children')]
)
def update_display(clear_clicks, timer_output):
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
        line_recap = html.Div(children=[html.Div(
            f"{i+1}: {line}") for i, line in enumerate(lines)], className='my-3')

    hexagram_details = []
    if len(lines) == 6:
        hexagram = get_hexagram()
        if (hexagram):
            hexagram_details = [
                html.Div(className='hexagram-title text-danger',
                         children=hexagram[1]),
                html.Div(className='hexagram-detail',
                         children=f"Hexagram Number: {hexagram[0]}"),
                html.Div(className='hexagram-detail',
                         children=f"Name: {hexagram[1]}"),
                html.Div(className='hexagram-detail',
                         children=f"Upper Trigram: {hexagram[2]}"),
                html.Div(className='hexagram-detail',
                         children=f"Lower Trigram: {hexagram[3]}"),
                html.Div(className='hexagram-section',
                         children=f"Judgment: {hexagram[4]}"),
                *[html.Div(className='hexagram-section', children=f"{detail}") for detail in hexagram[5:]]
            ]
            hexagram_output = html.Div(
                children=hexagram_lines + hexagram_details, className='container hexagram-details')
        else:
            hexagram_output = html.Div(
                "Error fetching hexagram details", className='alert alert-danger')

    return line_recap, hexagram_output


@app.callback(
    Output('interpretation-output', 'children'),
    Input('get-interpretation-btn', 'n_clicks'),
    [State('question-input', 'value'), State('hexagram-output', 'children')]
)
def provide_interpretation(n_clicks, question, hexagram_output):
    if n_clicks > 0 and question and hexagram_output:
        iching_response_parts = []

        # Extract text from hexagram_output
        def extract_text(children):
            texts = []
            if isinstance(children, list):
                for child in children:
                    texts.extend(extract_text(child))
            elif isinstance(children, dict):
                if 'props' in children and 'children' in children['props']:
                    texts.extend(extract_text(children['props']['children']))
                elif 'children' in children:
                    texts.extend(extract_text(children['children']))
            elif isinstance(children, str):
                texts.append(children)
            return texts

        iching_response_parts = extract_text(hexagram_output)
        iching_response = ' '.join(iching_response_parts).strip()

        print(f"Hexagram Output: {hexagram_output}")  # Debugging statement
        print(f"I Ching Response: {iching_response}")  # Debugging statement

        if not iching_response:
            return "Error: Invalid I Ching response format."

        interpretation = get_interpretation(question, iching_response)
        return interpretation

    return ""


# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(debug=True, host='0.0.0.0', port=port)
