# Configuration Guide

## Setup Steps

### 1. Get Bot Token

1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Follow the prompts
4. Copy the token

### 2. Get Channel IDs

1. Search for **@userinfobot** on Telegram
2. Send `/start`
3. Forward a message from your channel
4. Bot will show the channel ID

### 3. Get Admin User ID

1. Search for **@userinfobot** on Telegram
2. Send `/start`
3. Bot will show your user ID

## Edit bot.py

```python
# Line 1: Add your bot token
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# Line 2: Add target channels (optional)
TARGET_CHANNELS = [
    -1001234567890,  # Channel 1
    -1001234567891,  # Channel 2
]

# Line 3: Add admin IDs (optional)
ADMIN_IDS = [123456789]

# Line 4: Customize banned words (optional)
BANNED_WORDS = [
    r'\b(spam|scam)\b',
    r'(http|https):\/\/[^\s]+',
]
```

## Install & Run

```bash
# Install dependencies
pip install -r requirements.txt

# Run bot
python bot.py
```

## Add Bot to Channel

1. Open Telegram channel
2. Click channel name
3. Tap "Add Members"
4. Search for your bot
5. Add it
6. Make bot an administrator
7. Enable "Delete messages" permission

## Test Bot

1. Send `/start` in channel
2. Send `/rules` in channel
3. Test content filtering with "spam"
4. Test `/post` command (admin only)

## Troubleshooting

**Bot not responding?**
- Check if running
- Check logs: `tail -f telegram_bot.log`
- Verify token

**Can't delete messages?**
- Make bot administrator
- Enable permissions

**Messages not filtering?**
- Check banned words patterns
- Test at regex101.com

## Advanced Configuration

### Custom Welcome Message

Edit `WELCOME_MESSAGE`:

```python
WELCOME_MESSAGE = """
🎉 Welcome to {channel_name}!
Hello {user_name}!
📋 Your custom rules...
"""
```

### Add More Channels

Edit `TARGET_CHANNELS`:

```python
TARGET_CHANNELS = [
    -1001234567890,
    -1001234567891,
    -1001234567892,
    -1001234567893,
    -1001234567894,
]
```

### Add More Admins

Edit `ADMIN_IDS`:

```python
ADMIN_IDS = [
    123456789,
    987654321,
    111111111,
]
```

### Custom Banned Words

Edit `BANNED_WORDS`:

```python
BANNED_WORDS = [
    r'\b(word1|word2|word3)\b',
    r'pattern_here',
    r'another_pattern',
]
```

## Running 24/7

### Option 1: Screen (Linux/Mac)

```bash
screen -S telegram-bot
python bot.py
# Ctrl+A, then D to detach
```

### Option 2: Systemd (Linux)

Create `/etc/systemd/system/telegram-bot.service`:

```ini
[Unit]
Description=Telegram Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/path/to/bot
ExecStart=/usr/bin/python3 /path/to/bot/bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
```

### Option 3: Docker

```bash
docker build -t telegram-bot .
docker run -d telegram-bot
```

## Monitoring

View logs:
```bash
tail -f telegram_bot.log
```

Check if running:
```bash
ps aux | grep bot.py
```

## Data Files

- `telegram_bot.log` - Bot activity log
- `bot_data.json` - User warning data

## Security

⚠️ **Important:**
- Never share your bot token
- Don't commit token to GitHub
- Use environment variables in production

## Support

For issues:
1. Check logs
2. Verify configuration
3. Test bot permissions
4. Check Telegram API status
