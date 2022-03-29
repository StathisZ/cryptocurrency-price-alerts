import requests
import time
from datetime import datetime

# Replace the {my-IFTTT-key} with the key found in your IFTTT account.

IFTTT_WEBHOOKS_URL = 'https://maker.ifttt.com/trigger/{}/with/key/bZ6ju4k6baW8L-Kmx1LpIEHqN-ysrTrko15jPow6dfM'

# input sequence

symbol = input("Insert the cryptocurrency symbol you want to track:")
CRYPTO_PRICE_THRESHOLD = input("What is the minimum price for which you want to receive alert?")
freq = input("How often (seconds) do you wish to receive updates on your Telegram?")
api_key = input("Please paste your coinmarketcap API key:")
print("Great! Fetching prices....Check your Telegram....")


# parameters for the cmc api

url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
parameters = {
    'symbol': symbol,
    'convert': 'USD'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': api_key,
}


# function that gets the latest price and converts it two a two decimal floating number

def get_latest_crypto_price():
    response = requests.get(url, params=parameters, headers=headers).json()
    return float("{0:.2f}".format(
        response['data'][symbol]['quote']['USD']['price']))


# function that sends a HTTP POST request of the desired event to the webhook URL

def post_ifttt_webhook(event, value):
    data = {'value1': value}  # The payload that will be sent to IFTTT service
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    requests.post(ifttt_event_url, json=data)


def format_crypto_history(crypto_history):
    rows = []
    for crypto_price in crypto_history:
        date = crypto_price['date'].strftime('%d.%m.%Y %H:%M')  # Formats the date into a string: '24.02.2018 15:09'
        price = crypto_price['price']
        # <b> (bold) tag creates bolded text
        row = '{}: $<b>{}</b>'.format(date, price)  # 24.02.2018 15:09: $<b>10123.4</b>
        rows.append(row)

    # Use a <br> (break) tag to create a new line
    return '<br>'.join(rows)  # Join the rows delimited by <br> tag: row1<br>row2<br>row3


def main():
    crypto_history = []
    while True:
        price = get_latest_crypto_price()
        date = datetime.now()
        crypto_history.append({'date': date, 'price': price})

        # Send an emergency notification based on the desired threshold
        if price < float(CRYPTO_PRICE_THRESHOLD):
            post_ifttt_webhook('crypto_price_emergency', price)

        # Send a Telegram notification
        if len(crypto_history) == 5:  # Once we have 5 items in crypto_history send an update
            post_ifttt_webhook('crypto_price_update', format_crypto_history(crypto_history))
            # Reset the history
            crypto_history = []

        time.sleep(float(freq))  # Sleep for the selected amount of time


if __name__ == '__main__':
    main()
