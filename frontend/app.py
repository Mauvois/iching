import streamlit as st
import requests
import time

# Define the base URL of your API
BASE_URL = "http://localhost:8000"

# Custom styles
st.markdown("""
    <style>
    .start-button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 10px 24px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
    }
    .start-button:hover {
        background-color: #45a049;
    }
    .stop-button {
        background-color: #f44336;
        color: white;
        font-size: 16px;
        padding: 10px 24px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
    }
    .stop-button:hover {
        background-color: #e53935;
    }
    .clear-button {
        background-color: #2196F3;
        color: white;
        font-size: 16px;
        padding: 10px 24px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
    }
    .clear-button:hover {
        background-color: #1e88e5;
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        padding: 10px;
        border: 2px solid #ccc;
        font-size: 16px;
    }
    .stAlert {
        border-radius: 8px;
        padding: 10px;
    }
    .hexagram-line {
        width: 100%;
        height: 10px;
        margin: 5px 0;
    }
    .solid {
        background-color: black;
    }
    .broken {
        background: linear-gradient(to right, black 40%, white 40%, white 60%, black 60%);
    }
    .hexagram-title {
        font-size: 24px;
        font-weight: bold;
        margin-top: 20px;
    }
    .hexagram-detail {
        margin-top: 10px;
    }
    .hexagram-section {
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("I Ching Digital Project")

# Step 1: Initialize Toss
st.header("Step 1: Initialize Toss")
st.write("Enter your question to start the I Ching consultation process.")
question = st.text_input("Enter your question:")

random_state = None

if st.button("Initialize Toss"):
    response = requests.post(
        f"{BASE_URL}/initialize-toss", json={"text": question})
    if response.status_code == 200:
        random_state = response.json().get("random_state")
        st.session_state["random_state"] = random_state
        st.session_state["lines"] = []
        st.session_state["start_time"] = None
        st.session_state["times"] = []
        st.session_state["timer_running"] = False
        st.session_state["stopped_timers"] = [False, False, False]
        st.success(f"Random State: {random_state}")
    else:
        st.error(f"Error: {response.json().get('detail')}")

if "random_state" in st.session_state:
    random_state = st.session_state["random_state"]

# Step 2: Generate Line
st.header("Step 2: Generate Line")
st.write("Start the timer and stop it three times to generate a line.")

if random_state is not None:
    if "timer_running" not in st.session_state:
        st.session_state["timer_running"] = False
    if "stopped_timers" not in st.session_state:
        st.session_state["stopped_timers"] = [False, False, False]

    def start_timer():
        st.session_state["start_time"] = time.time()
        st.session_state["times"] = []
        st.session_state["timer_running"] = True
        st.session_state["stopped_timers"] = [False, False, False]

    def stop_timer(index):
        if st.session_state["start_time"] is not None:
            elapsed_time = int(
                (time.time() - st.session_state["start_time"]) * 1000)
            if len(st.session_state["times"]) < index + 1:
                st.session_state["times"].append(elapsed_time)
            else:
                st.session_state["times"][index] = elapsed_time
            st.session_state["stopped_timers"][index] = True
            if all(st.session_state["stopped_timers"]):
                st.session_state["timer_running"] = False
                process_line()

    def process_line():
        times_list = st.session_state["times"]
        response = requests.post(
            f"{BASE_URL}/generate-line",
            json={"times": times_list, "random_state": random_state}
        )
        if response.status_code == 200:
            result = response.json()
            st.session_state["lines"].append(result['line_sum'])
            # st.success(
            #     f"Line Type: {result['line_type']}, Line Sum: {result['line_sum']}")
        else:
            st.error(f"Error: {response.json().get('detail')}")

    def get_hexagram():
        response = requests.post(
            f"{BASE_URL}/get-hexagram", json={"line_values": st.session_state["lines"]})
        if response.status_code == 200:
            hexagram = response.json().get("hexagram")
            display_hexagram(hexagram)
        else:
            st.error(f"Error: {response.json().get('detail')}")

    def clear_state():
        st.session_state["times"] = []
        st.session_state["start_time"] = None
        st.session_state["timer_running"] = False
        st.session_state["stopped_timers"] = [False, False, False]

    def render_hexagram_line(line_value):
        if line_value in [6, 8]:  # Yin line
            return '<div class="hexagram-line broken"></div>'
        elif line_value in [7, 9]:  # Yang line
            return '<div class="hexagram-line solid"></div>'
        else:
            return ''

    def display_hexagram(hexagram):
        st.markdown(
            f'<div class="hexagram-title">{hexagram[1]}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="hexagram-detail">Hexagram Number: {hexagram[0]}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="hexagram-detail">Name: {hexagram[1]}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="hexagram-detail">Upper Trigram: {hexagram[2]}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="hexagram-detail">Lower Trigram: {hexagram[3]}</div>', unsafe_allow_html=True)
        st.markdown(
            f'<div class="hexagram-section"><strong>Judgment:</strong> {hexagram[4]}</div>', unsafe_allow_html=True)
        for line_detail in hexagram[5:]:
            st.markdown(
                f'<div class="hexagram-section"><strong>Line:</strong> {line_detail}</div>', unsafe_allow_html=True)

    # Start Timer button
    if st.button("Start Timer", key="start_timer", help="Start the timer to begin generating a line"):
        start_timer()

    # Stop Timer buttons
    st.write("Stop the timer three times to complete a line:")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Stop Timer 1", key="stop_timer_1"):
            stop_timer(0)
    with col2:
        if st.button("Stop Timer 2", key="stop_timer_2"):
            stop_timer(1)
    with col3:
        if st.button("Stop Timer 3", key="stop_timer_3"):
            stop_timer(2)

    st.write("")  # Just to add a little space
    if st.button("Clear", key="clear_button"):
        clear_state()

    if st.session_state["timer_running"]:
        st.info("Timer is running...")
    elif all(st.session_state["stopped_timers"]):
        st.info("Timer is stopped.")

    st.info(f"Lines: {st.session_state['lines']}")

    # Render the hexagram visually
    if len(st.session_state["lines"]) > 0:
        # Reverse the lines to display from bottom to top
        reversed_lines = st.session_state["lines"][::-1]
        hexagram_html = ''.join([render_hexagram_line(line)
                                for line in reversed_lines])
        st.markdown(f'<div>{hexagram_html}</div>', unsafe_allow_html=True)

    if len(st.session_state["lines"]) == 6:
        get_hexagram()
