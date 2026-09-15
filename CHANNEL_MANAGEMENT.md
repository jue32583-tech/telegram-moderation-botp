# 📡 Channel Management Guide

## Public & Private Channels Support

Bot သည် **Public channels** နှင့် **Private channels** နှစ်မျိုးလုံးမှာ အလုပ်လုပ်နိုင်ပါတယ်။

---

## 🌍 Public Channels

### Public Channel ID ရယူခြင်း

**Method 1: Using @userinfobot**
1. Telegram မှာ @userinfobot ရှာပါ
2. `/start` ပို့ပါ
3. Public channel မှ message forward လုပ်ပါ
4. Bot ကို channel ID ပြပေးမှာ ဖြစ်ပါတယ်

**Method 2: Manual**
- Public channel name ကို သုံးပါ
- Format: `@channel_name`
- Example: `@mychannel`, `@news_channel`

### Add Public Channel

```bash
/addchannel MyPublicChannel @mychannel
```

**Example:**
```
/addchannel NewsChannel @breaking_news
/addchannel UpdatesChannel @daily_updates
```

---

## 🔒 Private Channels

### Private Channel ID ရယူခြင်း

**Method 1: Using @userinfobot**
1. Telegram မှာ @userinfobot ရှာပါ
2. `/start` ပို့ပါ
3. Private channel မှ message forward လုပ်ပါ
4. Bot ကို channel ID ပြပေးမှာ ဖြစ်ပါတယ် (negative number)

**Method 2: Using Telegram API**
```bash
curl "https://api.telegram.org/botYOUR_TOKEN/getUpdates"
```

### Private Channel ID Format

Private channel IDs သည် negative numbers ဖြစ်ပါတယ်:
- Example: `-1001234567890`
- Example: `-1009876543210`

### Add Private Channel

```bash
/addchannel MyPrivateChannel -1001234567890
```

**Example:**
```
/addchannel AdminChannel -1001234567890
/addchannel TeamChannel -1001234567891
/addchannel VIPChannel -1001234567892
```

---

## 🎛️ Channel Management Commands

### View All Channels

```bash
/channels
```

**Output:**
```
📡 Configured Channels:

1. 🌍 Public: NewsChannel
2. 🔒 Private: AdminChannel
3. 🔒 Private: TeamChannel
4. 🌍 Public: UpdatesChannel
```

### Add Channel

```bash
/addchannel <name> <channel_id>
```

**Public Channel:**
```bash
/addchannel MyNews @my_news_channel
```

**Private Channel:**
```bash
/addchannel MyTeam -1001234567890
```

### Remove Channel

```bash
/removechannel <name>
```

**Example:**
```bash
/removechannel MyNews
/removechannel MyTeam
```

---

## 📤 Post to Multiple Channels

### Post Message

```bash
/post Your message here
```

Bot သည် အားလုံး configured channels မှာ message ပို့ပေးပါတယ်။

**Example:**
```
/post 🎉 Important announcement for everyone!
```

**Output:**
```
✅ Message posted to 4 channels!
```

### Post with Formatting

```bash
/post **Bold text** and *italic text* with [links](https://example.com)
```

---

## 🔄 Round-Robin Posting

Bot သည် channels မှာ အလှည့်အစီ ပို့ပေးပါတယ်။

**Example with 3 channels:**

```
Post 1 → Channel 1
Post 2 → Channel 2
Post 3 → Channel 3
Post 4 → Channel 1 (cycle repeats)
```

---

## ⚙️ Configuration in Code

### bot.py မှာ Channels ထည့်သွင်းခြင်း

```python
TARGET_CHANNELS = {
    "NewsChannel": "@breaking_news",      # Public
    "AdminChannel": -1001234567890,       # Private
    "TeamChannel": -1001234567891,        # Private
    "UpdatesChannel": "@daily_updates",   # Public
}
```

### Environment Variables (Render.com)

```
BOT_TOKEN = [REDACTED_BOT_TOKEN]
TARGET_CHANNELS = NewsChannel:@breaking_news,AdminChannel:-1001234567890
ADMIN_IDS = 123456789,987654321
```

---

## 🔐 Bot Permissions

### Required Permissions for Public Channels

1. ✅ Send messages
2. ✅ Delete messages (for filtering)
3. ✅ Ban users (for violations)

### Required Permissions for Private Channels

1. ✅ Send messages
2. ✅ Delete messages (for filtering)
3. ✅ Ban users (for violations)
4. ✅ Add members (optional)

### How to Set Permissions

1. Open Telegram channel
2. Click channel name
3. Tap "Edit Channel"
4. Go to "Administrators"
5. Select bot
6. Enable required permissions

---

## 📋 Channel Setup Checklist

### For Each Channel

- [ ] Bot added to channel
- [ ] Bot is administrator
- [ ] "Delete messages" permission enabled
- [ ] "Ban users" permission enabled
- [ ] Channel ID obtained
- [ ] Channel added via `/addchannel`

### Verify Setup

```bash
/channels
```

Should show all your channels.

---

## 🚀 Quick Setup Example

### Scenario: Setup 5 Channels

**Step 1: Get Channel IDs**

Using @userinfobot:
- Public Channel 1: `@news_channel`
- Public Channel 2: `@updates_channel`
- Private Channel 1: `-1001234567890`
- Private Channel 2: `-1001234567891`
- Private Channel 3: `-1001234567892`

**Step 2: Add Channels**

```bash
/addchannel News @news_channel
/addchannel Updates @updates_channel
/addchannel Admin -1001234567890
/addchannel Team -1001234567891
/addchannel VIP -1001234567892
```

**Step 3: Verify**

```bash
/channels
```

**Step 4: Test Posting**

```bash
/post Hello everyone! Testing multi-channel posting.
```

---

## 🔍 Troubleshooting

### Bot Can't Post to Channel

**Check:**
1. Bot is administrator in channel
2. Bot has "Send messages" permission
3. Channel ID is correct
4. Channel is not archived

**Solution:**
1. Remove bot from channel
2. Add bot again
3. Grant permissions
4. Re-add channel: `/addchannel Name ID`

### Channel Not Appearing in /channels

**Check:**
1. Channel was added correctly
2. Channel name is spelled correctly
3. Channel ID is correct

**Solution:**
```bash
/removechannel WrongName
/addchannel CorrectName correct_id
```

### Private Channel ID Not Working

**Check:**
1. ID starts with `-100`
2. ID is complete (13-14 digits)
3. Bot is member of channel

**Example of correct format:**
- ✅ `-1001234567890` (13 digits after -)
- ❌ `-123456789` (too short)
- ❌ `1001234567890` (missing -)

---

## 📊 Channel Statistics

### View Channel Info

```bash
/status
```

Shows:
- Total channels configured
- Active users
- Total warnings
- Current channel index

---

## 🎯 Best Practices

### Channel Organization

1. **Name channels clearly**
   - ✅ `/addchannel News @news_channel`
   - ❌ `/addchannel ch1 @channel`

2. **Group by type**
   - Public channels first
   - Private channels second

3. **Document channel purposes**
   - News channels
   - Admin channels
   - Team channels

### Posting Strategy

1. **Use meaningful messages**
   - Include context
   - Use formatting
   - Add emojis for clarity

2. **Avoid spam**
   - Don't post too frequently
   - Keep messages relevant
   - Use `/post` wisely

3. **Monitor channels**
   - Check logs regularly
   - Review violations
   - Update rules as needed

---

## 📝 Example Workflows

### Workflow 1: News Distribution

```bash
# Setup
/addchannel Breaking @breaking_news
/addchannel Updates @daily_updates
/addchannel Archive -1001234567890

# Use
/post 🚨 Breaking News: Important update!
```

### Workflow 2: Team Communication

```bash
# Setup
/addchannel TeamChat -1001234567890
/addchannel AdminOnly -1001234567891
/addchannel Announcements @team_announcements

# Use
/post 📢 Team meeting at 3 PM today!
```

### Workflow 3: Community Management

```bash
# Setup
/addchannel General @community_general
/addchannel Announcements @community_news
/addchannel Support -1001234567890
/addchannel VIP -1001234567891

# Use
/post 🎉 Welcome to our community!
```

---

## ✅ Ready to Manage Channels!

Bot သည် Public နှင့် Private channels အားလုံးမှာ အလုပ်လုပ်ပြီး ကောင်းကောင်း! 🚀

**Next Steps:**
1. ✅ Channel IDs ရယူပါ
2. ✅ Channels ထည့်သွင်းပါ
3. ✅ `/channels` ကြည့်ပါ
4. ✅ `/post` နဲ့ test လုပ်ပါ
5. ✅ Logs monitor လုပ်ပါ
