import requests
import time

# Telegram settings
ENABLE_TELEGRAM_REPORTING = True



def send_telegram_message(message):

    ENABLE_TELEGRAM_REPORTING = True
    TELEGRAM_TOKEN = "7140485854:AAFaIV7BDNpTNIxU8BtMXcITYPGpnyzzyak"
    CHAT_ID = "6744465611"

    if not ENABLE_TELEGRAM_REPORTING:
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    response = requests.post(url, payload)
    return response.json()


def run():
    while True:

        send_telegram_message( "works")
        time.sleep( 60)

if __name__ == "__main__":
   run()
