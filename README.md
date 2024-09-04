# IChing Project

## Overview

IChing is a web application that brings the ancient Chinese oracle, the **I Ching** (Book of Changes), into the modern digital age. Built using Dash for the front end, FastAPI for the back end, and DuckDB for efficient storage and querying, this app allows users to interact with the I Ching through a simple and intuitive interface.

Users can pose a question to the oracle, and a randomized process is used to generate a hexagram based on the question. The resulting hexagram is then sent to ChatGPT via Langchain, which provides a contemporary interpretation of the oracle's response.

## Features

- **User Interaction**: Users can enter their question and interact with a simulation of the I Ching's traditional coin-toss method to generate hexagrams.
- **Hexagram Generation**: Six lines are constructed based on user interaction and a random procedure to form one of the 64 possible hexagrams.
- **Interpretation**: The generated hexagram is sent to a Langchain-powered service that uses ChatGPT to provide a modern interpretation of the ancient text.
- **Microservice Architecture**: The application uses a FastAPI backend to handle the logic and a separate Langchain microservice for generating interpretations via ChatGPT.

## Architecture

- **Front End**: Built with Dash, providing a responsive and interactive user interface. It manages user inputs and displays the results.
- **Back End**: Implemented with FastAPI, which handles API requests for generating hexagram lines and retrieving interpretations.
- **Database**: DuckDB is used for storing data related to hexagrams and user interactions efficiently.
- **Langchain Service**: A separate microservice using Langchain connects to ChatGPT, providing nuanced and contextual interpretations.

## Installation

### Prerequisites

- Python 3.8 or higher
- Node.js (for building frontend assets if modified)
- Docker (optional, for containerized deployment)

### Steps

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/iching.git
    cd iching
    ```

2. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3. **Set Environment Variables**:
    Define the following environment variables for connecting to backend services:

    - `BACKEND_API_URL`: URL for the FastAPI backend service.
    - `INTERPRETATION_API_URL`: URL for the Langchain interpretation microservice.

4. **Run the Application**:
    ```bash
    python front.py
    ```
    The application will start on `http://0.0.0.0:8050` by default.

## Usage

1. **Enter a Question**: On the homepage, users can enter a question for the oracle in the input field provided.
2. **Generate Hexagram**: By clicking on the "Alea Jacta Est" button, users start the process of generating hexagram lines. The app simulates the traditional coin toss six times to generate a hexagram.
3. **Interpretation**: Once the hexagram is generated, users can click on the "Get Interpretation" button to receive a modern interpretation of their hexagram from ChatGPT.

## Development

### Frontend

The frontend is built with Dash. To make changes:

- Modify the `front.py` file for layout and callback changes.
- Use CSS for styling located in the `styles.py` file.

### Backend

The backend logic is handled by a FastAPI application:

- The backend processes the random number generation and constructs hexagrams based on user interactions.
- It communicates with the Langchain service to fetch interpretations.

### Langchain Microservice

The microservice that connects with ChatGPT is hosted separately. For more details, see the repository: [Langchain Interpreter](https://github.com/Mauvois/interpreter).

## Deployment

### Docker

1. **Build Docker Image**:
    ```bash
    docker build -t iching-app .
    ```

2. **Run Docker Container**:
    ```bash
    docker run -d -p 8050:8050 iching-app
    ```

### Cloud Deployment

- **Google Cloud Run**: The FastAPI backend and Langchain services are suitable for deployment on platforms like Google Cloud Run.
- **Heroku**: Use Docker-based deployments for Heroku to run the complete stack.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- **I Ching Community**: For the timeless wisdom and insights provided by the Book of Changes.
- **OpenAI**: For providing the underlying language model that powers modern interpretations.
- **Dash & FastAPI**: For creating powerful frameworks that facilitate rapid development of web applications.
