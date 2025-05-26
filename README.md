# Telegram Channel Manager

A Telegram bot for managing channels and communicating with members efficiently.

## Features
- Channel member management
- Backup member lists
- Smart message broadcasting
- Multi-channel support

## Setup
1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables in `.env`:
```env
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
```

3. Run the bot:
```bash
python main.py
```

## Project Structure
- `bot/`: Main bot modules
  - `handler/`: Command handlers
    - `start/`: Start command
    - `help/`: Help command
- `docs/`: Project documentation
