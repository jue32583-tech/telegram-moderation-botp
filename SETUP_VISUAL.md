# 📊 Visual Setup Guide

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Your Telegram Channels                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │   Public 1   │  │   Public 2   │  │   Private 1  │       │
│  │  @news_ch    │  │  @updates_ch │  │  -100123456  │       │
│  └──────────────┘  └──────────────┘  └──────────────┘       │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Messages
                         ▼
┌─────────────────────────────────────────────────────────────┐
│           Telegram Moderation Bot (Render.com)              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  • Welcome Messages                                 │   │
│  │  • Content Filtering                                │   │
│  │  • Warning System (3-Strike)                        │   │
│  │  • Multi-Channel Posting                            │   │
│  │  • Admin Commands                                   │   │
│  └─────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ Logs & Data
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              GitHub Repository (Backup)                      │
│  • bot.py                                                    │
│  • requirements.txt                                          │
│  • bot_data.json (warnings)                                 │
│  • telegram_bot.log                                          │
└─────────────────────────────────────────────────────────────┘
```

---

## Deployment Flow

```
START
  │
  ├─► 1. Create Render Account
  │     └─► Sign up with GitHub
  │
  ├─► 2. Connect GitHub Repository
  │     └─► jue32583-tech/telegram-moderation-bot
  │
  ├─► 3. Configure Service
  │     ├─► Name: telegram-moderation-bot
  │     ├─► Environment: Python 3
  │     ├─► Build: pip install -r requirements.txt
  │     ├─► Start: python bot.py
  │     └─► Plan: Starter ($7/month)
  │
  ├─► 4. Add Environment Variables
  │     ├─► BOT_TOKEN = your_token
  │     └─► ADMIN_IDS = your_id
  │
  ├─► 5. Deploy Service
  │     └─► Click "Create Web Service"
  │
  ├─► 6. Monitor Logs
  │     └─► Check: "BOT STARTED"
  │
  ├─► 7. Add Channels
  │     ├─► Get channel IDs
  │     └─► /addchannel Name ID
  │
  ├─► 8. Test Bot
  │     ├─► /channels
  │     ├─► /post Hello
  │     └─► Check logs
  │
  └─► SUCCESS! ✅
```

---

## Channel Setup Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    Get Channel ID                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Public Channel:                                             │
│  ├─► Telegram: @userinfobot                                │
│  ├─► /start                                                │
│  ├─► Forward message from public channel                   │
│  └─► ID: @channel_name                                     │
│                                                              │
│  Private Channel:                                            │
│  ├─► Telegram: @userinfobot                                │
│  ├─► /start                                                │
│  ├─► Forward message from private channel                  │
│  └─► ID: -1001234567890                                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Add Bot to Channel                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Open Channel                                             │
│  2. Channel name → Edit Channel                             │
│  3. Administrators → Add Administrator                      │
│  4. Search for your bot                                     │
│  5. Add bot                                                 │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│               Grant Bot Permissions                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ✅ Delete messages                                         │
│  ✅ Ban users                                               │
│  ✅ Send messages                                           │
│  ✅ Pin messages                                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│            Add Channel via Bot Command                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Public:  /addchannel News @breaking_news                   │
│  Private: /addchannel Admin -1001234567890                  │
│                                                              │
│  Verify:  /channels                                         │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Bot Features Flow

```
Message Received
  │
  ├─► Check if Admin
  │   ├─► YES → Skip moderation
  │   └─► NO → Continue
  │
  ├─► Check Content
  │   ├─► Banned words?
  │   ├─► URLs?
  │   ├─► Spam?
  │   └─► Other violations?
  │
  ├─► If Clean
  │   └─► Message stays ✅
  │
  └─► If Violation
      ├─► Delete message
      ├─► Add warning (1/3)
      ├─► Send warning message
      │
      ├─► If 3 warnings
      │   ├─► Ban user
      │   └─► Send removal notice
      │
      └─► Save data to bot_data.json
```

---

## Admin Command Flow

```
Admin sends command
  │
  ├─► /start
  │   └─► Show bot information
  │
  ├─► /rules
  │   └─► Show channel rules
  │
  ├─► /channels
  │   └─► List all configured channels
  │
  ├─► /addchannel Name ID
  │   ├─► Add channel
  │   └─► Save to configuration
  │
  ├─► /post Message
  │   ├─► Send to all channels
  │   └─► Log action
  │
  ├─► /status
  │   └─► Show bot status
  │
  └─► /stats
      └─► Show violation statistics
```

---

## Monitoring Dashboard

```
┌─────────────────────────────────────────────────────────────┐
│              Render.com Dashboard                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Service: telegram-moderation-bot                           │
│  Status: ✅ Running                                         │
│  Plan: Starter ($7/month)                                   │
│  Region: Singapore                                          │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Logs (Real-time)                                      │ │
│  ├───────────────────────────────────────────────────────┤ │
│  │ 2026-01-18 13:00:00 - BOT STARTED                    │ │
│  │ 2026-01-18 13:00:05 - New member joined               │ │
│  │ 2026-01-18 13:00:10 - Welcome message sent            │ │
│  │ 2026-01-18 13:00:15 - Message approved                │ │
│  │ 2026-01-18 13:00:20 - Violation detected              │ │
│  │ 2026-01-18 13:00:25 - Warning sent                    │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                              │
│  ┌───────────────────────────────────────────────────────┐ │
│  │ Metrics                                               │ │
│  ├───────────────────────────────────────────────────────┤ │
│  │ CPU: 5%                                               │ │
│  │ Memory: 45 MB                                         │ │
│  │ Uptime: 24h 15m                                       │ │
│  └───────────────────────────────────────────────────────┘ │
│                                                              │
│  [Manual Deploy] [View Logs] [Settings]                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Quick Command Reference

```
┌─────────────────────────────────────────────────────────────┐
│                    Bot Commands                              │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  PUBLIC COMMANDS                                             │
│  ├─► /start      → Show bot information                     │
│  ├─► /rules      → Display channel rules                    │
│  ├─► /channels   → List all channels                        │
│  └─► /help       → Show help message                        │
│                                                              │
│  ADMIN COMMANDS                                              │
│  ├─► /status     → Show bot status                          │
│  ├─► /addchannel → Add a channel                            │
│  ├─► /removechannel → Remove a channel                      │
│  ├─► /post       → Post to all channels                     │
│  └─► /stats      → Show statistics                          │
│                                                              │
│  EXAMPLES                                                    │
│  ├─► /addchannel News @breaking_news                        │
│  ├─► /addchannel Admin -1001234567890                       │
│  ├─► /post 🎉 Important announcement!                       │
│  └─► /channels                                              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Troubleshooting Decision Tree

```
Bot Not Working?
  │
  ├─► Check Logs
  │   ├─► Error messages?
  │   │   ├─► ModuleNotFoundError
  │   │   │   └─► Fix: Update requirements.txt
  │   │   ├─► Invalid token
  │   │   │   └─► Fix: Check BOT_TOKEN env var
  │   │   └─► Connection error
  │   │       └─► Fix: Check internet connection
  │   │
  │   └─► No errors?
  │       └─► Continue below
  │
  ├─► Check Configuration
  │   ├─► BOT_TOKEN set?
  │   ├─► ADMIN_IDS set?
  │   └─► Channels added?
  │
  ├─► Check Permissions
  │   ├─► Bot is administrator?
  │   ├─► Delete messages enabled?
  │   └─► Ban users enabled?
  │
  ├─► Test Bot
  │   ├─► /start
  │   ├─► /channels
  │   └─► /post test
  │
  └─► Still not working?
      └─► Check GitHub issues or contact support
```

---

## Setup Time Estimate

```
┌─────────────────────────────────────────────────────────────┐
│                    Time Breakdown                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Create Render Account        ⏱️  2 minutes              │
│  2. Connect GitHub               ⏱️  1 minute               │
│  3. Configure Service            ⏱️  3 minutes              │
│  4. Add Environment Variables    ⏱️  2 minutes              │
│  5. Deploy                       ⏱️  3 minutes              │
│  6. Get Channel IDs              ⏱️  5 minutes              │
│  7. Add Channels                 ⏱️  5 minutes              │
│  8. Test Bot                     ⏱️  3 minutes              │
│                                                              │
│  TOTAL TIME: ~24 minutes                                     │
│                                                              │
│  ✅ Bot is now running 24/7!                               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Success Indicators

```
✅ Bot is deployed successfully when:

1. Render Dashboard shows "Running" status
2. Logs show "BOT STARTED" message
3. Bot responds to /start command
4. /channels shows your channels
5. /post successfully sends messages
6. Welcome messages appear for new members
7. Content filtering works
8. Logs show no errors

🎉 Congratulations! Your bot is ready!
```

---

**Visual Guide Complete! 📊**
