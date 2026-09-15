# 🔐 Secure Bot Setup Guide

## Bot API Key ကို လုံခြုံအောင် သိမ်းဆည်းခြင်း

---

## 📋 Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Environment Variables](#environment-variables)
3. [GitHub Secrets Setup](#github-secrets-setup)
4. [Render.com Deployment](#rendercom-deployment)
5. [Security Best Practices](#security-best-practices)

---

## 🖥️ Local Development Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/jue32583-tech/telegram-moderation-bot.git
cd telegram-moderation-bot
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Create .env File

```bash
# Copy template
cp .env.example .env

# Edit .env file
nano .env
```

### Step 5: Fill in Your Secrets

```env
# .env file
TELEGRAM_BOT_TOKEN=[REDACTED_BOT_TOKEN]
TELEGRAM_ADMIN_IDS=123456789,987654321
TELEGRAM_TARGET_CHANNELS={}
DEBUG=False
LOG_LEVEL=INFO
```

### Step 6: Test Locally

```bash
# Run secure version
python bot_secure.py

# You should see:
# ✅ Bot started successfully!
```

### Step 7: Verify .env is Protected

```bash
# Check .env is in .gitignore
cat .gitignore | grep ".env"

# Set file permissions (Linux/Mac)
chmod 600 .env

# Verify permissions
ls -la .env
# Should show: -rw------- (600)
```

---

## 🔑 Environment Variables

### Required Variables

```env
# Bot Token (REQUIRED)
TELEGRAM_BOT_TOKEN=your_token_here

# Admin IDs (Optional)
TELEGRAM_ADMIN_IDS=123456789,987654321

# Target Channels (Optional)
TELEGRAM_TARGET_CHANNELS={}

# Debug Mode (Optional)
DEBUG=False

# Log Level (Optional)
LOG_LEVEL=INFO
```

### How to Get Bot Token

1. Open Telegram
2. Search: `@BotFather`
3. Send: `/start`
4. Send: `/newbot`
5. Follow instructions
6. Copy token: `[REDACTED_BOT_TOKEN]`

### How to Get Admin IDs

1. Open Telegram
2. Search: `@userinfobot`
3. Send: `/start`
4. Bot shows your ID
5. Add to `TELEGRAM_ADMIN_IDS`

---

## 🔐 GitHub Secrets Setup

### Why Use GitHub Secrets?

- ✅ Secrets not visible in code
- ✅ Secrets not in Git history
- ✅ Secrets only in CI/CD environment
- ✅ Automatic deployment with secrets

### Step 1: Go to GitHub Settings

1. Open: https://github.com/jue32583-tech/telegram-moderation-bot
2. Click: **Settings**
3. Click: **Secrets and variables**
4. Click: **Actions**

### Step 2: Add Secrets

Click: **New repository secret**

**Add these secrets:**

```
Name: TELEGRAM_BOT_TOKEN
Value: [REDACTED_BOT_TOKEN]
```

```
Name: TELEGRAM_ADMIN_IDS
Value: 123456789,987654321
```

```
Name: TELEGRAM_TARGET_CHANNELS
Value: {}
```

```
Name: DEBUG
Value: False
```

```
Name: LOG_LEVEL
Value: INFO
```

### Step 3: Verify Secrets

All secrets should appear in the list (values hidden).

---

## 🚀 Render.com Deployment

### Step 1: Connect GitHub

1. Go to: https://render.com
2. Sign up / Login
3. Click: **New +**
4. Click: **Web Service**
5. Click: **Connect GitHub**
6. Select: `telegram-moderation-bot`
7. Click: **Connect**

### Step 2: Configure Service

```
Name: telegram-moderation-bot
Environment: Python 3
Build Command: pip install -r requirements.txt
Start Command: python bot_secure.py
Plan: Starter ($7/month)
```

### Step 3: Add Environment Variables

In Render Dashboard:

1. Click: **Environment**
2. Add variables:

```
TELEGRAM_BOT_TOKEN = [REDACTED_BOT_TOKEN]
TELEGRAM_ADMIN_IDS = 123456789,987654321
TELEGRAM_TARGET_CHANNELS = {}
DEBUG = False
LOG_LEVEL = INFO
```

### Step 4: Deploy

1. Click: **Create Web Service**
2. Wait for deployment
3. Check logs for: `✅ Bot started successfully!`

### Step 5: Verify Deployment

```bash
# Check logs in Render Dashboard
# Should show:
# 🤖 Starting Telegram Bot...
# ✅ Bot started successfully!
```

---

## 🛡️ Security Best Practices

### ✅ DO

```python
# ✅ Load from environment
token = os.getenv('TELEGRAM_BOT_TOKEN')

# ✅ Use .env file (local)
from dotenv import load_dotenv
load_dotenv()

# ✅ Add .env to .gitignore
echo ".env" >> .gitignore

# ✅ Use GitHub Secrets (CI/CD)
# Secrets automatically available in Actions

# ✅ Use Render Environment Variables
# Variables set in Render Dashboard

# ✅ Rotate tokens regularly
# Every 90 days, regenerate token from @BotFather

# ✅ Use secure file permissions
chmod 600 .env

# ✅ Backup securely
# Store backups in secure location
```

### ❌ DON'T

```python
# ❌ Hard-code tokens
token = "[REDACTED_BOT_TOKEN]"

# ❌ Commit .env file
git add .env  # NEVER!

# ❌ Share token in emails
email.send(f"Token: {token}")

# ❌ Log tokens
print(f"Token: {token}")

# ❌ Push to GitHub
git push  # Check .gitignore first!

# ❌ Store in comments
# token = "secret_token_here"

# ❌ Use weak permissions
chmod 644 .env  # WRONG!

# ❌ Share repository access
# Only trusted developers
```

---

## 🔄 Token Rotation

### Every 90 Days

1. Open Telegram
2. Search: `@BotFather`
3. Send: `/mybots`
4. Select your bot
5. Send: `/revoke`
6. Send: `/newbot` (get new token)
7. Update everywhere:
   - .env file
   - GitHub Secrets
   - Render Environment Variables
8. Redeploy application
9. Verify bot is working

### Emergency Rotation

If token is compromised:

1. Immediately revoke token (@BotFather)
2. Generate new token
3. Update all locations
4. Redeploy immediately
5. Review access logs
6. Notify users

---

## 📋 Deployment Checklist

### Pre-Deployment

- [ ] .env file created
- [ ] .env added to .gitignore
- [ ] Bot token filled in
- [ ] Admin IDs configured
- [ ] .env file permissions: 600
- [ ] Tested locally: `python bot_secure.py`
- [ ] No secrets in code
- [ ] No secrets in Git history

### GitHub Secrets

- [ ] TELEGRAM_BOT_TOKEN added
- [ ] TELEGRAM_ADMIN_IDS added
- [ ] TELEGRAM_TARGET_CHANNELS added
- [ ] DEBUG set to False
- [ ] LOG_LEVEL set to INFO

### Render Deployment

- [ ] Repository connected
- [ ] Environment variables added
- [ ] Service created
- [ ] Deployment successful
- [ ] Logs show: `✅ Bot started successfully!`
- [ ] Bot responding to commands

### Post-Deployment

- [ ] Test bot commands
- [ ] Check logs for errors
- [ ] Verify no secrets in logs
- [ ] Monitor bot activity
- [ ] Set up monitoring/alerts

---

## 🆘 Troubleshooting

### Bot Not Starting

**Error:** `TELEGRAM_BOT_TOKEN not found`

**Solution:**
1. Check .env file exists
2. Check TELEGRAM_BOT_TOKEN is set
3. Check token format is correct
4. Restart bot: `python bot_secure.py`

### Token Invalid

**Error:** `Unauthorized`

**Solution:**
1. Verify token from @BotFather
2. Check for typos
3. Regenerate new token
4. Update .env and redeploy

### Secrets Not Loading

**Error:** `KeyError: TELEGRAM_BOT_TOKEN`

**Solution:**
1. Check .env file in correct location
2. Check file permissions
3. Verify `load_dotenv()` is called
4. Check environment variable names

### Deployment Failed

**Error:** Build or deployment error

**Solution:**
1. Check Render logs
2. Verify all dependencies in requirements.txt
3. Check Python version compatibility
4. Verify environment variables set

---

## 📞 Support

### Get Help

- GitHub Issues: https://github.com/jue32583-tech/telegram-moderation-bot/issues
- Telegram: @support_username
- Email: support@yourbot.com

### Security Issues

If you find a security vulnerability:

1. **DO NOT** post in public issues
2. Email: security@yourbot.com
3. Include: Description, steps to reproduce, impact
4. We'll respond within 24 hours

---

## ✅ Security Setup Complete!

Your bot is now:
- ✅ Securely configured
- ✅ Secrets protected
- ✅ Ready for production
- ✅ Deployed on Render.com
- ✅ Running 24/7

**Happy Secure Posting! 🚀**

---

## 📚 Additional Resources

- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [GitHub Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Render Environment Variables](https://render.com/docs/environment-variables)
- [OWASP Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

---

**Last Updated:** 2026-07-30
**Version:** 1.0
