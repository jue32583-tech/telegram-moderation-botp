# 🚀 Render.com Complete Deployment Guide

## အလွယ်အသုံးပြုနိုင်တဲ့ Step-by-Step Guide

---

## 📋 Table of Contents

1. [Render Account ဖန်တီးခြင်း](#1-render-account-ဖန်တီးခြင်း)
2. [GitHub Repository ချိတ်ဆက်ခြင်း](#2-github-repository-ချိတ်ဆက်ခြင်း)
3. [Service Configure လုပ်ခြင်း](#3-service-configure-လုပ်ခြင်း)
4. [Environment Variables ထည့်သွင်းခြင်း](#4-environment-variables-ထည့်သွင်းခြင်း)
5. [Deploy လုပ်ခြင်း](#5-deploy-လုပ်ခြင်း)
6. [Channels ထည့်သွင်းခြင်း](#6-channels-ထည့်သွင်းခြင်း)
7. [Monitoring & Troubleshooting](#7-monitoring--troubleshooting)

---

## 1. Render Account ဖန်တီးခြင်း

### Step 1.1: Sign Up

1. **https://render.com** သို့ သွားပါ
2. **"Sign Up"** ကလစ်လုပ်ပါ
3. **GitHub နဲ့ Sign Up** ရွေးချယ်ပါ (အလွယ်ဆုံး)

![Sign Up](https://render.com/images/sign-up.png)

### Step 1.2: GitHub Authorization

1. **"Authorize render"** ကလစ်လုပ်ပါ
2. GitHub password ထည့်သွင်းပါ
3. Authorization အတည်ပြုပါ

### Step 1.3: Email Verification

1. Email ကို ကြည့်ပါ
2. Verification link ကလစ်လုပ်ပါ
3. Account ready!

✅ **Render Account ဖန်တီးပြီး!**

---

## 2. GitHub Repository ချိတ်ဆက်ခြင်း

### Step 2.1: Go to Render Dashboard

1. **Render Dashboard** သို့ သွားပါ
2. **"New +"** ကလစ်လုပ်ပါ
3. **"Web Service"** ရွေးချယ်ပါ

![New Service](https://render.com/images/new-service.png)

### Step 2.2: Connect GitHub Repository

1. **"Connect a repository"** ကလစ်လုပ်ပါ
2. GitHub account ကို authorize လုပ်ပါ
3. **"jue32583-tech/telegram-moderation-bot"** ရှာပါ
4. **"Connect"** ကလစ်လုပ်ပါ

![Connect Repo](https://render.com/images/connect-repo.png)

### Step 2.3: Select Repository

```
Search: telegram-moderation-bot
↓
Click on: jue32583-tech/telegram-moderation-bot
↓
Click: Connect
```

✅ **GitHub Repository ချိတ်ဆက်ပြီး!**

---

## 3. Service Configure လုပ်ခြင်း

### Step 3.1: Basic Configuration

Fill in the following fields:

| Field | Value |
|-------|-------|
| **Name** | `telegram-moderation-bot` |
| **Environment** | `Python 3` |
| **Region** | `Singapore` (or nearest) |
| **Branch** | `master` |

### Step 3.2: Build Settings

**Build Command:**
```bash
pip install -r requirements.txt
```

**Start Command:**
```bash
python bot.py
```

### Step 3.3: Instance Type

**Choose Plan:**
- 🆓 **Free** - Testing အတွက် (spins down after 15 min)
- 💰 **Starter** - $7/month (24/7 running) - အကြံပြုချက်

```
For production: Choose "Starter" ($7/month)
For testing: Choose "Free"
```

### Step 3.4: Review Configuration

```
Name: telegram-moderation-bot
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: python bot.py
Instance: Starter ($7/month)
```

✅ **Configuration အကြည့်အလည် ပြီး!**

---

## 4. Environment Variables ထည့်သွင်းခြင်း

### Step 4.1: Go to Environment Section

1. **"Environment"** tab ကလစ်လုပ်ပါ
2. **"Add Environment Variable"** ကလစ်လုပ်ပါ

### Step 4.2: Add BOT_TOKEN

| Key | Value |
|-----|-------|
| `BOT_TOKEN` | `[REDACTED_BOT_TOKEN]` |

**Steps:**
1. Key field မှာ: `BOT_TOKEN`
2. Value field မှာ: `[REDACTED_BOT_TOKEN]`
3. **"Add"** ကလစ်လုပ်ပါ

### Step 4.3: Add ADMIN_IDS (Optional)

| Key | Value |
|-----|-------|
| `ADMIN_IDS` | `123456789,987654321` |

**Steps:**
1. Key field မှာ: `ADMIN_IDS`
2. Value field မှာ: `123456789,987654321` (comma-separated)
3. **"Add"** ကလစ်လုပ်ပါ

### Step 4.4: Environment Variables Summary

```
✅ BOT_TOKEN = [REDACTED_BOT_TOKEN]
✅ ADMIN_IDS = 123456789,987654321
```

✅ **Environment Variables ထည့်သွင်းပြီး!**

---

## 5. Deploy လုပ်ခြင်း

### Step 5.1: Create Service

1. **"Create Web Service"** ကလစ်လုပ်ပါ
2. Deployment စတင်ပါတယ် (2-3 minutes စောင့်ဆိုင်းပါ)

### Step 5.2: Monitor Deployment

```
Deployment Status:
↓
Building... (1-2 min)
↓
Running... (success!)
```

### Step 5.3: Check Logs

1. **"Logs"** tab ကလစ်လုပ်ပါ
2. ရှာပါ:
```
🤖 TELEGRAM MODERATION BOT STARTED
Listening for messages...
```

### Step 5.4: Verify Deployment

```
✅ Service is running
✅ No errors in logs
✅ Bot is listening
```

✅ **Bot Render မှာ Deploy ဖြစ်ပြီး!**

---

## 6. Channels ထည့်သွင်းခြင်း

### Step 6.1: Get Your Bot Username

1. Telegram မှာ bot ရှာပါ
2. Bot username ကို copy လုပ်ပါ
3. Example: `@my_moderation_bot`

### Step 6.2: Get Channel IDs

#### Public Channel ID

**Using @userinfobot:**
1. Telegram မှာ `@userinfobot` ရှာပါ
2. `/start` ပို့ပါ
3. Public channel မှ message forward လုပ်ပါ
4. Bot ကို channel ID ပြပေးမှာ ဖြစ်ပါတယ်
5. Format: `@channel_name`

#### Private Channel ID

**Using @userinfobot:**
1. Telegram မှာ `@userinfobot` ရှာပါ
2. `/start` ပို့ပါ
3. Private channel မှ message forward လုပ်ပါ
4. Bot ကို negative number ပြပေးမှာ ဖြစ်ပါတယ်
5. Format: `-1001234567890`

### Step 6.3: Add Bot to Channels

**For Each Channel:**

1. Channel ကို ဖွင့်ပါ
2. Channel name ကလစ်လုပ်ပါ
3. **"Edit Channel"** ကလစ်လုပ်ပါ
4. **"Administrators"** သို့ သွားပါ
5. **"Add Administrator"** ကလစ်လုပ်ပါ
6. Bot ရှာပါ
7. **"Add"** ကလစ်လုပ်ပါ

### Step 6.4: Grant Permissions

Bot အတွက် enable လုပ်ပါ:

```
✅ Delete messages
✅ Ban users
✅ Send messages
✅ Pin messages
```

### Step 6.5: Add Channels via Bot Commands

Telegram မှာ bot ကို message ပို့ပါ:

**Public Channel:**
```
/addchannel NewsChannel @breaking_news
```

**Private Channel:**
```
/addchannel AdminChannel -1001234567890
```

### Step 6.6: Verify Channels

```
/channels
```

Output:
```
📡 Configured Channels:

1. 🌍 Public: NewsChannel
2. 🔒 Private: AdminChannel
```

✅ **Channels ထည့်သွင်းပြီး!**

---

## 7. Monitoring & Troubleshooting

### Step 7.1: Monitor Logs

1. **Render Dashboard** သို့ သွားပါ
2. Your service ရွေးချယ်ပါ
3. **"Logs"** ကလစ်လုပ်ပါ
4. Real-time logs ကြည့်ပါ

### Step 7.2: Common Issues

#### Issue 1: Bot Not Starting

**Symptoms:**
```
ModuleNotFoundError: No module named 'telegram'
```

**Solution:**
1. GitHub မှာ `requirements.txt` ကြည့်ပါ
2. `python-telegram-bot` ပါဝင်ခြင်း ကြည့်ပါ
3. Update လုပ်ပြီး push လုပ်ပါ
4. Render အလိုအလျောက် redeploy ဖြစ်ပါတယ်

#### Issue 2: Invalid Token Error

**Symptoms:**
```
Error: Invalid token
```

**Solution:**
1. Render Dashboard သို့ သွားပါ
2. Environment variables ကြည့်ပါ
3. BOT_TOKEN မှန်ကန်ခြင်း ကြည့်ပါ
4. Update လုပ်ပါ
5. Manual Deploy ကလစ်လုပ်ပါ

#### Issue 3: Bot Can't Post to Channel

**Symptoms:**
```
Error posting to channel
```

**Solution:**
1. Bot ကို channel မှာ administrator အဖြစ် ထည့်သွင်းပါ
2. Permissions enable လုပ်ပါ
3. Channel ID မှန်ကန်ခြင်း ကြည့်ပါ
4. `/channels` ကြည့်ပါ

### Step 7.3: Test Bot

**Test 1: Welcome Message**
```
1. Bot ကို channel မှာ add လုပ်ပါ
2. New user join လုပ်ပါ
3. Welcome message ရမှာ ဖြစ်ပါတယ်
```

**Test 2: Content Filtering**
```
1. "spam" ဆိုတဲ့ စာသား ပို့ပါ
2. Message delete ဖြစ်ပါတယ်
3. Warning message ရပါတယ်
```

**Test 3: Multi-Channel Posting**
```
1. /post Hello everyone!
2. Message အားလုံး channels မှာ ပြပေးမှာ ဖြစ်ပါတယ်
```

### Step 7.4: Manual Deploy

Code update လုပ်ပြီး redeploy လုပ်ရန်:

1. **Render Dashboard** သို့ သွားပါ
2. Your service ရွေးချယ်ပါ
3. **"Manual Deploy"** ကလစ်လုပ်ပါ
4. **"Deploy latest commit"** ကလစ်လုပ်ပါ
5. Deployment စောင့်ဆိုင်းပါ

---

## ✅ Complete Deployment Checklist

### Pre-Deployment

- [ ] Render account ဖန်တီးပြီး
- [ ] GitHub repository ချိတ်ဆက်ပြီး
- [ ] BOT_TOKEN ရယူပြီး
- [ ] ADMIN_IDs ကြည့်ပြီး

### Deployment

- [ ] Service name ထည့်သွင်းပြီး
- [ ] Build command မှန်ကန်ပြီး
- [ ] Start command မှန်ကန်ပြီး
- [ ] Environment variables ထည့်သွင်းပြီး
- [ ] Service create လုပ်ပြီး
- [ ] Deployment successful ပြီး

### Post-Deployment

- [ ] Logs ကြည့်ပြီး (no errors)
- [ ] Bot ကို channels မှာ add လုပ်ပြီး
- [ ] Permissions enable လုပ်ပြီး
- [ ] Channels ထည့်သွင်းပြီး (`/addchannel`)
- [ ] `/channels` verify လုပ်ပြီး
- [ ] `/post` test လုပ်ပြီး

---

## 🎯 Quick Reference

### Render Dashboard Links

```
Dashboard: https://dashboard.render.com
Services: https://dashboard.render.com/services
Settings: https://dashboard.render.com/settings
```

### Important Commands

```bash
# View logs
tail -f telegram_bot.log

# Test bot locally
python bot.py

# Check GitHub status
git status
git log --oneline
```

### Environment Variables

```
BOT_TOKEN = [REDACTED_BOT_TOKEN]
ADMIN_IDS = 123456789,987654321
```

### Bot Commands

```
/start - Bot information
/rules - Channel rules
/channels - List channels
/addchannel - Add channel
/post - Post to channels
/stats - Statistics
```

---

## 💰 Pricing

| Plan | Price | Features |
|------|-------|----------|
| Free | $0 | Spins down after 15 min |
| Starter | $7/month | 24/7 running |
| Standard | $25/month | More resources |

**Recommendation:** Starter plan ($7/month) for 24/7 bot running

---

## 🆘 Support & Resources

### Render Support

- **Docs:** https://render.com/docs
- **Status:** https://status.render.com
- **Support:** https://render.com/support

### Bot Resources

- **GitHub:** https://github.com/jue32583-tech/telegram-moderation-bot
- **Telegram Bot API:** https://core.telegram.org/bots/api
- **python-telegram-bot:** https://python-telegram-bot.readthedocs.io

---

## 🎉 Success!

Bot သည် Render.com မှာ 24/7 running ဖြစ်ပြီး ကောင်းကောင်း! 🚀

**Next Steps:**
1. ✅ Render.com မှာ deploy လုပ်ပါ
2. ✅ Channels ထည့်သွင်းပါ
3. ✅ Features test လုပ်ပါ
4. ✅ Logs monitor လုပ်ပါ
5. ✅ Community မှာ share လုပ်ပါ

---

## 📞 Need Help?

### Troubleshooting Steps

1. **Check logs** in Render Dashboard
2. **Verify environment variables**
3. **Check GitHub repository**
4. **Test locally** with `python bot.py`
5. **Contact support** if issues persist

---

**Happy Deploying! 🚀**
