# 🚀 Render.com Bot Deployment - Complete Step-by-Step Guide

## Overview

This guide will help you deploy your Telegram bot to Render.com for 24/7 operation.

**Time Required:** 10-15 minutes
**Cost:** $7/month (Starter plan)
**Uptime:** 99.9%

---

## 📋 Prerequisites

Before starting, make sure you have:

- ✅ GitHub account with bot repository
- ✅ Render.com account (free signup)
- ✅ Bot token: `[REDACTED_BOT_TOKEN]`
- ✅ API_ID: `[REDACTED_API_ID]`
- ✅ API_HASH: `[REDACTED_API_HASH]`

---

## 🎯 Step 1: Create Render Account

### 1.1 Go to Render.com
```
https://render.com
```

### 1.2 Click "Sign Up"
- Choose: **Sign up with GitHub**
- This makes deployment easier!

### 1.3 Authorize GitHub
- Click: **Authorize render-oss**
- Confirm your GitHub account

### 1.4 Complete Signup
- Enter your email
- Verify email
- Done! ✅

---

## 🔗 Step 2: Connect GitHub Repository

### 2.1 Go to Render Dashboard
```
https://dashboard.render.com
```

### 2.2 Click "New +"
- Top right corner
- Select: **Web Service**

### 2.3 Connect GitHub
1. Click: **Connect GitHub**
2. Search: `telegram-moderation-bot`
3. Click: **Connect**
4. Authorize Render to access your repo

### 2.4 Select Repository
- Choose: `jue32583-tech/telegram-moderation-bot`
- Click: **Connect**

---

## ⚙️ Step 3: Configure Web Service

### 3.1 Basic Settings

Fill in these fields:

| Field | Value |
|-------|-------|
| **Name** | `telegram-moderation-bot` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python bot_production.py` |
| **Plan** | `Starter ($7/month)` |
| **Region** | `Singapore` (or your preferred region) |

### 3.2 Example Screenshot

```
┌─────────────────────────────────────────┐
│ Name: telegram-moderation-bot           │
│ Environment: Python 3                   │
│ Build: pip install -r requirements.txt  │
│ Start: python bot_production.py         │
│ Plan: Starter ($7/month)                │
│ Region: Singapore                       │
└─────────────────────────────────────────┘
```

---

## 🔐 Step 4: Add Environment Variables

### 4.1 Scroll Down to "Environment"

Click: **Add Environment Variable**

### 4.2 Add Bot Token

```
Key:   TELEGRAM_BOT_TOKEN
Value: [REDACTED_BOT_TOKEN]
```

Click: **Add**

### 4.3 Add API Credentials

```
Key:   TELEGRAM_API_ID
Value: [REDACTED_API_ID]
```

Click: **Add**

```
Key:   TELEGRAM_API_HASH
Value: [REDACTED_API_HASH]
```

Click: **Add**

### 4.4 Add Admin IDs

```
Key:   TELEGRAM_ADMIN_IDS
Value: @waiyanphyo99,@waiyan7861,@Bingopop1991
```

Click: **Add**

### 4.5 Add Target Channels

```
Key:   TELEGRAM_TARGET_CHANNELS
Value: {"caverpro":"@caverpro","onepiecemmk":"@onepiecemmk","allmovie00099":"@allmovie00099","channeliingo":"@channeliingo","channelningo":"@channelningo","channelhingo":"@channelhingo","channelaingo":"@channelaingo","channeldogo":"@channeldogo","chatCGAi":"@chatCGAi","chanpingo":"@chanpingo","Cartoonmovie2002":"@Cartoonmovie2002"}
```

Click: **Add**

### 4.6 Add Private Group Link

```
Key:   TELEGRAM_PRIVATE_GROUP_LINK
Value: https://t.me/+ziCAX-uVbtlhMTk1
```

Click: **Add**

### 4.7 Add Debug Mode

```
Key:   DEBUG
Value: False
```

Click: **Add**

### 4.8 Add Log Level

```
Key:   LOG_LEVEL
Value: INFO
```

Click: **Add**

---

## 📊 Step 5: Review Configuration

### 5.1 Check All Settings

Before deploying, verify:

- ✅ Name: `telegram-moderation-bot`
- ✅ Environment: `Python 3`
- ✅ Build Command: `pip install -r requirements.txt`
- ✅ Start Command: `python bot_production.py`
- ✅ Plan: `Starter ($7/month)`
- ✅ All 8 environment variables added
- ✅ No typos in values

### 5.2 Environment Variables Checklist

- [ ] TELEGRAM_BOT_TOKEN
- [ ] TELEGRAM_API_ID
- [ ] TELEGRAM_API_HASH
- [ ] TELEGRAM_ADMIN_IDS
- [ ] TELEGRAM_TARGET_CHANNELS
- [ ] TELEGRAM_PRIVATE_GROUP_LINK
- [ ] DEBUG
- [ ] LOG_LEVEL

---

## 🚀 Step 6: Deploy Service

### 6.1 Click "Create Web Service"

- Bottom right corner
- Wait for deployment to start

### 6.2 Monitor Deployment

The deployment process:

1. **Building** (1-2 minutes)
   - Render clones your repository
   - Installs dependencies
   - Builds the service

2. **Starting** (30-60 seconds)
   - Service starts
   - Bot initializes
   - Connects to Telegram

3. **Live** ✅
   - Service is running
   - Bot is active
   - Ready to use

### 6.3 Check Deployment Status

- Status should show: **Live** (green)
- URL shows your service URL
- Logs show startup messages

---

## 📊 Step 7: Monitor Logs

### 7.1 View Logs

1. Go to Render Dashboard
2. Click: `telegram-moderation-bot`
3. Click: **Logs** tab
4. Watch real-time logs

### 7.2 Expected Log Messages

```
✅ Bot Token: Loaded
✅ API ID: Loaded
✅ API Hash: Loaded
✅ Channels: 11 configured
✅ Admins: 3 configured
✅ Bot started successfully!
```

### 7.3 Common Startup Messages

```
2026-07-30 12:00:00 - INFO - 🤖 TELEGRAM BOT STARTING
2026-07-30 12:00:01 - INFO - ✅ Bot Token loaded
2026-07-30 12:00:02 - INFO - ✅ API credentials loaded
2026-07-30 12:00:03 - INFO - ✅ 11 channels configured
2026-07-30 12:00:04 - INFO - ✅ 3 admins configured
2026-07-30 12:00:05 - INFO - ✅ Bot started successfully!
```

---

## 🧪 Step 8: Test Bot

### 8.1 Open Telegram

Find your bot and send commands:

```
/start
```

**Expected Response:**
```
🤖 Welcome to Telegram Moderation Bot!
✅ Bot is online and running
```

### 8.2 Test Status Command

```
/status
```

**Expected Response:**
```
📊 Bot Status:
✅ Online
✅ 11 channels configured
✅ 3 admins active
```

### 8.3 Test Channels Command

```
/channels
```

**Expected Response:**
```
📡 Configured Channels:
1. @caverpro
2. @onepiecemmk
3. @allmovie00099
... (all 11 channels)
```

### 8.4 Test Admin Command

```
/admins
```

**Expected Response:**
```
👥 Admin Users:
1. @waiyanphyo99
2. @waiyan7861
3. @Bingopop1991
```

### 8.5 Test Post Command (Admin Only)

```
/post Hello everyone! Test message from Render.
```

**Expected Result:**
- Bot posts to all 11 channels
- Check each channel for the message

---

## 🔄 Step 9: Verify All Channels

### 9.1 Check Each Channel

1. @caverpro - ✅ Message received
2. @onepiecemmk - ✅ Message received
3. @allmovie00099 - ✅ Message received
4. @channeliingo - ✅ Message received
5. @channelningo - ✅ Message received
6. @channelhingo - ✅ Message received
7. @channelaingo - ✅ Message received
8. @channeldogo - ✅ Message received
9. @chatCGAi - ✅ Message received
10. @chanpingo - ✅ Message received
11. @Cartoonmovie2002 - ✅ Message received

---

## 📊 Step 10: Monitor & Maintain

### 10.1 Daily Monitoring

- Check Render Dashboard daily
- Review logs for errors
- Monitor bot activity

### 10.2 Weekly Maintenance

- Test all commands
- Verify all channels working
- Check for any issues

### 10.3 Monthly Tasks

- Review logs for patterns
- Check resource usage
- Plan upgrades if needed

---

## 🛠️ Troubleshooting

### Problem: Bot Not Starting

**Check Logs:**
```
Go to Logs tab and look for errors
```

**Common Issues:**
```
❌ TELEGRAM_BOT_TOKEN not found
   → Add to environment variables

❌ Invalid token format
   → Verify token is correct

❌ Connection error
   → Check internet connection
```

### Problem: Bot Not Responding

**Check:**
1. Bot status in Render Dashboard (should be "Live")
2. Logs for any errors
3. Bot token is correct
4. Bot is admin in channels

### Problem: Posts Not Appearing

**Check:**
1. Bot is admin in all channels
2. Bot has "Send Messages" permission
3. Channel names are correct
4. No typos in channel names

### Problem: Deployment Failed

**Check:**
1. All dependencies in requirements.txt
2. Python version compatible
3. No syntax errors in code
4. GitHub repository is public or Render has access

---

## 📞 Getting Help

### Render Support
- https://render.com/support
- Email: support@render.com

### Telegram Bot API
- https://core.telegram.org/bots/api
- Documentation: https://core.telegram.org/bots

### GitHub Issues
- https://github.com/jue32583-tech/telegram-moderation-bot/issues

---

## 💰 Pricing & Costs

### Render.com Plans

| Plan | Price | CPU | RAM | Best For |
|------|-------|-----|-----|----------|
| Free | $0 | 0.1 | 512MB | Testing |
| Starter | $7/month | 0.5 | 512MB | Bot (Recommended) |
| Standard | $12/month | 1 | 1GB | Production |
| Pro | $29/month | 2 | 4GB | High Traffic |

**Recommended:** Starter ($7/month) for 24/7 bot operation

### Total Cost
```
Bot Hosting: $7/month
Telegram Bot API: Free
Total: $7/month
```

---

## ✅ Deployment Checklist

### Before Deployment
- [ ] GitHub repository created
- [ ] Bot code ready
- [ ] requirements.txt updated
- [ ] .env file configured locally
- [ ] Bot tested locally

### During Deployment
- [ ] Render account created
- [ ] GitHub connected
- [ ] Service configured
- [ ] All 8 environment variables added
- [ ] Build command correct
- [ ] Start command correct
- [ ] Plan selected (Starter)

### After Deployment
- [ ] Deployment successful (status: Live)
- [ ] Logs show "Bot started successfully!"
- [ ] /start command works
- [ ] /status command works
- [ ] /channels command works
- [ ] /post command works
- [ ] Messages appear in all 11 channels
- [ ] Bot responds to all admins

---

## 🎉 Success!

Your bot is now:
- ✅ Deployed to Render.com
- ✅ Running 24/7
- ✅ Monitoring 11 channels
- ✅ Managed by 3 admins
- ✅ Auto-forwarding posts
- ✅ Filtering inappropriate content
- ✅ Welcoming new members

---

## 📚 Next Steps

1. **Monitor Bot**
   - Check logs regularly
   - Verify all commands working
   - Monitor channel activity

2. **Update Bot**
   - Make changes to code
   - Push to GitHub
   - Render automatically redeploys

3. **Scale Up**
   - If needed, upgrade to Standard plan
   - Add more channels
   - Add more admins

4. **Maintain Security**
   - Rotate credentials every 90 days
   - Keep dependencies updated
   - Monitor for suspicious activity

---

## 📖 Additional Resources

- **Render Docs:** https://render.com/docs
- **Telegram Bot API:** https://core.telegram.org/bots/api
- **Python Telegram Bot:** https://github.com/python-telegram-bot/python-telegram-bot
- **GitHub Repository:** https://github.com/jue32583-tech/telegram-moderation-bot

---

## 🎯 Quick Reference

### Render Dashboard
```
https://dashboard.render.com
```

### Your Bot Service
```
https://dashboard.render.com/web/telegram-moderation-bot
```

### GitHub Repository
```
https://github.com/jue32583-tech/telegram-moderation-bot
```

### Telegram Bot
```
Search for: Movie Auto Forward
```

---

**Last Updated:** 2026-07-30
**Version:** 1.0
**Status:** ✅ Complete & Ready

---

**Happy Deploying! 🚀**
