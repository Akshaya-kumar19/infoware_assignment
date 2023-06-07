from flask import Flask, render_template, request
import requests
import pyttsx3
import openai

app = Flask(__name__)


health_conditions = ["Condition 1", "Condition 2", "Condition 3"]
severity_levels = ["Low", "Medium", "High"]


chatgpt_api_url = "https://api.openai.com/v1/engines/davinci-codex/completions"


def chat_with_gpt(prompt):
    headers = {
        "Authorization": "Bearer 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",
        "Content-Type": "application/json"
    }
    data = {
        "prompt": prompt,
        "max_tokens": 50
    }
    response = requests.post(chatgpt_api_url, headers=headers, json=data)
    return response.json()["choices"][0]["text"].strip()


def text_to_speech(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.say(text)
    engine.runAndWait()

@app.route("/", methods=["GET", "POST"])
def chatbot():
    if request.method == "POST":
        condition = request.form.get("condition")
        severity = request.form.get("severity")
        prompt = f"Health Condition: {condition}\nSeverity: {severity}\n"
        response = chat_with_gpt(prompt)
        text_to_speech(response)
        return render_template("index.html", conditions=health_conditions, severity=severity_levels, response=response)
    return render_template("index.html", conditions=health_conditions, severity=severity_levels)

if __name__ == "__main__":
    app.run(debug=True)
