# 🎯 Quick Reference Card

## အလွယ်အသုံးပြုနိုင်တဲ့ အကျဉ်းချုပ်

---

## 🚀 5 Minute Deployment

### 1. Render.com Sign Up
```
https://render.com → Sign Up with GitHub
```

### 2. Create Service
```
Dashboard → New + → Web Service
Connect Repository → jue32583-tech/telegram-moderation-bot
```

### 3. Configure
```
Name: telegram-moderation-bot
Environment: Python 3
Build: pip install -r requirements.txt
Start: python bot.py
Plan: Starter ($7/month)
```

### 4. Environment Variables
```
BOT_TOKEN = [REDACTED_BOT_TOKEN]
ADMIN_IDS = 123456789,987654321
```

### 5. Deploy
```
Click "Create Web Service"
Wait 2-3 minutes
Check Logs → ✅ Success!
```

---

## 📡 Add Channels

### Get Channel IDs

**Public:** `@channel_name`
**Private:** `-1001234567890`

### Add Channels

```bash
/addchannel NewsChannel @breaking_news
/addchannel AdminChannel -1001234567890
```

### Verify

```bash
/channels
```

---

## 🎛️ Bot Commands

| Command | Usage |
|---------|-------|
| `/start` | Bot info |
| `/rules` | Channel rules |
| `/channels` | List channels |
| `/addchannel` | Add channel |
| `/removechannel` | Remove channel |
| `/post` | Post to all |
| `/status` | Bot status |
| `/stats` | Statistics |

---

## ⚙️ Environment Variables

```
BOT_TOKEN = Your bot token
ADMIN_IDS = Your user ID (comma-separated)
```

---

## 🔍 Troubleshooting

### Bot Not Starting
```
Check: requirements.txt has python-telegram-bot
Fix: Update and push to GitHub
```

### Invalid Token
```
Check: BOT_TOKEN in environment variables
Fix: Update and manually deploy
```

### Can't Post to Channel
```
Check: Bot is administrator
Check: Permissions enabled
Check: Channel ID correct
```

---

## 📊 Monitoring

### View Logs
```
Render Dashboard → Logs → Real-time monitoring
```

### Manual Deploy
```
Render Dashboard → Manual Deploy → Deploy latest commit
```

---

## 💡 Tips

✅ Use Starter plan for 24/7 running
✅ Add bot as administrator to channels
✅ Enable "Delete messages" permission
✅ Test with `/post` command
✅ Monitor logs regularly

---

## 🔗 Links

- **GitHub:** https://github.com/jue32583-tech/telegram-moderation-bot
- **Render:** https://render.com
- **Telegram Bot API:** https://core.telegram.org/bots/api

---

## 📝 Checklist

- [ ] Render account created
- [ ] GitHub connected
- [ ] Service configured
- [ ] Environment variables set
- [ ] Bot deployed
- [ ] Channels added
- [ ] Bot tested
- [ ] Logs monitored

---

**Ready to go! 🚀**
