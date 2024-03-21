# twilio_utils.py
from twilio.rest import Client

def send_sms(recipient_number, message):
    # Your Twilio credentials
    account_sid = 'AC5649992a1008a1d4e8455e183b97072d'
    auth_token = '11aac5884cccdfd8869d78de65606fb5'

    # Initialize Twilio client
    client = Client(account_sid, auth_token)

    try:
        # Send SMS message
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body='Your Booking has been successful',
            to='whatsapp:+919061849932'
        )
        print("Message sent successfully:", message.sid)
        return True
    except Exception as e:
        print("Failed to send message:", str(e))
        return False