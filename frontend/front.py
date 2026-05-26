import os
import dash
from dash import html, dcc, Input, Output, State, callback_context
import requests
import time
import re
import unicodedata
from styles import external_stylesheets, index_string

# Backend API URL (Update this URL after deploying the backend)
BACKEND_API_URL = os.environ.get(
    "BACKEND_API_URL", "http://backend:8080")
INTERPRETATION_API_URL = os.environ.get(
    "INTERPRETATION_API_URL", "http://interpreter:8080")

# Initialize the Dash app with a theme and custom font
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.index_string = index_string

app.layout = html.Div([
    dcc.Store(id='session-store', data={
        "question": "",
        "random_state": None,
        "line_values": [],
        "last_line_type": "",
        "hexagram": None,
        "interpretation_context": "",
        "phase": "idle",
        "draw_id": 0,
        "draw_started": False,
        "piece_stops": [False, False, False],
        "stop_times": [None, None, None],
        "draw_started_at": None
    }),
    html.Div(id='part-1', className="part-1", children=[
        html.Div(className='question-input-shell', children=[
            dcc.Input(id='question-input', type='text', debounce=False,
                      placeholder='', className='form-control'),
            html.Div("Posez votre question a l'Oracle", id='question-ghost', className='question-ghost')
        ]),
        html.Button('Consulter', id='submit-question-btn', n_clicks=0,
                    className='btn btn-submit')
    ]),

    html.Div(id='part-2', className="part-2 hidden", children=[
        html.Div(id='question-display', className='question-display'),
        html.H3("Lancez les 3 pièces 6 fois", id='generate-6-lines-title',
                className="text-primary"),
        html.Button('Alea Jacta Est', id='start-timer-btn',
                     n_clicks=0, className='btn btn-start'),
        html.Div(id='timer-output', className='info-box'),
        html.Div([
            html.Button('1', id='stop-timer1-btn',
                        n_clicks=0, className='btn btn-stop'),
            html.Button('2', id='stop-timer2-btn',
                        n_clicks=0, className='btn btn-stop'),
            html.Button('3', id='stop-timer3-btn',
                        n_clicks=0, className='btn btn-stop'),
        ], className='button-group'),
        html.Div(id='line-output', className='info-box line-recap'),
        html.Div(id='line-type-output', className='line-type')
    ]),

    html.Div(id='part-3', className="part-3 hidden", children=[
        html.Div(id='question-display-3', className='question-display'),
        html.Div(id='hexagram-output', className="container my-5"),
        html.Div(className='center', children=[
            html.Button('Interpretation', id='get-interpretation-btn',
                         n_clicks=0, className='btn btn-interpret')
        ]),
        html.Div(id='interpretation-output',
                 className='info-box', children='')
    ])
])

# Define global variables
lines = []
random_state = None

# Helper functions


def api_request(url, json_data):
    response = requests.post(url, json=json_data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.json().get('detail')}


def process_line(stop_times, random_state):
    global lines
    result = api_request(f"{BACKEND_API_URL}/generate-line",
                         {"times": stop_times, "random_state": random_state})
    if "error" not in result:
        lines.append(result['line_sum'])
        return f"{result['line_type']}, {result['line_sum']}"
    return f"Error: {result['error']}"


def reset_draw_state(session_data):
    session_data["phase"] = "idle"
    session_data["draw_started"] = False
    session_data["piece_stops"] = [False, False, False]
    session_data["stop_times"] = [None, None, None]
    session_data["draw_started_at"] = None


def ensure_session_defaults(session_data):
    session_data.setdefault("phase", "idle")
    session_data.setdefault("draw_id", 0)
    session_data.setdefault("draw_started", False)
    session_data.setdefault("piece_stops", [False, False, False])
    session_data.setdefault("stop_times", [None, None, None])
    session_data.setdefault("draw_started_at", None)
    return session_data


def get_hexagram():
    result = api_request(
        f"{BACKEND_API_URL}/get-hexagram", {"line_values": lines})
    if "error" not in result:
        return result['hexagram']
    return None


def render_hexagram_line(line_value):
    return html.Div(className='hexagram-line solid' if line_value % 2 else 'hexagram-line broken')


def render_annotated_hexagram_lines(line_values, finalized=False):
    position_labels = ["1 (bas)", "2", "3", "4", "5", "6 (haut)"]
    rows = []

    for idx in range(6, 0, -1):
        if idx <= len(line_values):
            value = line_values[idx - 1]
            if finalized:
                is_selected = value in (6, 9)
                line_class = 'hexagram-line-row selected-line' if is_selected else 'hexagram-line-row default-line'
                line_style = 'hexagram-line solid line-selected' if (value % 2 and is_selected) else \
                    'hexagram-line broken line-selected' if ((value % 2 == 0) and is_selected) else \
                    'hexagram-line solid line-default' if value % 2 else 'hexagram-line broken line-default'
            else:
                line_class = 'hexagram-line-row default-line'
                line_style = 'hexagram-line solid line-default' if value % 2 else 'hexagram-line broken line-default'
            meta = f"{position_labels[idx - 1]} - {value}"
        else:
            line_class = 'hexagram-line-row default-line pending-line'
            line_style = 'hexagram-line solid line-pending'
            meta = f"{position_labels[idx - 1]} - -"

        rows.append(html.Div([
            html.Div(className='hexagram-line-wrap', children=[
                html.Div(className=line_style)
            ]),
            html.Div(className='hexagram-line-meta', children=meta)
        ], className=line_class))

    return html.Div(children=rows, className='hexagram-lines-annotated')


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


def build_interpretation_context(line_values, hexagram):
    if not hexagram:
        return ""

    judgment = hexagram[4] if len(hexagram) > 4 else ""
    traits = [trait for trait in list(hexagram[5:]) if trait is not None] if len(hexagram) > 5 else []
    line_to_word = {6: 'six', 7: 'sept', 8: 'huit', 9: 'neuf'}
    positions = [
        "au commencement",
        "a la deuxieme place",
        "a la troisieme place",
        "a la quatrieme place",
        "a la cinquieme place",
        "en haut"
    ]

    def normalize_text(value):
        if value is None:
            return ""
        if not isinstance(value, str):
            value = str(value)
        return ''.join(
            char for char in unicodedata.normalize('NFD', value.lower().strip())
            if unicodedata.category(char) != 'Mn'
        )

    selected_traits = []
    for i, value in enumerate(line_values):
        if value not in (6, 9):
            continue

        line_word = line_to_word[value]
        position = positions[i]
        for trait in traits:
            trait_cleaned = normalize_text(trait)
            if normalize_text(line_word) in trait_cleaned and normalize_text(position) in trait_cleaned:
                selected_traits.append(trait)
                break

    if selected_traits:
        return f"Judgment: {judgment} " + " ".join(selected_traits)
    return f"Judgment: {judgment}"


def render_live_hexagram(line_values):
    return html.Div(
        className='hexagram-live-wrapper',
        children=[render_annotated_hexagram_lines(line_values, finalized=False)]
    )


def render_hexagram_details(hexagram, line_values):
    if not hexagram:
        return html.Div("Error fetching hexagram details", className='error-box')

    hexagram_lines = render_annotated_hexagram_lines(line_values, finalized=True)
    details = [
        html.Div(className='hexagram-detail', children=f"Hexagram Number: {hexagram[0]}"),
        html.Div(className='hexagram-detail', children=f"Name: {hexagram[1]}"),
        html.Div(className='hexagram-section', children=f"Judgment: {hexagram[4]}"),
    ]

    line_to_word = {6: 'six', 7: 'sept', 8: 'huit', 9: 'neuf'}
    positions = [
        "au commencement",
        "a la deuxieme place",
        "a la troisieme place",
        "a la quatrieme place",
        "a la cinquieme place",
        "en haut"
    ]

    def normalize_text(value):
        if value is None:
            return ""
        if not isinstance(value, str):
            value = str(value)
        return ''.join(
            char for char in unicodedata.normalize('NFD', value.lower().strip())
            if unicodedata.category(char) != 'Mn'
        )

    position_map = {
        "au commencement": 1,
        "a la deuxieme place": 2,
        "a la troisieme place": 3,
        "a la quatrieme place": 4,
        "a la cinquieme place": 5,
        "en haut": 6,
    }

    parsed_traits = []
    for detail in hexagram[5:]:
        if detail is None:
            continue
        normalized_detail = normalize_text(detail)
        position_idx = None
        for label, idx in position_map.items():
            if label in normalized_detail:
                position_idx = idx
                break

        is_selected = False
        for idx, line_value in enumerate(line_values):
            if line_value not in (6, 9):
                continue
            if line_to_word[line_value] in normalized_detail and positions[idx] in normalized_detail:
                is_selected = True
                break

        parsed_traits.append({
            "text": detail,
            "selected": is_selected,
            "position": position_idx if position_idx is not None else 0,
        })

    parsed_traits.sort(key=lambda trait: trait["position"], reverse=True)

    for trait in parsed_traits:
        cls = 'hexagram-section selected-trait' if trait["selected"] else 'hexagram-section muted-trait'
        details.append(html.Div(className=cls, children=trait["text"]))

    return html.Div(children=[hexagram_lines] + details, className='container hexagram-details')

# Callbacks


@app.callback(
    Output('part-1', 'className'),
    Output('part-2', 'className'),
    Output('part-3', 'className'),
    Output('question-display', 'children'),
    Output('question-display-3', 'children'),
    Output('session-store', 'data'),
    Input('submit-question-btn', 'n_clicks'),
    Input('question-input', 'n_submit'),
    State('question-input', 'value'),
    State('session-store', 'data')
)
def submit_question(n_clicks, n_submit, question, session_data):
    global random_state
    n_clicks = n_clicks or 0
    n_submit = n_submit or 0
    if (n_clicks > 0 or n_submit > 0) and question:
        result = api_request(
            f"{BACKEND_API_URL}/initialize-toss", {"text": question})
        if "error" not in result:
            random_state = result.get("random_state")
            lines.clear()
            session_data = {
                "question": question,
                "random_state": random_state,
                "line_values": [],
                "last_line_type": "",
                "hexagram": None,
                "interpretation_context": "",
                "phase": "idle",
                "draw_id": 0,
                "draw_started": False,
                "piece_stops": [False, False, False],
                "stop_times": [None, None, None],
                "draw_started_at": None
            }
            return 'part-1 hidden', 'part-2', 'part-3 hidden', f"{question}", f"Question: {question}", session_data
        return 'part-1', 'part-2 hidden', 'part-3 hidden', f"Error: {result['error']}", "", session_data
    return 'part-1', 'part-2 hidden', 'part-3 hidden', "", "", session_data


@app.callback(
    Output('timer-output', 'children'),
    Output('line-output', 'children'),
    Output('hexagram-output', 'children'),
    Output('part-2', 'className', allow_duplicate=True),
    Output('part-3', 'className', allow_duplicate=True),
    Output('session-store', 'data', allow_duplicate=True),
    Input('start-timer-btn', 'n_clicks'),
    Input('stop-timer1-btn', 'n_clicks'),
    Input('stop-timer2-btn', 'n_clicks'),
    Input('stop-timer3-btn', 'n_clicks'),
    State('session-store', 'data'),
    prevent_initial_call=True
)
def manage_timers(start_clicks, stop1_clicks, stop2_clicks, stop3_clicks, session_data):
    global random_state
    ctx = callback_context

    if not ctx.triggered:
        return "", "", "", 'part-2', 'part-3 hidden', session_data

    if not session_data or session_data.get("random_state") is None:
        return "Veuillez poser une question d'abord", "", "", 'part-2', 'part-3 hidden', session_data

    session_data = ensure_session_defaults(session_data)

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    now_ms = int(time.time() * 1000)

    if button_id == 'start-timer-btn':
        if session_data.get("phase") in ("drawing", "resolving") or session_data.get("draw_started"):
            return "Tirage déjà en cours", render_live_hexagram(session_data.get("line_values", [])), "", 'part-2', 'part-3 hidden', session_data
        session_data["draw_id"] = int(session_data.get("draw_id", 0)) + 1
        session_data["phase"] = "drawing"
        session_data["draw_started"] = True
        session_data["piece_stops"] = [False, False, False]
        session_data["stop_times"] = [None, None, None]
        session_data["draw_started_at"] = now_ms
        return "Le sort est lancé", render_live_hexagram(session_data.get("line_values", [])), "", 'part-2', 'part-3 hidden', session_data

    if 'stop-timer' in button_id:
        try:
            if session_data.get("phase") != "drawing" or not session_data.get("draw_started"):
                return "Lancez d'abord Alea Jacta Est", render_live_hexagram(session_data.get("line_values", [])), "", 'part-2', 'part-3 hidden', session_data

            draw_started_at = session_data.get("draw_started_at")
            if not isinstance(draw_started_at, int):
                reset_draw_state(session_data)
                return "Tirage réinitialisé: relancez Alea Jacta Est", render_live_hexagram(session_data.get("line_values", [])), "", 'part-2', 'part-3 hidden', session_data

            index = int(re.search(r'stop-timer(\d+)-btn',
                        button_id).group(1)) - 1
            piece_stops = session_data.get("piece_stops", [False, False, False])
            stop_times = session_data.get("stop_times", [None, None, None])

            if not isinstance(piece_stops, list) or len(piece_stops) != 3:
                piece_stops = [False, False, False]
            if not isinstance(stop_times, list) or len(stop_times) != 3:
                stop_times = [None, None, None]

            if piece_stops[index]:
                return f"Pièce {index + 1} déjà stoppée", render_live_hexagram(session_data.get("line_values", [])), "", 'part-2', 'part-3 hidden', session_data

            elapsed_time = max(0, now_ms - draw_started_at)
            piece_stops[index] = True
            stop_times[index] = elapsed_time
            session_data["piece_stops"] = piece_stops
            session_data["stop_times"] = stop_times

            if all(time_value is not None for time_value in stop_times):
                session_data["phase"] = "resolving"
                random_state = session_data.get("random_state")
                result = process_line(stop_times, random_state)
                reset_draw_state(session_data)
                if "Error:" in result:
                    return result, render_live_hexagram(session_data.get("line_values", [])), "", 'part-2', 'part-3 hidden', session_data

                session_data["line_values"] = list(lines)
                session_data["last_line_type"] = result
                line_recap = render_live_hexagram(session_data["line_values"])

                if len(lines) == 6:
                    hexagram = get_hexagram()
                    session_data["hexagram"] = hexagram
                    session_data["interpretation_context"] = build_interpretation_context(lines, hexagram)
                    final_recap = render_annotated_hexagram_lines(session_data["line_values"], finalized=True)
                    return result, final_recap, render_hexagram_details(hexagram, lines), 'part-2 hidden', 'part-3', session_data

                return result, line_recap, "", 'part-2', 'part-3 hidden', session_data

            return f"Pièce {index + 1} stoppée", render_live_hexagram(session_data.get("line_values", [])), "", 'part-2', 'part-3 hidden', session_data
        except (IndexError, ValueError) as e:
            reset_draw_state(session_data)
            return f"Error processing timer: {str(e)}", render_live_hexagram(session_data.get("line_values", [])), "", 'part-2', 'part-3 hidden', session_data

    return "", render_live_hexagram(session_data.get("line_values", [])), "", 'part-2', 'part-3 hidden', session_data


@app.callback(
    Output('start-timer-btn', 'style'),
    Output('stop-timer1-btn', 'style'),
    Output('stop-timer2-btn', 'style'),
    Output('stop-timer3-btn', 'style'),
    Output('generate-6-lines-title', 'style'),
    Output('line-type-output', 'style'),
    Output('get-interpretation-btn', 'style'),
    Input('session-store', 'data')
)
def update_display(session_data):
    session_data = ensure_session_defaults(session_data or {})
    line_values = session_data.get("line_values", [])
    draw_started = session_data.get("phase") == "drawing" and session_data.get("draw_started", False)
    piece_stops = session_data.get("piece_stops", [False, False, False])
    if not isinstance(piece_stops, list) or len(piece_stops) != 3:
        piece_stops = [False, False, False]
    line_type_output_style = {'display': 'none'}
    hidden_style = {'display': 'none'}
    interpretation_button_style = {'display': 'none'}
    start_active_style = {'display': 'inline-block'}
    start_disabled_style = {
        'display': 'inline-block',
        'opacity': 0.45,
        'filter': 'grayscale(35%)',
        'pointerEvents': 'none',
        'transform': 'none'
    }
    piece_active_style = {'display': 'inline-block'}
    piece_disabled_style = {
        'display': 'inline-block',
        'opacity': 0.45,
        'filter': 'grayscale(35%)',
        'pointerEvents': 'none',
        'transform': 'none'
    }

    if len(line_values) == 6:
        start_style = hidden_style
        piece_1_style = hidden_style
        piece_2_style = hidden_style
        piece_3_style = hidden_style
        title_style = {'display': 'none'}
        line_type_output_style = {'display': 'none'}
        interpretation_button_style = {'display': 'block'}
    else:
        start_style = start_disabled_style if draw_started else start_active_style
        piece_1_style = piece_active_style if draw_started and not piece_stops[0] else piece_disabled_style
        piece_2_style = piece_active_style if draw_started and not piece_stops[1] else piece_disabled_style
        piece_3_style = piece_active_style if draw_started and not piece_stops[2] else piece_disabled_style
        title_style = {'display': 'block'}
        line_type_output_style = {'display': 'block'}

    return start_style, piece_1_style, piece_2_style, piece_3_style, title_style, line_type_output_style, interpretation_button_style


@app.callback(
    Output('interpretation-output', 'children'),
    Input('get-interpretation-btn', 'n_clicks'),
    State('session-store', 'data')
)
def provide_interpretation(n_clicks, session_data):
    if n_clicks > 0 and session_data:
        question = session_data.get("question")
        interpretation_context = session_data.get("interpretation_context", "")

        if not question or not interpretation_context:
            return "Error: contexte d'interpretation indisponible."

        interpretation = get_interpretation(question, interpretation_context)
        return interpretation

    return ""


@app.callback(
    Output('question-ghost', 'style'),
    Input('question-input', 'value')
)
def toggle_question_ghost(value):
    if value:
        return {'display': 'none'}
    return {'display': 'block'}


# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run(debug=False, host='0.0.0.0', port=port, dev_tools_ui=False)
