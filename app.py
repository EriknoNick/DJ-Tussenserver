from flask import Flask, request, jsonify
import openai
import os
import logging

app = Flask(__name__)

# Zet logging aan om de ontvangen data van DJ te bekijken
logging.basicConfig(level=logging.INFO)

# Haal de OpenAI API-key op vanuit de omgevingsvariabelen
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route('/openai-webhook', methods=['POST'])
def openai_webhook():
    # Haal de JSON-data op van DJ
    data = request.json

    # Log de volledige binnenkomende request zodat we zien wat DJ stuurt
    logging.info(f"DJ stuurde deze data: {data}")

    if not data:
        return jsonify({"error": "Lege request ontvangen"}), 400

    # DJ stuurt "text" in plaats van "message"
    user_message = data.get("text")  # Aangepast naar "text"

    if not user_message:
        return jsonify({"error": "Geen geldig bericht ontvangen. Controleer de JSON-structuur."}), 400

    try:
        # **Nieuwe OpenAI-aanroep volgens de juiste syntax**
        client = openai.OpenAI(api_key=OPENAI_API_KEY)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )

        # Haal het antwoord op en stuur het terug naar DJ
        openai_response = response.choices[0].message.content
        return jsonify({"response": openai_response})

    except Exception as e:
        logging.error(f"OpenAI-fout: {str(e)}")
        return jsonify({"error": "Er is een probleem met de OpenAI-verwerking."}), 500

# Start de server op de juiste poort
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
