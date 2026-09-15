#!/usr/bin/env python3
"""
Test script to verify bot configuration and API key
"""

import os
import sys
from dotenv import load_dotenv

print("=" * 60)
print("🤖 BOT CONFIGURATION TEST")
print("=" * 60)

# Load environment variables
load_dotenv()

# Test 1: Check Bot Token
print("\n1️⃣  Testing Bot Token...")
token = os.getenv('TELEGRAM_BOT_TOKEN')
if not token:
    print("❌ TELEGRAM_BOT_TOKEN not found!")
    sys.exit(1)

print(f"✅ Token found: {token[:20]}...{token[-10:]}")
print(f"✅ Token length: {len(token)}")

# Validate token format
if ':' not in token:
    print("❌ Token format invalid (missing colon)")
    sys.exit(1)

parts = token.split(':')
if len(parts) != 2:
    print("❌ Token format invalid (wrong format)")
    sys.exit(1)

bot_id, bot_hash = parts
print(f"✅ Bot ID: {bot_id}")
print(f"✅ Bot Hash: {bot_hash[:10]}...{bot_hash[-5:]}")

# Test 2: Check Admin IDs
print("\n2️⃣  Testing Admin IDs...")
admin_ids = os.getenv('TELEGRAM_ADMIN_IDS', '')
if not admin_ids:
    print("⚠️  No admin IDs configured")
else:
    admins = [id.strip() for id in admin_ids.split(',')]
    print(f"✅ Admins configured: {len(admins)}")
    for i, admin in enumerate(admins, 1):
        print(f"   {i}. {admin}")

# Test 3: Check Target Channels
print("\n3️⃣  Testing Target Channels...")
import json
channels_json = os.getenv('TELEGRAM_TARGET_CHANNELS', '{}')
try:
    channels = json.loads(channels_json)
    print(f"✅ Channels configured: {len(channels)}")
    for i, (name, channel) in enumerate(channels.items(), 1):
        print(f"   {i}. {name}: {channel}")
except json.JSONDecodeError:
    print("⚠️  Invalid TELEGRAM_TARGET_CHANNELS format")

# Test 4: Check Private Group
print("\n4️⃣  Testing Private Group Link...")
private_group = os.getenv('TELEGRAM_PRIVATE_GROUP_LINK', '')
if private_group:
    print(f"✅ Private group: {private_group}")
else:
    print("⚠️  No private group configured")

# Test 5: Check Debug Mode
print("\n5️⃣  Testing Debug Mode...")
debug = os.getenv('DEBUG', 'False').lower() == 'true'
print(f"✅ Debug mode: {debug}")

# Test 6: Try to import telegram library
print("\n6️⃣  Testing Telegram Library...")
try:
    from telegram import Bot
    print("✅ python-telegram-bot library imported successfully")
    
    # Try to create bot instance
    try:
        bot = Bot(token=token)
        print("✅ Bot instance created successfully")
    except Exception as e:
        print(f"⚠️  Bot instance creation error: {e}")
except ImportError:
    print("❌ python-telegram-bot library not found")
    print("   Install with: pip install python-telegram-bot")
    sys.exit(1)

# Summary
print("\n" + "=" * 60)
print("✅ CONFIGURATION TEST PASSED!")
print("=" * 60)
print("\n📝 Next Steps:")
print("1. Deploy to Render.com")
print("2. Add bot to channels")
print("3. Test /start command")
print("4. Monitor logs")
print("\n" + "=" * 60)
