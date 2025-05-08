from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
user_ingredients = {}

@app.route("/whatsapp", methods=['POST'])
def whatsapp_bot():
    incoming_msg = request.values.get('Body', '').strip().lower()
    sender = request.values.get('From')

    if sender not in user_ingredients:
        user_ingredients[sender] = []

    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg == 'show list':
        if user_ingredients[sender]:
            msg.body("📝 Your ingredients:\n" + "\n".join(user_ingredients[sender]))
        else:
            msg.body("Your list is empty.")
    elif incoming_msg == 'clear list':
        user_ingredients[sender] = []
        msg.body("✅ List cleared.")
    else:
        user_ingredients[sender].append(incoming_msg)
        msg.body(f"Added: {incoming_msg}")

    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
