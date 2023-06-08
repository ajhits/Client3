from flask import Flask, render_template, session


import random
import string
import time

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.debug = True  # Enable debug mode


OTP_EXPIRATION_SECONDS = 60

def generate_otp(length=6):
        characters = string.ascii_uppercase + string.ascii_lowercase + string.digits
        return ''.join(random.choice(characters) for _ in range(length))

@app.route('/')
def index():
        current_time = time.time()

        if 'otp' not in session or 'otp_expiration' not in session or current_time > session['otp_expiration']:
            session['otp'] = generate_otp()
            session['otp_expiration'] = current_time + OTP_EXPIRATION_SECONDS
            session.modified = True


            remaining_time = session['otp_expiration'] - current_time
            return render_template('index.html', otp=session['otp'], remaining_time=int(remaining_time))

if __name__ == '__main__':
        app.run()