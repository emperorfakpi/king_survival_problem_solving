from flask import Flask, request, jsonify, render_template
import requests
import re

app = Flask(__name__, static_folder='assets', template_folder='templates')

# Your Telegram bot token and chat ID
TELEGRAM_BOT_TOKEN = '7377509769:AAF9uJ1kRFAHQkio80h2xfykDkh3Pcpekx4'
CHAT_ID = '1803335709'

def escape_markdown(text):
    # Escape special Markdown characters
    return re.sub(r'([*_`\[\]()])', r'\\\1', text)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Get data from the form submission
        section = request.form.get('section')
        book_id = request.form.get('bookId')
        user_name = request.form.get('userName')
        index_number = request.form.get('indexNumber')
        unique_code = request.form.get('uniqueCode')

        if not all([section, book_id, user_name, index_number, unique_code]):
            return jsonify({"status": "error", "message": "All form fields are required."}), 400

        # Format message to be sent to Telegram
        message = (
            f"New Reservation Request:\n"
            f"Unique Code: {escape_markdown(unique_code)}\n"
            f"Section: {escape_markdown(section)}\n"
            f"Book ID: {escape_markdown(book_id)}\n"
            f"User Name: {escape_markdown(user_name)}\n"
            f"Index Number: {escape_markdown(index_number)}"
        )

        # Send message to Telegram
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            'chat_id': CHAT_ID,
            'text': message,
            'parse_mode': 'Markdown'
        }
        response = requests.post(telegram_url, data=payload)

        # Log detailed response
        print(f"Telegram API response status code: {response.status_code}")
        print(f"Telegram API response content: {response.text}")

        if response.status_code == 200:
            return jsonify({"status": "success", "message": "Request sent to Telegram."}), 200
        else:
            return jsonify({"status": "error", "message": "Failed to send request to Telegram."}), 500
    except Exception as e:
        # Log the exception and return a 500 response
        print(f"Error occurred: {e}")
        return jsonify({"status": "error", "message": "Internal server error."}), 500

if __name__ == '__main__':
    app.run(debug=True)
