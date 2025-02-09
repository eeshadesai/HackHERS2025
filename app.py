import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from dotenv import load_dotenv
from groq import Groq

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

client = Groq(api_key="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")


# Secret key for session management (Change this in production)
app.secret_key = os.getenv("SECRET_KEY", "your_default_secret_key")

# Pre-set username and password
USERNAME = 'admin'
PASSWORD = 'password123'

@app.route('/')
def home():
    """Redirects to the login page if not logged in, else to the index page."""
    if not session.get('logged_in'):  # Check if user is logged in
        return redirect(url_for('login'))  # Redirect to login page
    return render_template('index.html')  # Render main page

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handles user login authentication."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Debugging output (remove in production)
        print(f"Login attempt: {username}, {password}")

        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True  # Store session information
            return redirect(url_for('home'))  # Redirect to main page
        else:
            return render_template("login.html", error="Invalid credentials. Please try again.")  # Show error

    return render_template('login.html')  # Render login form for GET request

@app.route('/logout')
def logout():
    """Logs the user out and redirects to the login page."""
    session.pop('logged_in', None)  # Remove session data
    return redirect(url_for('login'))

@app.route("/chat", methods=["POST"])
def chat():
   user_message = request.json.get("message")
  
   if not user_message:
       return jsonify({"error": "No message received"}), 400


   messages = [
       {"role": "system", "content": "You are a rehab specialist. You give a diagnosis based on symptoms or if given an injury, create a plan to heal."},
       {"role": "user", "content": user_message},
   ]


   chat_completion = client.chat.completions.create(
       messages=messages,
       model="llama-3.3-70b-versatile",
   )


   response = chat_completion.choices[0].message.content
   return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
