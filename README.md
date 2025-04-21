# Telegram Bot 2.0 for Buyer Service "KUPIDON" 

This Telegram bot is built to support the buyer-service **KUPIDON**, helping clients browse options, calculate currency conversions, and directly contact a manager. It serves as a virtual assistant for users looking to purchase goods from the USA, Europe, and Dubai.

## Features

- Interactive inline menu with navigation
- Currency conversion from USD/EUR to RUB (with margin included)
- Photo-based delivery guide by region
- Manager-client messaging system with forwarding and live chat support
- Persistent state tracking for ongoing conversations
- Clean modular code structure

## Project Structure

## Technologies Used

- Python 3.x
- [pyTelegramBotAPI (telebot)](https://github.com/eternnoir/pyTelegramBotAPI)
- [CBR Daily Currency API](https://www.cbr-xml-daily.ru/)
- Inline Keyboards and Callback Queries

## Getting Started

1. Clone the repository

```bash
git clone https://github.com/your-username/kupidon-telegram-bot.git
cd kupidon-telegram-bot

2. Install dependencies

pip install pyTelegramBotAPI requests

3. Set up configuration

Create a .env file or manually set the following values in config.py:

TOKEN = "your_telegram_bot_token"
MANAGER_CHAT_ID = 123456789  # Replace with the Telegram ID of the manager
CBR_API_URL = "https://www.cbr-xml-daily.ru/daily_json.js"
TELEGRAM_CATALOG_LINK = "https://t.me/kupidonbuyer"

4. Run the bot

python bot.py

The bot will start polling and be ready to respond to users.

Resources

Make sure to include your delivery-related images in a /resources directory as the bot uses them to display visual guides for delivery options.

Example Use Cases

	•	A client taps “💱 Конвертация валют” and gets a real-time conversion with shipping margin.
	•	A manager uses /clients to list current conversations and replies directly in Telegram.
	•	A client views delivery photos for USA and Europe before making a decision.

License

This project is licensed under the MIT License.
