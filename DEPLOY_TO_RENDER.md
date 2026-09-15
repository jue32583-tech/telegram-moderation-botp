# 🚀 Deploy Bot to Render.com - Step by Step

## Bot Configuration

✅ **11 Channels Pre-configured:**
1. @caverpro
2. @onepiecemmk
3. @allmovie00099
4. @channeliingo
5. @channelningo
6. @channelhingo
7. @channelaingo
8. @channeldogo
9. @chatCGAi
10. @chanpingo
11. @Cartoonmovie2002

✅ **3 Admins Pre-configured:**
1. @waiyanphyo99
2. @waiyan7861
3. @Bingopop1991

✅ **Private Group:**
- https://t.me/+ziCAX-uVbtlhMTk1

---

## 📋 Deployment Steps

### Step 1: Go to Render.com

1. Open: https://render.com
2. Sign up / Login with GitHub
3. Click: **New +**
4. Click: **Web Service**

### Step 2: Connect GitHub Repository

1. Click: **Connect GitHub**
2. Select: `telegram-moderation-bot`
3. Click: **Connect**

### Step 3: Configure Service

Fill in these details:

```
Name: telegram-moderation-bot
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: python bot_production.py
Plan: Starter ($7/month)
Region: Singapore (or your preferred region)
```

### Step 4: Add Environment Variables

Click: **Environment**

Add these variables:

```
Key: TELEGRAM_BOT_TOKEN
Value: [REDACTED_BOT_TOKEN]

Key: TELEGRAM_ADMIN_IDS
Value: @waiyanphyo99,@waiyan7861,@Bingopop1991

Key: TELEGRAM_TARGET_CHANNELS
Value: {"caverpro": "@caverpro", "onepiecemmk": "@onepiecemmk", "allmovie00099": "@allmovie00099", "channeliingo": "@channeliingo", "channelningo": "@channelningo", "channelhingo": "@channelhingo", "channelaingo": "@channelaingo", "channeldogo": "@channeldogo", "chatCGAi": "@chatCGAi", "chanpingo": "@chanpingo", "Cartoonmovie2002": "@Cartoonmovie2002"}

Key: TELEGRAM_PRIVATE_GROUP_LINK
Value: https://t.me/+ziCAX-uVbtlhMTk1

Key: DEBUG
Value: False

Key: LOG_LEVEL
Value: INFO
```

### Step 5: Create Service

1. Click: **Create Web Service**
2. Wait for deployment (2-3 minutes)
3. Check logs for: `✅ Bot started successfully!`

### Step 6: Verify Deployment

In Render Dashboard:

1. Check: **Status** should be "Live"
2. Check: **Logs** for any errors
3. Should see:
   ```
   🤖 TELEGRAM MODERATION BOT - PRODUCTION
   ✅ Bot Token: Loaded
   ✅ Channels: 11
   ✅ Admins: 3
   ✅ Bot started successfully!
   ```

---

## 🧪 Test Bot

### Test Commands

1. **Start Bot:**
   ```
   /start
   ```

2. **Check Status:**
   ```
   /status
   ```

3. **List Channels:**
   ```
   /channels
   ```

4. **List Admins:**
   ```
   /admins
   ```

5. **Show Rules:**
   ```
   /rules
   ```

### Test Posting (Admin Only)

1. **Post to All Channels:**
   ```
   /post Hello everyone! Test message.
   ```

2. **Check Channels:**
   - Bot should post to all 11 channels
   - Check each channel for the message

---

## 📊 Monitoring

### Check Logs

1. Go to Render Dashboard
2. Click: **telegram-moderation-bot**
3. Click: **Logs**
4. View real-time logs

### Common Log Messages

```
✅ Bot started successfully!
✅ Welcomed new member
⚠️ Warned user
❌ Removed user
✅ Posted to channel
```

---

## 🔄 Updates & Redeploy

### If You Update Code

1. Push to GitHub:
   ```bash
   git add .
   git commit -m "Update bot"
   git push origin master
   ```

2. Render automatically redeploys
3. Check logs to verify

### If You Update Environment Variables

1. Go to Render Dashboard
2. Click: **Environment**
3. Update variables
4. Service automatically restarts

---

## 🛑 Stop/Restart Bot

### Stop Bot

1. Go to Render Dashboard
2. Click: **telegram-moderation-bot**
3. Click: **Settings**
4. Click: **Suspend Service**

### Restart Bot

1. Go to Render Dashboard
2. Click: **telegram-moderation-bot**
3. Click: **Manual Deploy**
4. Or wait for automatic redeploy

---

## 💰 Pricing

### Render.com Plans

| Plan | Price | Features |
|------|-------|----------|
| Free | $0 | Spins down after 15 min inactivity |
| Starter | $7/month | Always on, 0.5 CPU, 512 MB RAM |
| Standard | $12/month | 1 CPU, 1 GB RAM |
| Pro | $29/month | 2 CPU, 4 GB RAM |

**Recommended:** Starter ($7/month) for 24/7 operation

---

## 🔐 Security

### Protect Your Secrets

✅ **Never commit .env file**
✅ **.env is in .gitignore**
✅ **Use Render Environment Variables**
✅ **Rotate tokens every 90 days**

### Update Secrets

1. Go to Render Dashboard
2. Click: **Environment**
3. Update variables
4. Service restarts automatically

---

## 📞 Troubleshooting

### Bot Not Starting

**Check logs for:**
- `TELEGRAM_BOT_TOKEN not found` → Add to environment variables
- `Invalid token` → Verify token format
- `Connection error` → Check internet connection

### Bot Not Posting

**Check:**
- Bot is admin in channels
- Bot has "Send Messages" permission
- Channel names are correct
- No typos in channel names

### Deployment Failed

**Check:**
- All dependencies in requirements.txt
- Python version compatible
- No syntax errors in code
- Environment variables set

---

## ✅ Deployment Checklist

- [ ] GitHub repository connected
- [ ] Environment variables added
- [ ] Service created
- [ ] Deployment successful
- [ ] Logs show "Bot started successfully!"
- [ ] Test /start command
- [ ] Test /status command
- [ ] Test /channels command
- [ ] Test /post command (admin)
- [ ] Verify posts in channels
- [ ] Monitor logs for errors

---

## 🎉 Bot is Live!

Your bot is now:
- ✅ Running 24/7 on Render.com
- ✅ Monitoring 11 channels
- ✅ Managed by 3 admins
- ✅ Auto-forwarding posts
- ✅ Filtering inappropriate content
- ✅ Welcoming new members

**Happy Posting! 🚀**

---

## 📚 Additional Resources

- Render Docs: https://render.com/docs
- Telegram Bot API: https://core.telegram.org/bots/api
- Python Telegram Bot: https://github.com/python-telegram-bot/python-telegram-bot
- GitHub Repository: https://github.com/jue32583-tech/telegram-moderation-bot

---

**Last Updated:** 2026-07-30
**Version:** 1.0
