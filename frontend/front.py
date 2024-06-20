import os
import dash
from dash import html, dcc, Input, Output, State, callback_context
import requests
import time
import re
from styles import external_stylesheets, index_string

# Backend API URL (Update this URL after deploying the backend)
BACKEND_API_URL = os.environ.get(
    "BACKEND_API_URL", "https://backend-5ols2im5la-ew.a.run.app")
INTERPRETATION_API_URL = os.environ.get(
    "INTERPRETATION_API_URL", "https://interpretation-5ols2im5la-ew.a.run.app")

# Initialize the Dash app with a theme and custom font
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.index_string = index_string

# Commonly used styles
HIDDEN = {'display': 'none'}
VISIBLE = {'display': 'block'}
BUTTON_STYLE = {'display': 'inline-block'}

app.layout = html.Div([
    html.Div(id='part-1', children=[
        html.Div('Quelle est votre question pour l\'Oracle?',
                 className='question-label'),
        dcc.Input(id='question-input', type='text', debounce=True,
                  placeholder='', className='form-control my-3', value=''),
        html.Button('', id='submit-question-btn', n_clicks=0,
                    className='btn btn-transparent my-3')
    ], className="container"),

    html.Div(id='part-2', children=[
        html.Div(id='question-display', className='question-display my-3'),
        html.H3("Lancez les 3 pièces 6 fois", id='generate-6-lines-title',
                className="mt-5 text-primary"),
        html.Button('Alea Jacta Est', id='start-timer-btn',
                    n_clicks=0, className='btn btn-success my-3'),
        html.Div(id='timer-output', className='alert alert-info'),
        html.Div([
            html.Button('Pièce n°1', id='stop-timer1-btn',
                        n_clicks=0, className='btn btn-danger mr-2'),
            html.Button('Pièce n°2', id='stop-timer2-btn',
                        n_clicks=0, className='btn btn-danger mr-2'),
            html.Button('Pièce n°3', id='stop-timer3-btn',
                        n_clicks=0, className='btn btn-danger')
        ], className='my-3'),
        html.Div(id='line-output', className='alert alert-info line-recap'),
        html.Div(id='line-type-output', className='line-type')
    ], className="container", style=HIDDEN),

    html.Div(id='part-3', children=[
        html.Div(id='question-display-3', className='question-display my-3'),
        html.Div(id='hexagram-output', className="container my-5"),
        html.H3("Interpretation", className="mt-5 text-primary"),
        html.Button('Get Interpretation', id='get-interpretation-btn',
                    n_clicks=0, className='btn btn-info my-3'),
        html.Div(id='interpretation-output',
                 className='alert alert-warning', children='holi')
    ], className="container", style=HIDDEN)
])

# Define global variables
start_time = None
stop_times = []
lines = []
random_state = None

# Helper functions


def api_request(url, json_data):
    response = requests.post(url, json=json_data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.json().get('detail')}


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


def process_line():
    global stop_times, lines, random_state
    result = api_request(f"{BACKEND_API_URL}/generate-line",
                         {"times": stop_times, "random_state": random_state})
    if "error" not in result:
        lines.append(result['line_sum'])
        return f"{result['line_type']}, {result['line_sum']}"
    return f"Error: {result['error']}"


def get_hexagram():
    result = api_request(
        f"{BACKEND_API_URL}/get-hexagram", {"line_values": lines})
    if "error" not in result:
        return result['hexagram']
    return None


def render_hexagram_line(line_value):
    return html.Div(className='hexagram-line solid' if line_value % 2 else 'hexagram-line broken')


def get_interpretation(question, iching_response):
    result = api_request(f"{INTERPRETATION_API_URL}/interpret",
                         {"question": question, "iching_response": iching_response})
    if "error" not in result:
        return result['interpretation']
    return f"Error: {result['error']}"

# Callbacks


@app.callback(
    Output('part-1', 'style'),
    Output('part-2', 'style'),
    Output('part-3', 'style'),
    Output('question-display', 'children'),
    Output('question-display-3', 'children'),
    Input('submit-question-btn', 'n_clicks'),
    Input('question-input', 'n_submit'),
    State('question-input', 'value')
)
def submit_question(n_clicks, n_submit, question):
    global random_state
    n_clicks = n_clicks or 0
    n_submit = n_submit or 0
    if (n_clicks > 0 or n_submit > 0) and question:
        result = api_request(
            f"{BACKEND_API_URL}/initialize-toss", {"text": question})
        if "error" not in result:
            random_state = result.get("random_state")
            lines.clear()
            return HIDDEN, VISIBLE, HIDDEN, f"{question}", f"Question: {question}"
        return VISIBLE, HIDDEN, HIDDEN, f"Error: {result['error']}", ""
    return VISIBLE, HIDDEN, HIDDEN, "", ""


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
            index = int(re.search(r'stop-timer(\d+)-btn',
                        button_id).group(1)) - 1
            elapsed_time = stop_timer(index)
            if elapsed_time is not None:
                if len(stop_times) == 3:
                    result = process_line()
                    stop_times.clear()
                    if len(lines) == 6:
                        hexagram = get_hexagram()
                        hexagram_lines = [render_hexagram_line(
                            line) for line in lines[::-1]]
                        hexagram_details = [
                            html.Br(),
                            html.Div(
                                className='hexagram-title', children=f"Hexagramme {hexagram[0]} — {hexagram[1]} "),
                            html.Br(),
                            html.Div(className='hexagram-section',
                                     children=f"{hexagram[4]}"),
                            *[html.Div(className='hexagram-section',
                                       children=f"{detail}") for detail in hexagram[5:]],
                            html.Button('Get Interpretation', id='get-interpretation-btn',
                                        n_clicks=0, className='btn btn-info my-3'),
                            # Add 'holi' here
                            html.Div(id='interpretation-output',
                                     className='alert alert-warning', children='holi')
                        ]
                        hexagram_output = html.Div(
                            children=hexagram_lines + hexagram_details, className='container hexagram-details')
                        return result, hexagram_output
                    return result, ""
                return f" {index + 1}e fois", ""
        except (IndexError, ValueError) as e:
            return f"Error processing timer: {str(e)}", ""

    return "", ""


@app.callback(
    Output('line-output', 'children'),
    Output('hexagram-output', 'children'),
    Output('start-timer-btn', 'style'),
    Output('stop-timer1-btn', 'style'),
    Output('stop-timer2-btn', 'style'),
    Output('stop-timer3-btn', 'style'),
    Output('generate-6-lines-title', 'style'),
    Output('line-type-output', 'style'),
    Output('get-interpretation-btn', 'style'),
    Input('timer-output', 'children')
)
def update_display(timer_output):
    global lines
    line_recap = ""
    hexagram_output = ""
    hexagram_lines = []
    line_type_output_style = HIDDEN  # Initialize the line type style to hidden
    button_style = HIDDEN  # Initialize the button style to hidden
    # Initialize the interpretation button style to hidden
    interpretation_button_style = HIDDEN

    if len(lines) > 0:
        hexagram_lines = [render_hexagram_line(line) for line in lines[::-1]]
        line_recap = html.Div(children=[html.Div(
            f"{i+1}: {line}") for i, line in enumerate(lines)], className='my-3')

    if len(lines) == 6:
        hexagram = get_hexagram()
        if hexagram:
            hexagram_details = [
                html.Div(className='hexagram-detail',
                         children=f"Hexagram Number: {hexagram[0]}"),
                html.Div(className='hexagram-detail',
                         children=f"Name: {hexagram[1]}"),
                html.Div(className='hexagram-section',
                         children=f"Judgment: {hexagram[4]}"),
                *[html.Div(className='hexagram-section',
                           children=f"{detail}") for detail in hexagram[5:]],
            ]
            hexagram_output = html.Div(
                children=hexagram_lines + hexagram_details, className='container hexagram-details')
            # Show interpretation button when hexagram details are displayed
            interpretation_button_style = VISIBLE
        else:
            hexagram_output = html.Div(
                "Error fetching hexagram details", className='alert alert-danger')

        button_style = HIDDEN  # Hide timer buttons when hexagram is complete
        title_style = HIDDEN
        line_type_output_style = HIDDEN  # Ensure line type is hidden
    else:
        button_style = BUTTON_STYLE
        title_style = VISIBLE
        line_type_output_style = VISIBLE  # Show line type when not complete

    return line_recap, hexagram_output, button_style, button_style, button_style, button_style, title_style, line_type_output_style, interpretation_button_style  # Update return statement



@app.callback(
    Output('interpretation-output', 'children'),
    Input('get-interpretation-btn', 'n_clicks'),
    [State('question-input', 'value'), State('hexagram-output', 'children')]
)
def provide_interpretation(n_clicks, question, hexagram_output):
    if n_clicks > 0 and question and hexagram_output:
        iching_response_parts = []

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

        if not iching_response:
            return "Error: Invalid I Ching response format."

        interpretation = get_interpretation(question, iching_response)
        return interpretation

    return "holi"


# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(debug=True, host='0.0.0.0', port=port)
