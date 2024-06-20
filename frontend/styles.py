# styles.py

external_stylesheets = [
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
                padding: 10px 20px;
                font-size: 1.2em;
                border-radius: 8px;
                cursor: pointer;
                transition: background-color 0.3s, transform 0.3s;
            }
            .btn:hover {
                transform: scale(1.05);
            }
            .btn-start {
                background-color: #99C24D; /* MIT Celadon */
                border: 2px solid #99C24D;
                padding: 10px;
                margin: 50px;
                color: black;
            }
            .btn-start:hover {
                background-color: #7BA035;
            }
            .btn-interpret {
                background-color: #99C24D; /* MIT Celadon */
                border: 2px solid #99C24D;
                color: white;
            }
            .btn-interpret:hover {
                background-color: #7BA035;
            }
            .btn-stop {
                background-color: #E2725B; /* Terracotta Ocre */
                border: 2px solid #E2725B;
                color: white;
            }
            .btn-stop:hover {
                background-color: #B55A46;
            }
            .btn-transparent {
                background-color: transparent;
                border: none;
                color: white;
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
                color: white;
                text-align: center;
                font-size: 2em;
            }
            .hexagram-detail {
                color: white;
                text-align: left;
                width: 100%;
            }
            .hexagram-section {
                color: white;
                text-align: left;
                width: 100%;
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
            .button-group {
                display: flex;
                justify-content: center;
                gap: 10px;
            }
            .part-1, .part-2, .part-3 {
                display: none;
            }
            .visible {
                display: block;
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
