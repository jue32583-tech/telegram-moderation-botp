# 🔐 Telegram API Credentials Security Guide

## What are API_ID and API_HASH?

**API_ID** and **API_HASH** are Telegram credentials used for:
- Advanced Telegram client features (Telethon, Pyrogram)
- File uploads and downloads
- Media processing
- Advanced automation

**They are different from Bot Token:**
- Bot Token: For Bot API (simple commands, messages)
- API_ID/API_HASH: For Client API (advanced features)

---

## 🔑 How to Get API_ID and API_HASH

### Step 1: Go to Telegram App Settings
```
https://my.telegram.org/apps
```

### Step 2: Login with Your Phone Number
- Enter your phone number
- Enter the code sent to your Telegram app

### Step 3: Create Application
1. Click: **Create a new application**
2. Fill in:
   - App title: `My Bot`
   - Short name: `my_bot`
   - URL: `https://example.com` (or leave blank)
   - Description: `My Telegram Bot`

### Step 4: Get Credentials
- **API_ID**: Copy the number
- **API_HASH**: Copy the hash string

---

## 📝 Your Credentials

```
API_ID: [REDACTED_API_ID]
API_HASH: [REDACTED_API_HASH]
```

---

## 🔐 Security Best Practices

### ✅ DO

1. **Store in .env file**
   ```bash
   TELEGRAM_API_ID=[REDACTED_API_ID]
   TELEGRAM_API_HASH=[REDACTED_API_HASH]
   ```

2. **Add .env to .gitignore**
   ```bash
   echo ".env" >> .gitignore
   ```

3. **Use environment variables in production**
   ```python
   api_id = os.getenv('TELEGRAM_API_ID')
   api_hash = os.getenv('TELEGRAM_API_HASH')
   ```

4. **Load securely in code**
   ```python
   from secure_credentials import SecureCredentials
   api_id, api_hash = SecureCredentials.get_api_credentials()
   ```

5. **Rotate credentials regularly**
   - Every 90 days
   - After any security incident
   - When team member leaves

6. **Use Render environment variables**
   ```
   Dashboard → Environment → Add variables
   ```

### ❌ DON'T

1. **Hard-code credentials**
   ```python
   # NEVER DO THIS!
   api_id = [REDACTED_API_ID]
   api_hash = "[REDACTED_API_HASH]"
   ```

2. **Commit .env to Git**
   ```bash
   git add .env  # NEVER!
   ```

3. **Share credentials**
   - Don't email them
   - Don't paste in chat
   - Don't share in documents

4. **Log credentials**
   ```python
   # NEVER DO THIS!
   print(f"API_ID: {api_id}")
   logger.info(f"API_HASH: {api_hash}")
   ```

5. **Use weak permissions**
   ```bash
   chmod 644 .env  # WRONG!
   chmod 600 .env  # CORRECT!
   ```

---

## 🛡️ Secure Implementation

### Using secure_credentials.py

```python
from secure_credentials import SecureCredentials

# Get credentials securely
api_id, api_hash = SecureCredentials.get_api_credentials()

# Validate all credentials
if SecureCredentials.validate_all_credentials():
    print("✅ All credentials valid")
else:
    print("❌ Credentials validation failed")

# Get bot token
token = SecureCredentials.get_bot_token()

# Get admin IDs
admins = SecureCredentials.get_admin_ids()
```

### Using with Telethon

```python
from telethon import TelegramClient
from secure_credentials import SecureCredentials

api_id, api_hash = SecureCredentials.get_api_credentials()

client = TelegramClient('session_name', api_id, api_hash)
```

### Using with Pyrogram

```python
from pyrogram import Client
from secure_credentials import SecureCredentials

api_id, api_hash = SecureCredentials.get_api_credentials()

app = Client("my_account", api_id=api_id, api_hash=api_hash)
```

---

## 📋 Setup Checklist

### Local Setup

- [ ] Get API_ID from https://my.telegram.org/apps
- [ ] Get API_HASH from https://my.telegram.org/apps
- [ ] Create .env file from .env.example
- [ ] Add API_ID to .env
- [ ] Add API_HASH to .env
- [ ] Verify .env in .gitignore
- [ ] Test with test_bot.py
- [ ] Verify secure_credentials.py works

### Production Setup (Render.com)

- [ ] Go to Render Dashboard
- [ ] Click: **Environment**
- [ ] Add: `TELEGRAM_API_ID=[REDACTED_API_ID]`
- [ ] Add: `TELEGRAM_API_HASH=[REDACTED_API_HASH]`
- [ ] Service automatically restarts
- [ ] Check logs for: `✅ API credentials loaded`

### Security Audit

- [ ] .env file NOT in Git
- [ ] Credentials NOT in logs
- [ ] Credentials NOT in code
- [ ] File permissions: 600
- [ ] Backed up securely
- [ ] Team aware of security policy
- [ ] Rotation schedule set

---

## 🔄 Rotating Credentials

### When to Rotate
- Every 90 days (security best practice)
- After security incident
- When team member leaves
- When credentials are exposed

### How to Rotate

1. **Go to https://my.telegram.org/apps**
2. **Click: Revoke**
3. **Create new application** (get new API_ID and API_HASH)
4. **Update .env file**
5. **Update Render environment variables**
6. **Redeploy bot**
7. **Test bot functionality**

---

## 🆘 Troubleshooting

### Problem: "Invalid API_ID"
**Solution:**
- Verify API_ID is a number
- Check for extra spaces
- Regenerate from https://my.telegram.org/apps

### Problem: "Invalid API_HASH"
**Solution:**
- Verify API_HASH is correct
- Check for typos
- Regenerate from https://my.telegram.org/apps

### Problem: "Credentials not loading"
**Solution:**
- Check .env file exists
- Verify TELEGRAM_API_ID is set
- Verify TELEGRAM_API_HASH is set
- Run test_bot.py to debug

### Problem: "Permission denied"
**Solution:**
- Check file permissions: `chmod 600 .env`
- Check user has read access
- Check environment variables set

---

## 📞 Support

### Resources
- Telegram API Docs: https://core.telegram.org/api
- Telethon Docs: https://docs.telethon.dev/
- Pyrogram Docs: https://docs.pyrogram.org/

### Files
- **secure_credentials.py** - Credentials loader
- **.env.example** - Configuration template
- **test_bot.py** - Test script

---

## ✅ Summary

Your credentials are now:
- ✅ Securely stored in .env
- ✅ Protected from Git
- ✅ Loaded securely in code
- ✅ Ready for production
- ✅ Audit-ready

**Happy Coding! 🚀**

---

**Last Updated:** 2026-07-30
**Version:** 1.0
