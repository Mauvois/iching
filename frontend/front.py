import dash
from frontend.layout import create_layout
from frontend.callbacks import register_callbacks
import os

external_stylesheets = [
    'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css',
    'https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap'
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

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
                color: white;
            }
            .container {
                background-color: rgba(255, 255, 255, 0);
                padding: 20px;
                border-radius: 8px;
                max-width: 800px;
                text-align: center;
                box-shadow: 0 0px 8px rgba(0, 0, 0, 0);
                color: white;
                width: 100%;
            }
            .hexagram-line {
                height: 8px;
                margin: 10px 0;
            }
            .hexagram-line.solid {
                background-color: white;
                margin-left: 30%;
                margin-right: 30%;
            }
            .hexagram-line.broken {
                background: linear-gradient(to right, white 40%, transparent 40%, transparent 60%, white 60%);
                margin-left: 30%;
                margin-right: 30%;
            }
            .alert-info, .alert-warning, .alert-danger {
                background-color: rgba(255, 255, 255, 0);
                border: none;
                color: white;
            }
            .text-primary {
                color: white !important;
            }
            .text-center {
                text-align: center !important;
                color: white;
            }
            .btn {
                margin: 5px;
            }
            .btn-transparent {
                background-color: transparent;
                border: none;
                color: white.
            }
            .question-label {
                color: white.
                font-size: 1.5em.
                margin-bottom: 10px.
            }
            .form-control::placeholder {
                color: white.
                opacity: 1.
            }
            .form-control {
                background-color: rgba(255, 255, 255, 0).
                color: white.
                border: 1px solid white.
                transition: border-color 0.3s.
            }
            .form-control:focus {
                background-color: rgba(255, 255, 255, 0).
                color: white.
                border: 2px solid white.
                outline: none.
            }
            .question-display {
                color: white.
                font-size: 2em.
                margin-top: 20px.
                text-align: center.
            }
            .hexagram-title {
                color: white.
                text-align: center.
                font-size: 2em.
            }
            .hexagram-detail {
                color: white.
                text-align: left.
                width: 100%.
            }
            .hexagram-section {
                color: white.
                text-align: left.
                width: 100%.
            }
            .line-recap {
                position: absolute.
                left: 10px.
                top: 20%.
                color: white.
                text-align: left.
                max-width: 200px.
            }
            .line-type {
                margin-top: 20px.
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

app.layout = create_layout()

register_callbacks(app)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run_server(debug=True, host='0.0.0.0', port=port)
