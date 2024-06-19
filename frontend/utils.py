import time
import requests
from dash import html
from .config import BACKEND_API_URL, INTERPRETATION_API_URL

start_time = None
stop_times = []
lines = []
random_state = None


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
        f"{BACKEND_API_URL}/generate-line",
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
        f"{BACKEND_API_URL}/get-hexagram", json={"line_values": lines}
    )
    if response.status_code == 200:
        hexagram = response.json().get("hexagram")
        return hexagram
    else:
        return None


def render_hexagram_line(line_value):
    if (line_value % 2) == 0:
        return html.Div(className='hexagram-line broken')
    else:
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
