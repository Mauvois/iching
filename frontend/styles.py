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
            :root {
                --text-main: #f1ece2;
                --text-soft: #d8d0c2;
                --terracotta: #b86f52;
                --terracotta-dark: #8f5139;
                --celadon: #97b08b;
                --celadon-dark: #72886c;
                --mineral-red: #9c4f43;
            }
            body {
                font-family: 'Lato', sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                min-height: 100vh;
                margin: 0;
                background-image: url('/assets/frantisek-g-XXuVXLy5gHU-unsplash.jpg');
                background-size: cover;
                background-position: center;
                color: var(--text-main);
            }
            .container {
                background-color: transparent;
                padding: 24px 20px 36px 20px;
                border-radius: 8px;
                max-width: 800px;
                text-align: center;
                box-shadow: none;
                color: var(--text-main);
                width: min(92vw, 800px);
                margin: 0 auto;
            }
            .hexagram-line {
                height: 6px;
                margin: 6px 0;
            }
            .hexagram-line.solid {
                background-color: var(--text-main);
                margin-left: 30%;
                margin-right: 30%;
            }
            .hexagram-line.broken {
                background: linear-gradient(to right, var(--text-main) 40%, transparent 40%, transparent 60%, var(--text-main) 60%);
                margin-left: 30%;
                margin-right: 30%;
            }

            .hexagram-lines-annotated {
                width: min(96%, 700px);
                margin: 4px auto 10px auto;
            }
            .hexagram-line-row {
                display: grid;
                grid-template-columns: 190px max-content;
                align-items: center;
                column-gap: 3px;
                padding: 2px 2px;
                margin-bottom: 4px;
                max-width: 300px;
                margin-left: auto;
                margin-right: auto;
            }
            .hexagram-line-wrap {
                width: 190px;
                justify-self: center;
            }
            .hexagram-line-wrap .hexagram-line {
                margin-left: 0;
                margin-right: 0;
            }
            .hexagram-line-meta {
                min-width: 0;
                text-align: left;
                font-size: 0.88em;
                color: var(--text-main);
                white-space: nowrap;
            }
            .selected-line {
                color: #8fafc4;
            }
            .default-line {
                color: var(--text-main);
            }
            .pending-line {
                color: var(--text-soft);
            }
            .line-selected.solid {
                background-color: #8fafc4;
            }
            .line-selected.broken {
                background: linear-gradient(to right, #8fafc4 40%, transparent 40%, transparent 60%, #8fafc4 60%);
            }
            .line-default.solid {
                background-color: var(--text-main);
            }
            .line-default.broken {
                background: linear-gradient(to right, var(--text-main) 40%, transparent 40%, transparent 60%, var(--text-main) 60%);
            }
            .line-pending.solid {
                background-color: var(--text-soft);
            }

            .hexagram-live-wrapper {
                margin-top: 6px;
            }
            .info-box, .warning-box, .error-box, #interpretation-output {
                padding: 15px;
                border-radius: 0px;
                margin-bottom: 20px;
                color: var(--text-main);
                background-color: transparent;
                border: 0;
                text-align: center;
            }
            .transparent {
                opacity: 0.5; /* or any value between 0 and 1 for different levels of transparency */
                transition: opacity 0.5s ease; /* Smooth transition effect */
            }

            .text-primary {
                color: var(--text-main) !important;
            }
            .text-center {
                text-align: center !important;
                color: var(--text-main);
            }
            .btn {
                margin: 5px;
                padding: 10px 20px;
                font-size: 1.2em;
                border-radius: 8px;
                cursor: pointer;
                transparency: 0.3;
                transition: background-color 0.3s, transform 0.3s;
            }
            .btn:hover {
                transform: scale(1.05);
                transparency: 0.3;
            }
            .btn-start {
                background-color: var(--celadon);
                border: 2px solid var(--celadon);
                padding: 10px;
                margin: 16px 0;
                color: black;
                transparency: 0.3;
            }
            .btn-start:hover {
                background-color: var(--celadon-dark);
                transparency: 0.3;
            }
            .btn-interpret {
                background-color: var(--celadon);
                border: 2px solid var(--celadon);
                margin: 20px 0;
                color: black;
                padding: 10px 20px; /* Add padding for better appearance */
                font-size: 1.2em; /* Ensure consistent font size */
                border-radius: 8px; /* Add border radius for consistent button style */
                cursor: pointer;
                transition: background-color 0.3s, transform 0.3s;
                transparency: 0.3;
            }
            .btn-interpret:hover {
                background-color: var(--celadon-dark);
                transparency: 0.3;
            }
            .btn-stop {
                background-color: var(--terracotta);
                border: 2px solid var(--terracotta);
                margin: 8px;
                color: var(--text-main);
                transparency: 0.3;
                width: 56px;
                height: 56px;
                padding: 0;
                border-radius: 50%;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-size: 1.1em;
                line-height: 1;
                touch-action: manipulation;
                -webkit-tap-highlight-color: transparent;
                user-select: none;
            }
            .btn-stop:hover {
                background-color: var(--terracotta-dark);
                transparency: 0.3;
            }
            .btn-submit {
                background-color: transparent;
                border: 1px solid #8fafc4;
                color: #8fafc4;
                margin-top: 10px;
            }
            .btn-submit:hover {
                background-color: transparent;
                border-color: #8fafc4;
                color: #8fafc4;
            }
            .question-label {
                color: var(--text-main);
                font-size: 1.45em;
                margin-bottom: 10px;
            }
            .question-help {
                color: var(--text-soft);
                font-size: 0.95em;
                margin-bottom: 10px;
            }
            .question-input-shell {
                position: relative;
                width: 90%;
                border: 1px solid var(--text-main);
                border-radius: 8px;
                min-height: 40px;
                display: flex;
                align-items: center;
            }
            .question-input-shell:focus-within {
                border: 2px solid var(--text-main);
            }
            .question-ghost {
                position: absolute;
                left: 0;
                right: 0;
                text-align: center;
                color: var(--text-main);
                opacity: 1;
                pointer-events: none;
                user-select: none;
            }
            .form-control {
                -webkit-appearance: none;
                appearance: none;
                background-color: transparent;
                color: var(--text-main);
                border: 0;
                min-height: 40px;
                width: 100%;
                border-radius: 8px;
                padding: 4px 10px;
                transition: color 0.2s ease;
                text-align: center;
                outline: none;
                box-shadow: none;
                caret-color: var(--text-main);
            }
            .form-control:focus {
                background-color: transparent;
                color: var(--text-main);
                outline: none;
                border: 0;
                min-height: 40px;
                width: 100%;
                border-radius: 8px;
                box-shadow: none;
            }
            .form-control:focus-visible {
                outline: none;
                border: 0;
                box-shadow: none;
            }
            #question-input,
            #question-input:focus,
            #question-input:focus-visible {
                outline: none;
                border: 0;
                box-shadow: none;
            }
            .question-input-shell .dash-input-container,
            .question-input-shell .dash-input-container:focus-within,
            .question-input-shell .dash-input-container:has(:focus-visible) {
                border: 0 !important;
                outline: none !important;
                box-shadow: none !important;
                -webkit-box-shadow: none !important;
                background: transparent !important;
            }
            .question-input-shell #question-input,
            .question-input-shell #question-input:focus,
            .question-input-shell #question-input:focus-visible,
            .question-input-shell .dash-input-element,
            .question-input-shell .dash-input-element:focus,
            .question-input-shell .dash-input-element:focus-visible {
                border: 0 !important;
                outline: none !important;
                box-shadow: none !important;
                -webkit-box-shadow: none !important;
            }
            .question-display {
                color: var(--text-main);
                font-size: clamp(1.1rem, 3.6vw, 1.8rem);
                margin: 8px 0 14px 0;
                text-align: center;
                max-width: 90%;
                line-height: 1.4;
                overflow-wrap: anywhere;
            }
            .hexagram-title {
                color: var(--text-main);
                text-align: center;
                font-size: 2em;
            }
            .uniform-text {
                color: white;
                text-align: left; /* Uniform text alignment */
                font-size: 1.2em; /* Uniform font size */
                width: 100%;
            }
            .hexagram-detail {
                text-align: left; /* Uniform text alignment */
                font-size: 1.2em; /* Uniform font size */
            }
            .hexagram-section {
                text-align: left; /* Uniform text alignment */
                font-size: 1.2em; /* Uniform font size */
            }
            #interpretation-output {
                text-align: left; /* Uniform text alignment */
                font-size: 1.2em; /* Uniform font size */
            }
            .line-recap {
                width: min(92%, 620px);
                margin: 8px auto 18px auto;
                color: var(--text-main);
                text-align: left;
                max-width: 620px;
            }

            .line-row {
                display: flex;
                justify-content: space-between;
                border-radius: 6px;
                padding: 8px 10px;
                margin-bottom: 6px;
                gap: 12px;
            }
            .line-row-active {
                background: transparent;
                border: 0;
            }
            .line-row-inactive {
                background: transparent;
                border: 0;
            }
            .line-row-neutral {
                background: transparent;
                border: 0;
            }
            .line-row-pending {
                background: transparent;
                border: 0;
                color: var(--text-soft);
            }

            .selected-trait {
                color: #8fafc4;
                border-left: 2px solid #8fafc4;
                padding-left: 8px;
                margin: 4px 0;
            }

            .muted-trait {
                color: var(--text-main);
                border-left: 2px solid var(--text-soft);
                padding-left: 8px;
                margin: 4px 0;
            }

            .trait-legend {
                margin-top: 12px;
                color: var(--text-soft);
                font-size: 0.95em;
            }

            .hidden {
                opacity: 0;
                transition: opacity 0.5s ease;
            }

            .line-type {
                margin-top: 20px;
            }
            .button-group {
                display: flex;
                justify-content: center;
                gap: 10px;
                flex-wrap: wrap;
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

            @media (max-width: 680px) {
                .container {
                    width: 94vw;
                    padding: 18px 14px 28px 14px;
                }
                .btn {
                    width: 100%;
                    max-width: 360px;
                    font-size: 1em;
                }
                .btn-stop {
                    width: 52px;
                    height: 52px;
                    max-width: 52px;
                    font-size: 1em;
                }
                .button-group {
                    width: 100%;
                }
                .line-row {
                    font-size: 0.95em;
                }
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
