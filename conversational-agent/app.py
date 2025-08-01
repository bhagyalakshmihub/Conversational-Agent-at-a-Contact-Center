from flask import Flask, render_template, request, jsonify
from chatbot_logic import get_response

app = Flask(__name__, template_folder='.')


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/get-response', methods=['POST'])
def bot_response():
    user_input = request.form['message']
    reply = get_response(user_input)
    return jsonify({"response": reply})

# Add other routes if needed
@app.route('/help')
def help_page():
    return render_template("help.html")

@app.route('/history')
def history_page():
    return render_template("history.html")

if __name__ == '__main__':
    app.run(debug=True)
