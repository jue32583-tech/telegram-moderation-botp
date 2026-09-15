# 🤖 Telegram Bot - Complete Features Guide

## Bot အလုပ်လုပ်နိုင်တဲ့ အရာများ

### 1️⃣ Welcome Messages (ကြိုဆိုတဲ့ Message)

**အလုပ်လုပ်နည်း:**
- Channel မှာ အသုံးအသစ် join လုပ်ရင် အလိုအလျောက် welcome message ပို့ပေးတာ
- Welcome message မှာ channel rules ပါဝင်တာ
- User ရဲ့ နာမည် ပါဝင်တဲ့ personalized message

**Example:**
```
🎉 Welcome to Channel!
Hello @username! We're glad to have you here.

📋 Channel Rules:
1. Be respectful to all members
2. No spam or promotional content
3. No inappropriate language
4. No external links without permission
5. Stay on topic

Feel free to introduce yourself!
```

---

### 2️⃣ Content Filtering (စာသားဖြတ်ခြင်း)

**အလုပ်လုပ်နည်း:**
- Message တွေကို အလိုအလျောက် check လုပ်ပေးတာ
- Banned words/patterns ရှိရင် delete လုပ်ပေးတာ
- Warning message ပို့ပေးတာ

**Filter လုပ်တဲ့ အရာများ:**
- ✅ Spam keywords (spam, scam, hack, virus)
- ✅ URLs (http://, https://)
- ✅ Price mentions ($100, $50 etc)
- ✅ Adult content (xxx, adult, 18+)
- ✅ Commercial content (buy, sell, crypto, bitcoin)
- ✅ Custom patterns (သင်ထည့်သွင်းတဲ့ အရာများ)

**Example:**
```
User sends: "Check this spam link: https://example.com"
Bot: Deletes message
Bot: Sends warning "Your message was removed for violating channel rules"
```

---

### 3️⃣ Warning System (သတိပေးမှု စနစ်)

**3-Strike System:**

**First Violation (1/3):**
```
⚠️ Warning @username

Your message was removed for violating channel rules.
Warnings: 1/3

Please review our rules.
```

**Second Violation (2/3):**
```
⚠️ Final Warning @username

Your message was removed for violating channel rules.
Warnings: 2/3

One more violation will result in removal from the channel.
```

**Third Violation (3/3):**
```
❌ User Removed @username

User has been removed for repeated violations of channel rules.
```

**အလုပ်လုပ်နည်း:**
- User ကို 3 ကြိမ် warning ပေးတာ
- 3 ကြိမ်မြောက် ချိုးဖောက်ရင် channel ထဲက ဖယ်ထုတ်ပေးတာ
- Warning data ကို JSON file မှာ သိမ်းဆည်းတာ (bot restart ပြီးပါ ဆက်လက်ရှိနေတာ)

---

### 4️⃣ Multi-Channel Posting (Channel အများကို ပို့ခြင်း)

**အလုပ်လုပ်နည်း:**
- Admin ကို `/post` command ပေးတာ
- Message တွေကို configured channels အားလုံးဆီကို ပို့ပေးတာ
- Round-robin rotation (အလှည့်အစီ)

**Example:**
```
Admin sends: /post Hello everyone! This is important news.

Bot posts to:
✓ Channel 1 - Message posted
✓ Channel 2 - Message posted
✓ Channel 3 - Message posted
✓ Channel 4 - Message posted
✓ Channel 5 - Message posted

Admin receives: ✅ Message posted to 5 channels!
```

**Configuration:**
```python
TARGET_CHANNELS = [
    -1001234567890,  # Channel 1
    -1001234567891,  # Channel 2
    -1001234567892,  # Channel 3
    -1001234567893,  # Channel 4
    -1001234567894,  # Channel 5
]
```

---

### 5️⃣ Admin Commands (Admin Commands)

**Command List:**

| Command | Usage | Description |
|---------|-------|-------------|
| `/start` | Public | Bot information ကြည့်ရှုခြင်း |
| `/rules` | Public | Channel rules ကြည့်ရှုခြင်း |
| `/help` | Public | Help message ကြည့်ရှုခြင်း |
| `/status` | Admin | Bot status ကြည့်ရှုခြင်း |
| `/post <message>` | Admin | Channels အားလုံးဆီကို message ပို့ခြင်း |
| `/stats` | Admin | Violation statistics ကြည့်ရှုခြင်း |

**Command Examples:**

**1. /start**
```
🤖 Moderation Bot Active

This bot monitors channel content and enforces rules.

Commands:
/rules - Display channel rules
/help - Show help message
/status - Show bot status
```

**2. /rules**
```
📋 Channel Rules & Guidelines

1. Respect - Treat all members with respect
2. No Spam - Don't post repetitive content
3. Clean Language - Keep discussions family-friendly
4. No Links - External links require admin approval
5. Stay On Topic - Keep discussions relevant

Consequences:
- First violation: Warning (1/3)
- Second violation: Final Warning (2/3)
- Third violation: User Removed
```

**3. /status (Admin only)**
```
✅ Bot Status: Active

Active Users: 15
Total Warnings: 23
Target Channels: 5
Current Channel Index: 2
```

**4. /post (Admin only)**
```
Admin: /post 🎉 Special announcement for everyone!

Bot: ✅ Message posted to 5 channels!
```

**5. /stats (Admin only)**
```
📊 Statistics

Total Users with Warnings: 8
Total Warnings: 18

Top Violators:
• User 123456789: 5 warnings
• User 987654321: 4 warnings
• User 111111111: 3 warnings
• User 222222222: 3 warnings
• User 333333333: 3 warnings
```

---

### 6️⃣ Data Persistence (ဒေတာ သိမ်းဆည်းခြင်း)

**အလုပ်လုပ်နည်း:**
- User warning data ကို `bot_data.json` မှာ သိမ်းဆည်းတာ
- Bot restart ပြီးပါ ဒေတာ ဆက်လက်ရှိနေတာ
- အလိုအလျောက် update ဖြစ်တာ

**bot_data.json Example:**
```json
{
  "warnings": {
    "123456789": 2,
    "987654321": 1,
    "111111111": 3
  },
  "timestamp": "2026-01-18T13:00:00"
}
```

---

### 7️⃣ Logging (အလုပ်လုပ်မှု မှတ်တမ်း)

**အလုပ်လုပ်နည်း:**
- အားလုံး bot actions ကို `telegram_bot.log` မှာ မှတ်တမ်းတင်ပေးတာ
- Message filtering, warnings, commands အားလုံး log ဖြစ်တာ

**Log Examples:**
```
2026-01-18 13:00:00 - INFO - ✓ New member: @username (123456789) joined Channel
2026-01-18 13:00:05 - INFO - ✓ Welcome message sent to @username
2026-01-18 13:00:10 - INFO - Message from @username: Hello everyone!
2026-01-18 13:00:15 - INFO - ✓ Message approved from @username
2026-01-18 13:00:20 - WARNING - Deleted message from @username - violation #1
2026-01-18 13:00:25 - INFO - First warning sent to @username
```

---

### 8️⃣ Admin-Only Features (Admin အတွက်သာ)

**Admin IDs Configuration:**
```python
ADMIN_IDS = [
    123456789,  # Your user ID
    987654321,  # Another admin
]
```

**Admin Features:**
- ✅ `/status` - Bot status ကြည့်ရှုခြင်း
- ✅ `/post` - Multi-channel posting
- ✅ `/stats` - Violation statistics
- ✅ Moderation မခံရခြင်း (filtering မဖြစ်တာ)

---

## 🎯 Bot အလုပ်လုပ်မှု Flow

```
User joins channel
    ↓
Bot sends welcome message
    ↓
User sends message
    ↓
Bot checks for banned content
    ↓
If clean → Message stays
If violation → Delete + Warning
    ↓
If 3 violations → Remove user
    ↓
Admin can use /post to send to all channels
    ↓
Admin can check /stats for violations
```

---

## 📊 Bot Statistics

Bot အလုပ်လုပ်ပြီးတဲ့ အချိန်မှာ track လုပ်တဲ့ အရာများ:

- ✅ Total users with warnings
- ✅ Total warnings issued
- ✅ Messages filtered
- ✅ Users removed
- ✅ Commands executed
- ✅ Channels posted to

---

## 🔧 Customization Options

### Welcome Message ပြင်ဆင်ခြင်း

```python
WELCOME_MESSAGE = """
🎉 Welcome to {channel_name}!

Hello {user_name}! We're glad to have you here.

📋 Your custom rules here...
"""
```

### Banned Words ထည့်သွင်းခြင်း

```python
BANNED_WORDS = [
    r'\b(word1|word2|word3)\b',
    r'pattern_here',
    r'another_pattern',
]
```

### Channel Rules ပြင်ဆင်ခြင်း

```python
RULES_MESSAGE = """
📋 Your custom rules here...
"""
```

---

## ✅ Bot အသုံးပြုမှု အဖြေများ

### Q: Bot ကို ဘယ်လို add လုပ်ရမလဲ?
A: 
1. Bot ကို Telegram မှာ ရှာပါ
2. Channel မှာ add လုပ်ပါ
3. Administrator အဖြစ် ပြင်ဆင်ပါ
4. "Delete messages" permission ပေးပါ

### Q: Bot ကို ဘယ်လို run ရမလဲ?
A: 
```bash
pip install -r requirements.txt
python bot.py
```

### Q: Channel IDs ကို ဘယ်လို ရမလဲ?
A: @userinfobot မှာ message forward လုပ်ပါ

### Q: Admin ID ကို ဘယ်လို ရမလဲ?
A: @userinfobot မှာ /start ပို့ပါ

### Q: 24/7 run ရမလဲ?
A: Render.com, Railway.app, Heroku မှာ deploy လုပ်ပါ

---

## 🚀 Bot Ready!

Bot သည် အပြည့်အစုံ အလုပ်လုပ်ပြီး ကောင်းကောင်း! 🎉
