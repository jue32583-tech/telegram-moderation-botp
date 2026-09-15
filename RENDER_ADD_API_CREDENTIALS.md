# 🔐 Add API Credentials to Render.com - Secure Method

## Overview

This guide shows you how to add API_ID and API_HASH to Render.com **securely** for your bot.

---

## 📋 Your Credentials

```
API_ID: [REDACTED_API_ID]
API_HASH: [REDACTED_API_HASH]
```

---

## 🔐 Security First

### Why Secure Method?

- ✅ Credentials NOT in code
- ✅ Credentials NOT in Git
- ✅ Credentials only in Render environment
- ✅ Credentials NOT visible in logs
- ✅ Production-grade security

### How It Works

```
Your Credentials
       ↓
Render Environment Variables
       ↓
Bot Code (loads securely)
       ↓
Bot Uses Credentials
```

---

## 🚀 Step-by-Step Guide

### Step 1: Go to Render Dashboard

```
https://dashboard.render.com
```

### Step 2: Select Your Bot Service

1. Click: **telegram-moderation-bot**
2. You should see your service details

### Step 3: Go to Environment Tab

1. Click: **Environment** tab
2. You'll see existing environment variables

### Step 4: Add API_ID

1. Click: **Add Environment Variable**
2. Fill in:

```
Key:   TELEGRAM_API_ID
Value: [REDACTED_API_ID]
```

3. Click: **Save**

### Step 5: Add API_HASH

1. Click: **Add Environment Variable**
2. Fill in:

```
Key:   TELEGRAM_API_HASH
Value: [REDACTED_API_HASH]
```

3. Click: **Save**

### Step 6: Verify Variables

Check that both variables are added:

```
✅ TELEGRAM_API_ID = [REDACTED_API_ID]
✅ TELEGRAM_API_HASH = [REDACTED_API_HASH]
```

### Step 7: Service Restarts Automatically

- Render automatically restarts your service
- Bot reloads with new credentials
- Check logs for: `✅ API credentials loaded`

---

## 📊 Visual Guide

```
┌─────────────────────────────────────────┐
│ Render Dashboard                        │
├─────────────────────────────────────────┤
│ telegram-moderation-bot                 │
├─────────────────────────────────────────┤
│ Environment Variables:                  │
│                                         │
│ TELEGRAM_BOT_TOKEN = ***               │
│ TELEGRAM_API_ID = [REDACTED_API_ID]              │ ← Add this
│ TELEGRAM_API_HASH = 3c7752a...         │ ← Add this
│ TELEGRAM_ADMIN_IDS = @admin1,@admin2   │
│ TELEGRAM_TARGET_CHANNELS = {...}       │
│ TELEGRAM_PRIVATE_GROUP_LINK = https... │
│ DEBUG = False                           │
│ LOG_LEVEL = INFO                        │
│                                         │
└─────────────────────────────────────────┘
```

---

## ✅ Verification

### Step 1: Check Logs

1. Go to Render Dashboard
2. Click: **telegram-moderation-bot**
3. Click: **Logs** tab
4. Look for:

```
✅ API ID loaded securely
✅ API Hash loaded securely (32 chars)
```

### Step 2: Test Bot

Send command to bot:

```
/start
```

Bot should respond:

```
🤖 Welcome to Telegram Moderation Bot!
✅ Bot is online and running
```

### Step 3: Test Status

Send command:

```
/status
```

Bot should respond:

```
📊 Bot Status:
✅ Online
✅ 11 channels configured
✅ 3 admins active
✅ API credentials loaded
```

---

## 🔍 How Bot Uses Credentials

### In Code (Secure)

```python
from secure_credentials import SecureCredentials

# Load credentials securely
api_id, api_hash = SecureCredentials.get_api_credentials()

# Bot uses credentials
if api_id and api_hash:
    print("✅ API credentials loaded")
```

### NOT in Code (Insecure)

```python
# ❌ NEVER DO THIS!
api_id = [REDACTED_API_ID]
api_hash = "[REDACTED_API_HASH]"
```

---

## 🛡️ Security Checklist

- [ ] API_ID added to Render environment
- [ ] API_HASH added to Render environment
- [ ] Service restarted automatically
- [ ] Logs show "API credentials loaded"
- [ ] Bot responds to /start
- [ ] Bot responds to /status
- [ ] Credentials NOT in code
- [ ] Credentials NOT in Git
- [ ] Credentials NOT in logs

---

## 📞 Troubleshooting

### Problem: Service Not Restarting

**Solution:**
1. Go to Render Dashboard
2. Click: **Manual Deploy**
3. Wait for restart

### Problem: Logs Show "API credentials not found"

**Solution:**
1. Check environment variables are added
2. Verify spelling: `TELEGRAM_API_ID` and `TELEGRAM_API_HASH`
3. Click: **Manual Deploy**

### Problem: Bot Still Not Working

**Solution:**
1. Check all environment variables are set
2. Review logs for errors
3. Verify bot token is correct
4. Verify bot is admin in channels

---

## 📋 All Environment Variables

After adding API credentials, you should have:

```
1. TELEGRAM_BOT_TOKEN = [REDACTED_BOT_TOKEN]
2. TELEGRAM_API_ID = [REDACTED_API_ID]
3. TELEGRAM_API_HASH = [REDACTED_API_HASH]
4. TELEGRAM_ADMIN_IDS = @waiyanphyo99,@waiyan7861,@Bingopop1991
5. TELEGRAM_TARGET_CHANNELS = {"caverpro":"@caverpro",...}
6. TELEGRAM_PRIVATE_GROUP_LINK = https://t.me/+ziCAX-uVbtlhMTk1
7. DEBUG = False
8. LOG_LEVEL = INFO
```

---

## 🎯 Next Steps

1. ✅ Add API_ID to Render
2. ✅ Add API_HASH to Render
3. ✅ Wait for service restart
4. ✅ Check logs
5. ✅ Test bot commands
6. ✅ Verify all channels working

---

## 📚 Related Documentation

- **RENDER_DEPLOYMENT_GUIDE.md** - Full deployment guide
- **API_CREDENTIALS_GUIDE.md** - API credentials security
- **secure_credentials.py** - Credentials loader code

---

## ✅ Complete!

Your bot now has:
- ✅ Bot token configured
- ✅ API_ID configured
- ✅ API_HASH configured
- ✅ All credentials secure
- ✅ Ready to use

---

**Your bot should now be working! 🎉**

**Test it in Telegram: /start**

---

**Last Updated:** 2026-07-30
**Version:** 1.0
