"""
Telegram Moderation & Multi-Channel Bot - SECURE VERSION
Features:
- Welcome new members with customizable messages
- Filter inappropriate content and spam
- Post messages to multiple channels (public & private) in round-robin fashion
- Warning system with automatic user removal
- Admin commands and logging
- Easy button-based channel configuration
- SECURE: All secrets stored in environment variables
"""

import logging
import json
import re
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dotenv import load_dotenv

from telegram import Update, ChatMember, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    ChatMemberHandler,
    CallbackQueryHandler,
    filters,
)
from telegram.error import TelegramError
from telegram.constants import ChatAction

# ============================================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================================

# Load from .env file (for local development)
load_dotenv()

# ============================================================================
# SECURE CONFIGURATION
# ============================================================================

class SecureConfig:
    """Secure configuration loader"""
    
    @staticmethod
    def get_bot_token() -> str:
        """Get bot token from environment"""
        token = os.getenv('TELEGRAM_BOT_TOKEN')
        if not token:
            raise ValueError(
                "❌ TELEGRAM_BOT_TOKEN not found in environment variables!\n"
                "Please set it in .env file or hosting platform environment."
            )
        return token
    
    @staticmethod
    def get_admin_ids() -> List[int]:
        """Get admin IDs from environment"""
        admin_ids_str = os.getenv('TELEGRAM_ADMIN_IDS', '')
        if not admin_ids_str:
            return []
        try:
            return [int(id.strip()) for id in admin_ids_str.split(',')]
        except ValueError:
            logging.warning("Invalid TELEGRAM_ADMIN_IDS format")
            return []
    
    @staticmethod
    def get_target_channels() -> Dict:
        """Get target channels from environment"""
        channels_json = os.getenv('TELEGRAM_TARGET_CHANNELS', '{}')
        try:
            return json.loads(channels_json)
        except json.JSONDecodeError:
            logging.warning("Invalid TELEGRAM_TARGET_CHANNELS format")
            return {}
    
    @staticmethod
    def get_log_level() -> str:
        """Get log level from environment"""
        return os.getenv('LOG_LEVEL', 'INFO')
    
    @staticmethod
    def get_debug_mode() -> bool:
        """Get debug mode from environment"""
        return os.getenv('DEBUG', 'False').lower() == 'true'


# ============================================================================
# LOGGING SETUP
# ============================================================================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# CONFIGURATION
# ============================================================================

try:
    BOT_TOKEN = SecureConfig.get_bot_token()
    ADMIN_IDS = SecureConfig.get_admin_ids()
    TARGET_CHANNELS = SecureConfig.get_target_channels()
    DEBUG = SecureConfig.get_debug_mode()
except ValueError as e:
    logger.error(f"Configuration Error: {e}")
    raise

# Banned words/patterns
BANNED_WORDS = [
    r'\b(spam|scam|hack|virus)\b',
    r'(http|https):\/\/[^\s]+',
    r'\b(xxx|adult|18\+)\b',
    r'\b(buy|sell|crypto|bitcoin)\b',
]

# Welcome message
WELCOME_MESSAGE = """
👋 Welcome to our community!

📋 **Community Guidelines:**
1. Be respectful to all members
2. No spam or promotional content
3. No inappropriate language
4. Follow all community rules

⚠️ **Warning System:**
- 1st violation: Warning (1/3)
- 2nd violation: Final warning (2/3)
- 3rd violation: Removal from group

❓ For help, contact admins.
"""

# ============================================================================
# DATA STORAGE
# ============================================================================

class DataManager:
    """Manage user warnings and data"""
    
    def __init__(self, data_file: str = 'user_warnings.json'):
        self.data_file = data_file
        self.data = self._load_data()
    
    def _load_data(self) -> Dict:
        """Load data from file"""
        if Path(self.data_file).exists():
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading data: {e}")
                return {}
        return {}
    
    def _save_data(self):
        """Save data to file"""
        try:
            with open(self.data_file, 'w') as f:
                json.dump(self.data, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving data: {e}")
    
    def add_warning(self, user_id: int, group_id: int) -> int:
        """Add warning to user"""
        key = f"{group_id}_{user_id}"
        if key not in self.data:
            self.data[key] = {'warnings': 0, 'timestamp': datetime.now().isoformat()}
        self.data[key]['warnings'] += 1
        self._save_data()
        return self.data[key]['warnings']
    
    def get_warnings(self, user_id: int, group_id: int) -> int:
        """Get user warnings"""
        key = f"{group_id}_{user_id}"
        return self.data.get(key, {}).get('warnings', 0)
    
    def reset_warnings(self, user_id: int, group_id: int):
        """Reset user warnings"""
        key = f"{group_id}_{user_id}"
        if key in self.data:
            del self.data[key]
            self._save_data()
    
    def get_channels(self) -> List[Dict]:
        """Get all configured channels"""
        return self.data.get('channels', [])
    
    def add_channel(self, channel_id, channel_name: str, is_private: bool = False):
        """Add channel to list"""
        if 'channels' not in self.data:
            self.data['channels'] = []
        
        channel = {
            'id': channel_id,
            'name': channel_name,
            'private': is_private,
            'added_at': datetime.now().isoformat()
        }
        
        # Check if already exists
        if not any(c['id'] == channel_id for c in self.data['channels']):
            self.data['channels'].append(channel)
            self._save_data()
            return True
        return False
    
    def remove_channel(self, channel_id):
        """Remove channel from list"""
        if 'channels' in self.data:
            self.data['channels'] = [c for c in self.data['channels'] if c['id'] != channel_id]
            self._save_data()
            return True
        return False


# Initialize data manager
data_manager = DataManager()

# ============================================================================
# BOT HANDLERS
# ============================================================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    logger.info(f"User {user.id} started bot")
    
    keyboard = [
        [InlineKeyboardButton("📖 Help", callback_data='help')],
        [InlineKeyboardButton("⚙️ Settings", callback_data='settings')],
        [InlineKeyboardButton("🔗 Channels", callback_data='channels')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"👋 Welcome {user.first_name}!\n\n"
        "I'm a moderation and multi-channel posting bot.\n\n"
        "Use /help for available commands.",
        reply_markup=reply_markup
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /help command"""
    help_text = """
📖 **Available Commands:**

**Admin Commands:**
/start - Start bot
/help - Show this help message
/rules - Show community rules
/status - Bot status
/channels - Manage channels
/post - Post to all channels
/stats - Show statistics

**User Commands:**
/report - Report a user
/contact - Contact admins

**Channel Management:**
/addchannel - Add a channel
/removechannel - Remove a channel
/listchannels - List all channels

**Settings:**
/settings - Bot settings
/config - Configure bot

For more help, contact admins.
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /rules command"""
    await update.message.reply_text(WELCOME_MESSAGE, parse_mode='Markdown')


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    channels = data_manager.get_channels()
    status_text = f"""
✅ **Bot Status:**

Status: Online
Channels: {len(channels)}
Admins: {len(ADMIN_IDS)}
Debug: {DEBUG}

**Channels:**
"""
    for channel in channels:
        status_text += f"\n- {channel['name']} ({'Private' if channel['private'] else 'Public'})"
    
    await update.message.reply_text(status_text, parse_mode='Markdown')


async def channels_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /channels command"""
    user_id = update.effective_user.id
    
    # Check if admin
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ You don't have permission to manage channels.")
        return
    
    channels = data_manager.get_channels()
    
    if not channels:
        await update.message.reply_text("No channels configured yet.")
        return
    
    text = "📡 **Configured Channels:**\n\n"
    for i, channel in enumerate(channels, 1):
        channel_type = "🔒 Private" if channel['private'] else "🌍 Public"
        text += f"{i}. {channel['name']} ({channel_type})\n"
    
    await update.message.reply_text(text, parse_mode='Markdown')


async def post_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /post command"""
    user_id = update.effective_user.id
    
    # Check if admin
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("❌ You don't have permission to post.")
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /post <message>")
        return
    
    message = ' '.join(context.args)
    channels = data_manager.get_channels()
    
    if not channels:
        await update.message.reply_text("No channels configured.")
        return
    
    success_count = 0
    failed_count = 0
    
    for channel in channels:
        try:
            await context.bot.send_message(
                chat_id=channel['id'],
                text=message,
                parse_mode='Markdown'
            )
            success_count += 1
            logger.info(f"Posted to channel {channel['name']}")
        except Exception as e:
            failed_count += 1
            logger.error(f"Failed to post to {channel['name']}: {e}")
    
    result_text = f"✅ Posted to {success_count} channels"
    if failed_count > 0:
        result_text += f"\n❌ Failed: {failed_count} channels"
    
    await update.message.reply_text(result_text)


async def handle_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle new member joining"""
    for member in update.chat_member.new_chat_members:
        if not member.is_bot:
            try:
                await update.effective_chat.send_message(
                    f"👋 Welcome {member.mention_html()}!\n\n{WELCOME_MESSAGE}",
                    parse_mode='HTML'
                )
                logger.info(f"Welcomed new member {member.id} in group {update.effective_chat.id}")
            except Exception as e:
                logger.error(f"Error welcoming member: {e}")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle incoming messages"""
    message = update.message
    user = update.effective_user
    chat = update.effective_chat
    
    # Skip if from admin
    if user.id in ADMIN_IDS:
        return
    
    # Check for banned words
    text = message.text or message.caption or ""
    
    for pattern in BANNED_WORDS:
        if re.search(pattern, text, re.IGNORECASE):
            try:
                # Delete message
                await message.delete()
                
                # Add warning
                warnings = data_manager.add_warning(user.id, chat.id)
                
                if warnings >= 3:
                    # Remove user
                    await chat.ban_member(user.id)
                    await chat.send_message(
                        f"❌ User {user.mention_html()} has been removed for violating rules.",
                        parse_mode='HTML'
                    )
                    logger.info(f"Removed user {user.id} from group {chat.id}")
                else:
                    # Send warning
                    remaining = 3 - warnings
                    await chat.send_message(
                        f"⚠️ {user.mention_html()}, your message was removed.\n"
                        f"Warning {warnings}/3. {remaining} more and you'll be removed.",
                        parse_mode='HTML'
                    )
                    logger.info(f"Warned user {user.id} in group {chat.id} ({warnings}/3)")
                
                break
            except Exception as e:
                logger.error(f"Error handling message: {e}")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button callbacks"""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'help':
        await help_command(update, context)
    elif query.data == 'settings':
        await query.edit_message_text(text="⚙️ Settings page (coming soon)")
    elif query.data == 'channels':
        await channels_command(update, context)


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Start the bot"""
    logger.info("🤖 Starting Telegram Bot...")
    logger.info(f"Debug Mode: {DEBUG}")
    logger.info(f"Admin IDs: {ADMIN_IDS}")
    logger.info(f"Configured Channels: {len(TARGET_CHANNELS)}")
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("rules", rules_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("channels", channels_command))
    application.add_handler(CommandHandler("post", post_command))
    
    # Message handlers
    application.add_handler(ChatMemberHandler(handle_new_member, ChatMemberHandler.MY_CHAT_MEMBER))
    application.add_handler(MessageHandler(filters.TEXT | filters.CAPTION, handle_message))
    
    # Callback handlers
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Start bot
    logger.info("✅ Bot started successfully!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise
