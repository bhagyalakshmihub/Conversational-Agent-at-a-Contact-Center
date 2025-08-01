# No Talent Chatbot

This project is a simple chatbot web application built with Flask. It uses sentence-transformers for natural language processing, FAISS for efficient similarity search, and numpy for numerical operations.

## Features
- Web-based chatbot interface
- Semantic search using sentence-transformers and FAISS
- User chat history
- Settings and suggestions pages

## Project Structure
- `app.py`: Main Flask application
- `chatbot_logic.py`: Core chatbot logic
- `index.html`, `help.html`, `history.html`, `settings.html`, `suggestions.html`: HTML templates for the web interface
- `requirements.txt`: Python dependencies

## Installation
1. Clone the repository or download the source code.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. Open your browser and go to `http://127.0.0.1:5000/` to use the chatbot.

## Requirements
- Python 3.8+
- Flask
- sentence-transformers
- faiss-cpu
- numpy

## License
This project is for educational purposes.
