# 🚀 Deploy Bot to Render.com

## Step-by-Step Guide

### Step 1: Create Render Account

1. Go to https://render.com
2. Click "Sign Up"
3. Sign up with GitHub or email
4. Verify email

### Step 2: Connect GitHub Repository

1. Go to Render Dashboard
2. Click "New +" → "Web Service"
3. Click "Connect a repository"
4. Select "jue32583-tech/telegram-moderation-bot"
5. Click "Connect"

### Step 3: Configure Service

**Name:**
```
telegram-moderation-bot
```

**Environment:**
```
Python 3
```

**Build Command:**
```
pip install -r requirements.txt
```

**Start Command:**
```
python bot.py
```

**Instance Type:**
```
Free (or Starter for 24/7)
```

### Step 4: Add Environment Variables

Click "Environment" and add:

```
BOT_TOKEN = [REDACTED_BOT_TOKEN]
```

### Step 5: Deploy

1. Click "Create Web Service"
2. Wait for deployment (2-3 minutes)
3. Check logs to verify bot is running

---

## Alternative: Using Render Dashboard

### Method 1: Direct Upload

1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Choose "Public Git repository"
4. Paste: `https://github.com/jue32583-tech/telegram-moderation-bot.git`
5. Configure as above
6. Deploy

### Method 2: Using Render CLI

```bash
# Install Render CLI
npm install -g @render-com/cli

# Login
render login

# Deploy
render deploy
```

---

## Configuration on Render

### Environment Variables

Add these in Render Dashboard:

| Key | Value |
|-----|-------|
| BOT_TOKEN | [REDACTED_BOT_TOKEN] |
| TARGET_CHANNELS | -1001234567890,-1001234567891 |
| ADMIN_IDS | 123456789,987654321 |

### Update bot.py for Render

Edit `bot.py` to use environment variables:

```python
import os

BOT_TOKEN = os.getenv('BOT_TOKEN', '[REDACTED_BOT_TOKEN]')

# Parse channels from env
channels_str = os.getenv('TARGET_CHANNELS', '')
TARGET_CHANNELS = [int(ch.strip()) for ch in channels_str.split(',') if ch.strip()]

# Parse admins from env
admins_str = os.getenv('ADMIN_IDS', '')
ADMIN_IDS = [int(ad.strip()) for ad in admins_str.split(',') if ad.strip()]
```

---

## Verify Deployment

### Check Logs

1. Go to Render Dashboard
2. Select your service
3. Click "Logs"
4. Look for:
```
🤖 TELEGRAM MODERATION BOT STARTED
Listening for messages...
```

### Test Bot

1. Send `/start` to your bot in Telegram
2. Bot should respond
3. Check Render logs for activity

---

## Troubleshooting

### Bot Not Starting

**Check:**
1. Logs in Render Dashboard
2. BOT_TOKEN is correct
3. requirements.txt has all dependencies

**Common Errors:**

```
ModuleNotFoundError: No module named 'telegram'
→ Solution: requirements.txt is missing or incomplete
```

```
Error: Invalid token
→ Solution: Check BOT_TOKEN in environment variables
```

### Logs Show Errors

1. Go to Render Dashboard
2. Click "Logs"
3. Copy error message
4. Check requirements.txt
5. Verify all dependencies are listed

### Bot Crashes

**Check logs for:**
- `ModuleNotFoundError` - Missing dependency
- `Invalid token` - Wrong BOT_TOKEN
- `Connection error` - Network issue

**Solution:**
1. Fix the issue
2. Push to GitHub
3. Render auto-redeploys
4. Check logs again

---

## Upgrade to Paid Plan

### For 24/7 Running

1. Go to Render Dashboard
2. Select your service
3. Click "Settings"
4. Upgrade to "Starter" plan ($7/month)
5. Service runs 24/7

### Free Plan Limitations

- Service spins down after 15 minutes of inactivity
- Not suitable for 24/7 monitoring
- Good for testing only

---

## Update Bot Code

### To Update Bot

1. Edit `bot.py` locally
2. Commit and push to GitHub:
```bash
git add .
git commit -m "Update bot features"
git push origin master
```

3. Render auto-detects changes
4. Auto-redeploys (2-3 minutes)
5. Check logs to verify

---

## Monitor Bot

### Check Status

1. Go to Render Dashboard
2. Select service
3. View "Logs" in real-time
4. Check "Metrics" for CPU/Memory

### Restart Bot

1. Go to Render Dashboard
2. Select service
3. Click "Manual Deploy"
4. Bot restarts

---

## Backup & Recovery

### Backup Data

Bot data is saved in `bot_data.json`. To backup:

1. Download from Render file system (if available)
2. Or use GitHub to version control

### Restore Data

1. Upload `bot_data.json` to Render
2. Restart bot
3. Data is restored

---

## Cost Breakdown

| Plan | Price | Features |
|------|-------|----------|
| Free | $0 | Spins down after 15 min |
| Starter | $7/month | 24/7 running |
| Standard | $25/month | More resources |

---

## API Keys & Secrets

### Secure Bot Token

**Never commit token to GitHub!**

Use environment variables instead:

```python
import os
BOT_TOKEN = os.getenv('BOT_TOKEN')
```

### Set in Render

1. Go to Render Dashboard
2. Select service
3. Click "Environment"
4. Add BOT_TOKEN
5. Value: Your actual token
6. Save

---

## Advanced Configuration

### Custom Domain (Optional)

1. Go to Render Dashboard
2. Select service
3. Click "Settings"
4. Add custom domain
5. Update DNS records

### Webhooks (Optional)

Instead of polling, use webhooks:

```python
app.run_webhook(
    listen="0.0.0.0",
    port=10000,
    url_path="/telegram",
    webhook_url="https://your-render-url.onrender.com/telegram"
)
```

---

## Support

### Render Support

- Docs: https://render.com/docs
- Status: https://status.render.com
- Support: https://render.com/support

### Bot Issues

- Check logs in Render Dashboard
- Verify environment variables
- Test locally first

---

## Success! 🎉

Your bot is now deployed on Render.com and running 24/7!

**Next Steps:**
1. ✅ Add bot to your channels
2. ✅ Test features
3. ✅ Monitor logs
4. ✅ Upgrade to paid plan if needed
