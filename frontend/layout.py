from dash import html, dcc


def create_layout():
    return html.Div([

        # Part 1: Ask Question
        html.Div(id='part-1', children=[
            html.Div('Quelle est votre question pour l\'Oracle?',
                     className='question-label'),
            dcc.Input(id='question-input', type='text', debounce=True,
                      placeholder='', className='form-control my-3'),
            html.Button('', id='submit-question-btn',
                        n_clicks=0, className='btn btn-transparent my-3')
        ], className="container"),

        # Part 2: Initialize Toss and Generate Lines (Initially Hidden)
        html.Div(id='part-2', children=[
            html.Div(id='question-display', className='question-display my-3'),
            html.H3("Generate 6 Lines", id='generate-6-lines-title',
                    className="mt-5 text-primary"),
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
            html.Div(id='line-output', className='alert alert-info line-recap'),
            html.Div(id='line-type-output', className='line-type')
        ], className="container", style={'display': 'none'}),

        # Part 3: Display Hexagram and Interpretation (Initially Hidden)
        html.Div(id='part-3', children=[
            html.Div(id='question-display-3',
                     className='question-display my-3'),
            html.Div(id='hexagram-output', className="container my-5"),
            html.H3("Interpretation", className="mt-5 text-primary"),
            html.Button('Get Interpretation', id='get-interpretation-btn',
                        n_clicks=0, className='btn btn-info my-3'),
            html.Div(id='interpretation-output',
                     className='alert alert-warning')
        ], className="container", style={'display': 'none'})
    ])
