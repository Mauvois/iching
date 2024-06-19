import requests
import re
import time
from dash import Input, Output, State, callback_context
from .utils import start_timer, stop_timer, process_line, get_hexagram, get_interpretation, render_hexagram_line
from .config import BACKEND_API_URL

# Define global variables
start_time = None
stop_times = []
lines = []
random_state = None


def register_callbacks(app):

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
            response = requests.post(
                f"{BACKEND_API_URL}/initialize-toss", json={"text": question})
            if response.status_code == 200:
                random_state = response.json().get("random_state")
                lines.clear()
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
                            stop_times.clear()
                            if len(lines) == 6:
                                hexagram = get_hexagram()
                                hexagram_lines = [render_hexagram_line(
                                    line) for line in lines[::-1]]
                                hexagram_details = [
                                    html.Br(),
                                    html.Div(className='hexagram-title',
                                             children=f"Hexagramme {hexagram[0]} — {hexagram[1]} "),
                                    html.Br(),
                                    html.Div(className='hexagram-section',
                                             children=f"{hexagram[4]}"),
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
        Output('line-output', 'children'),
        Output('hexagram-output', 'children'),
        Output('start-timer-btn', 'style'),
        Output('stop-timer1-btn', 'style'),
        Output('stop-timer2-btn', 'style'),
        Output('stop-timer3-btn', 'style'),
        Output('generate-6-lines-title', 'style'),
        Output('line-type-output', 'style'),
        Input('timer-output', 'children')
    )
    def update_display(timer_output):
        global lines
        line_recap = ""
        hexagram_output = ""
        hexagram_lines = []
        line_type_output = timer_output

        if len(lines) > 0:
            hexagram_lines = [render_hexagram_line(
                line) for line in lines[::-1]]
            line_recap = html.Div(children=[html.Div(
                f"{i+1}: {line}") for i, line in enumerate(lines)], className='my-3')

        hexagram_details = []
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
                    *[html.Div(className='hexagram-section', children=f"{detail}") for detail in hexagram[5:]]
                ]
                hexagram_output = html.Div(
                    children=hexagram_lines + hexagram_details, className='container hexagram-details')
            else:
                hexagram_output = html.Div(
                    "Error fetching hexagram details", className='alert alert-danger')

            button_style = {'display': 'none'}
            title_style = {'display': 'none'}
            line_type_style = {'display': 'none'}
        else:
            button_style = {'display': 'inline-block'}
            title_style = {'display': 'block'}
            line_type_style = {'display': 'block'}

        return line_recap, hexagram_output, button_style, button_style, button_style, button_style, title_style, line_type_style

    @app.callback(
        Output('interpretation-output', 'children'),
        Input('get-interpretation-btn', 'n_clicks'),
        [State('question-input', 'value'),
         State('hexagram-output', 'children')]
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
                        texts.extend(extract_text(
                            children['props']['children']))
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

        return ""
