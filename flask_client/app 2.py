from flask import Flask, request, render_template, redirect, url_for, flash
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_default_secret_key')  # Load the secret key from environment variables

# Twilio credentials from environment variables
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')

client = Client(account_sid, auth_token)

@app.route('/')
def index():
    return render_template('index.html', available_numbers=[])

@app.route('/make_call', methods=['POST'])
def make_call():
    to_phone_number = request.form['to_phone_number']
    from_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
    call = client.calls.create(
        to=to_phone_number,
        from_=from_phone_number,
        url='http://demo.twilio.com/docs/voice.xml'
    )
    return f"Call initiated with SID: {call.sid}"

@app.route('/search_numbers', methods=['POST'])
def search_numbers():
    country = request.form['country']
    area_code = request.form.get('area_code', None)

    try:
        if area_code:
            available_numbers = client.available_phone_numbers(country).local.list(area_code=area_code)
        else:
            available_numbers = client.available_phone_numbers(country).local.list()

        return render_template('index.html', available_numbers=available_numbers)
    except Exception as e:
        flash(f"Error searching for numbers: {e}")
        return redirect(url_for('index'))

@app.route('/buy_number', methods=['POST'])
def buy_number():
    phone_number = request.form['phone_number']
    try:
        purchased_number = client.incoming_phone_numbers.create(phone_number=phone_number)
        flash(f"Purchased number: {purchased_number.phone_number}")
    except Exception as e:
        flash(f"Error purchasing number: {e}")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
