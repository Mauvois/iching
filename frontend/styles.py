# styles.py

external_stylesheets = [
    'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css',
    'https://fonts.googleapis.com/css2?family=Lato:wght@400;700&display=swap'
]

index_string = '''
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
                max-width: 800px; /* Increased max-width */
                text-align: center;
                box-shadow: 0 0px 8px rgba(0, 0, 0, 0);
                color: white; /* Turn container text white */
                width: 100%;
            }
            .hexagram-line {
                height: 8px;
                margin: 10px 0;
            }
            .hexagram-line.solid {
                background-color: white;
                margin-left: 30%; /* Reduce the left margin */
                margin-right: 30%; /* Reduce the right margin */
            }
            .hexagram-line.broken {
                background: linear-gradient(to right, white 40%, transparent 40%, transparent 60%, white 60%);
                margin-left: 30%; /* Reduce the left margin */
                margin-right: 30%; /* Reduce the right margin */
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
                text-align: center;
                font-size: 2em;
            }
            .hexagram-detail {
                color: white; /* Turn hexagram detail text white */
                text-align: left; /* Align detail text to the left */
                width: 100%; /* Ensure details use full width */
            }
            .hexagram-section {
                color: white; /* Turn hexagram section text white */
                text-align: left; /* Align section text to the left */
                width: 100%; /* Ensure sections use full width */
            }
            .line-recap {
                position: absolute;
                left: 10px;
                top: 20%;
                color: white;
                text-align: left;
                max-width: 200px;
            }
            .line-type {
                margin-top: 20px;
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
