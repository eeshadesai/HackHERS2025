import os
from flask import Flask, request, jsonify, render_template
from groq import Groq


from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)


client = Groq(api_key="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")


@app.route("/")
def index():
   return render_template("index.html")


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