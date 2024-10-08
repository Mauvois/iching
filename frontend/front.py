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

app.layout = html.Div([
    html.Div(id='part-1', className="part-1", children=[
        html.Div('Quelle est votre question pour l\'Oracle?',
                 className='question-label'),
        dcc.Input(id='question-input', type='text', debounce=True,
                  placeholder='', className='form-control'),
        html.Button('', id='submit-question-btn', n_clicks=0,
                    className='btn btn-transparent')
    ]),

    html.Div(id='part-2', className="part-2 hidden", children=[
        html.Div(id='question-display', className='question-display'),
        html.H3("Lancez les 3 pièces 6 fois", id='generate-6-lines-title',
                className="text-primary"),
        html.Button('Alea Jacta Est', id='start-timer-btn',
                    n_clicks=0, className='btn btn-start'),
        html.Div(id='timer-output', className='info-box'),
        html.Div([
            html.Button('Pièce n°1', id='stop-timer1-btn',
                        n_clicks=0, className='btn btn-stop'),
            html.Button('Pièce n°2', id='stop-timer2-btn',
                        n_clicks=0, className='btn btn-stop'),
            html.Button('Pièce n°3', id='stop-timer3-btn',
                        n_clicks=0, className='btn btn-stop'),
        ], className='button-group'),
        html.Div(id='line-output', className='info-box line-recap'),
        html.Div(id='line-type-output', className='line-type')
    ]),

    html.Div(id='part-3', className="part-3 hidden", children=[
        html.Div(id='question-display-3', className='question-display'),
        html.Div(id='hexagram-output', className="container my-5"),
        html.H3("Interpretation", className="text-primary"),
        html.Div(className='center', children=[
            html.Button('Get Interpretation', id='get-interpretation-btn',
                        n_clicks=0, className='btn btn-interpret')
        ]),
        html.Div(id='interpretation-output',
                 className='info-box', children='holi')
    ])
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

# Callbacks


@app.callback(
    Output('part-1', 'className'),
    Output('part-2', 'className'),
    Output('part-3', 'className'),
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
            return 'part-1 hidden', 'part-2', 'part-3 hidden', f"{question}", f"Question: {question}"
        return 'part-1', 'part-2 hidden', 'part-3 hidden', f"Error: {result['error']}", ""
    return 'part-1', 'part-2 hidden', 'part-3 hidden', "", ""


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
        return "Le sort est lancé"

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
                            html.Div(className='center', children=[
                                html.Button('Get Interpretation', id='get-interpretation-btn',
                                            n_clicks=0, className='btn btn-interpret')
                            ]),
                            html.Div(id='interpretation-output',
                                     className='info-box', children='holi')
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
    # Initialize the line type style to hidden
    line_type_output_style = {'display': 'none'}
    button_style = {'display': 'none'}  # Initialize the button style to hidden
    # Initialize the interpretation button style to hidden
    interpretation_button_style = {'display': 'none'}

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
            interpretation_button_style = {'display': 'block'}
        else:
            hexagram_output = html.Div(
                "Error fetching hexagram details", className='error-box')

        # Hide timer buttons when hexagram is complete
        button_style = {'display': 'none'}
        title_style = {'display': 'none'}
        # Ensure line type is hidden
        line_type_output_style = {'display': 'none'}
    else:
        button_style = {'display': 'inline-block'}
        title_style = {'display': 'block'}
        # Show line type when not complete
        line_type_output_style = {'display': 'block'}

    return line_recap, hexagram_output, button_style, button_style, button_style, button_style, title_style, line_type_output_style, interpretation_button_style  # Update return statement


@app.callback(
    Output('interpretation-output', 'children'),
    Input('get-interpretation-btn', 'n_clicks'),
    [State('question-input', 'value'), State('hexagram-output', 'children')]
)
def provide_interpretation(n_clicks, question, hexagram_output):
    if n_clicks > 0 and question and hexagram_output:
        iching_response_parts = extract_text(hexagram_output)

        # Extract judgment and all traits from iching_response_parts
        judgment = ""
        traits = []
        for part in iching_response_parts:
            if "Hexagram Number" in part:
                continue  # Skip hexagram number
            elif "Judgment" in part:
                judgment = part.split("Judgment: ")[-1]
            else:
                traits.append(part)

        # Ensure that extracted judgment and traits are valid
        if not judgment:
            return "Error: Invalid I Ching response format."

        print(f"Extracted Judgment: {judgment}")
        print(f"Extracted Traits: {traits}")
        print(f"Lines: {lines}")

        # Mapping from line values to French words
        line_to_word = {
            6: 'six',
            7: 'sept',
            8: 'huit',
            9: 'neuf'
        }

        # Positions in French for matching
        positions = [
            "au commencement",
            "à la deuxième place",
            "à la troisième place",
            "à la quatrième place",
            "à la cinquième place",
            "en haut"
        ]

        # Filter traits based on the drawn lines
        filtered_traits = []
        for i, line in enumerate(lines):
            line_word = line_to_word.get(line, "")
            position = positions[i]
            print(
                f"Processing line {i+1} with value {line} ({line_word}) at position {position}")
            for trait in traits:
                trait_cleaned = trait.lower().strip()  # Clean the trait
                line_word_cleaned = line_word.lower().strip()  # Clean the line word
                position_cleaned = position.lower().strip()  # Clean the position

                if line_word_cleaned in trait_cleaned and position_cleaned in trait_cleaned:
                    filtered_traits.append(trait)
                    print(f"Matched Trait: {trait}")
                    break
                else:
                    print(
                        f"No match for line {i+1} with value {line_word_cleaned} at position {position_cleaned} in trait: {trait_cleaned}")

        print(f"Filtered Traits: {filtered_traits}")

        # Use only the judgment if no matching traits are found
        if not filtered_traits:
            iching_response = f"Judgment: {judgment}"
        else:
            iching_response = f"Judgment: {judgment} " + \
                " ".join(filtered_traits)

        print(f"Formatted I Ching Response: {iching_response}")

        interpretation = get_interpretation(question, iching_response)
        print(f"Interpretation Result: {interpretation}")

        return interpretation

    return ""


# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(debug=True, host='0.0.0.0', port=port)
