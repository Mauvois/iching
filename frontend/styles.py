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
                background-color: rgba(0, 0, 0, 0);
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
            .info-box, .warning-box, .error-box, #interpretation-output {
                padding: 15px;
                border-radius: 0px;
                margin-bottom: 20px;
                color: white;
                background-color: rgba(0, 0, 0, 0); /* Set background to transparent */
                border: 0px solid white;
                text-align: justify; /* Use 'left' if you prefer left alignment */
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
                background-color: #99C24D; 
                border: 2px solid #99C24D;
                margin: 30px;
                color: black;
                padding: 10px 20px; /* Add padding for better appearance */
                font-size: 1.2em; /* Ensure consistent font size */
                border-radius: 8px; /* Add border radius for consistent button style */
                cursor: pointer;
                transition: background-color 0.3s, transform 0.3s;
            }
            .btn-interpret:hover {
                background-color: #7BA035;
            }
            .btn-stop {
                background-color: #E2725B; /* Terracotta Ocre */
                border: 2px solid #E2725B;
                margin: 30px;
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
                background-color: rgba(0, 0, 0, 0);
                color: white;
                border: 1px solid white;
                transition: border-color 0.3s, border-width 0.3s; /* Add border-width to the transition */
                height: 30px; 
                width: 90%;
                border-radius: 8px;
            }
            .form-control:focus {
                background-color: rgba(255, 255, 255, 0);
                color: white;
                border: 3px solid white; /* Ensure the border width is increased */
                outline: none;
                height: 30px; 
                width: 90%;
                border-radius: 8px;
            }
            .question-display {
                color: white;
                font-size: 3em;
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
                text-align: justify; /* Use 'left' if you prefer left alignment */
                width: 100%;
            }
            .hexagram-section {
                color: white;
                text-align: justify; /* Use 'left' if you prefer left alignment */
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
            .center {
                display: flex;
                justify-content: center;
                align-items: center;
                width: 100%;
            }
            .part-1, .part-2, .part-3 {
                display: flex;
                flex-direction: column;
                align-items: center;
                width: 100%;
                transition: opacity 0.3s ease, visibility 0.3s ease;
            }
            .part-1.hidden, .part-2.hidden, .part-3.hidden {
                opacity: 0;
                visibility: hidden;
                height: 0;
                overflow: hidden;
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
