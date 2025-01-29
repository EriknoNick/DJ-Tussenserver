from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Gebruik een omgevingsvariabele voor de OpenAI API-key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route('/openai-webhook', methods=['POST'])
def openai_webhook():
    data = request.json
    user_message = data.get("message")  # Haal de vraag uit DJ op

    if not user_message:
        return jsonify({"error": "Geen bericht ontvangen"}), 400

    # Verstuur de vraag naar OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=[{"role": "user", "content": user_message}],
        api_key=OPENAI_API_KEY
    )

    # Haal het antwoord op en stuur het terug naar DJ
    openai_response = response["choices"][0]["message"]["content"]
    return jsonify({"response": openai_response})

if __name__ == '__main__':
    import os
app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))


