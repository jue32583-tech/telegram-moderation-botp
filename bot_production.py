"""
Telegram Moderation & Multi-Channel Bot - PRODUCTION VERSION
With all channels and admins pre-configured

Channels (11):
- @caverpro, @onepiecemmk, @allmovie00099
- @channeliingo, @channelningo, @channelhingo, @channelaingo
- @channeldogo, @chatCGAi, @chanpingo, @Cartoonmovie2002

Admins (3):
- @waiyanphyo99, @waiyan7861, @Bingopop1991

Private Group:
- https://t.me/+ziCAX-uVbtlhMTk1
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
    def get_admin_ids() -> List[str]:
        """Get admin IDs/usernames from environment"""
        admin_ids_str = os.getenv('TELEGRAM_ADMIN_IDS', '')
        if not admin_ids_str:
            return []
        return [id.strip() for id in admin_ids_str.split(',')]
    
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
    def get_private_group_link() -> str:
        """Get private group link"""
        return os.getenv('TELEGRAM_PRIVATE_GROUP_LINK', '')
    
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
# CONFIGURATION - PRE-CONFIGURED
# ============================================================================

try:
    BOT_TOKEN = SecureConfig.get_bot_token()
    ADMIN_USERNAMES = SecureConfig.get_admin_ids()
    TARGET_CHANNELS = SecureConfig.get_target_channels()
    PRIVATE_GROUP_LINK = SecureConfig.get_private_group_link()
    DEBUG = SecureConfig.get_debug_mode()
except ValueError as e:
    logger.error(f"Configuration Error: {e}")
    raise

# Pre-configured channels (11 channels)
CHANNELS_CONFIG = {
    "caverpro": "@caverpro",
    "onepiecemmk": "@onepiecemmk",
    "allmovie00099": "@allmovie00099",
    "channeliingo": "@channeliingo",
    "channelningo": "@channelningo",
    "channelhingo": "@channelhingo",
    "channelaingo": "@channelaingo",
    "channeldogo": "@channeldogo",
    "chatCGAi": "@chatCGAi",
    "chanpingo": "@chanpingo",
    "Cartoonmovie2002": "@Cartoonmovie2002"
}

# Pre-configured admins (3 admins)
ADMIN_USERNAMES_CONFIG = [
    "@waiyanphyo99",
    "@waiyan7861",
    "@Bingopop1991"
]

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

❓ For help, contact admins:
- @waiyanphyo99
- @waiyan7861
- @Bingopop1991

🔗 Private Group: https://t.me/+ziCAX-uVbtlhMTk1
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


# Initialize data manager
data_manager = DataManager()

# ============================================================================
# BOT HANDLERS
# ============================================================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    user = update.effective_user
    logger.info(f"User {user.id} ({user.username}) started bot")
    
    keyboard = [
        [InlineKeyboardButton("📖 Help", callback_data='help')],
        [InlineKeyboardButton("📡 Channels", callback_data='channels')],
        [InlineKeyboardButton("👥 Admins", callback_data='admins')],
        [InlineKeyboardButton("🔗 Private Group", url=PRIVATE_GROUP_LINK)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"👋 Welcome {user.first_name}!\n\n"
        "I'm a moderation and multi-channel posting bot.\n\n"
        f"📡 **Channels:** {len(CHANNELS_CONFIG)}\n"
        f"👥 **Admins:** {len(ADMIN_USERNAMES_CONFIG)}\n\n"
        "Use /help for available commands.",
        reply_markup=reply_markup,
        parse_mode='Markdown'
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
/channels - List all channels
/post - Post to all channels
/stats - Show statistics

**User Commands:**
/report - Report a user
/contact - Contact admins

**Settings:**
/settings - Bot settings

For more help, contact admins.
"""
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def rules_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /rules command"""
    await update.message.reply_text(WELCOME_MESSAGE, parse_mode='Markdown')


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /status command"""
    status_text = f"""
✅ **Bot Status:**

Status: Online ✅
Channels: {len(CHANNELS_CONFIG)}
Admins: {len(ADMIN_USERNAMES_CONFIG)}
Debug: {DEBUG}

**Channels List:**
"""
    for i, (name, channel) in enumerate(CHANNELS_CONFIG.items(), 1):
        status_text += f"\n{i}. {channel}"
    
    status_text += f"\n\n**Admins:**\n"
    for i, admin in enumerate(ADMIN_USERNAMES_CONFIG, 1):
        status_text += f"\n{i}. {admin}"
    
    await update.message.reply_text(status_text, parse_mode='Markdown')


async def channels_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /channels command"""
    text = f"📡 **Configured Channels ({len(CHANNELS_CONFIG)}):**\n\n"
    for i, (name, channel) in enumerate(CHANNELS_CONFIG.items(), 1):
        text += f"{i}. {channel}\n"
    
    await update.message.reply_text(text, parse_mode='Markdown')


async def admins_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /admins command"""
    text = f"👥 **Admins ({len(ADMIN_USERNAMES_CONFIG)}):**\n\n"
    for i, admin in enumerate(ADMIN_USERNAMES_CONFIG, 1):
        text += f"{i}. {admin}\n"
    
    text += f"\n🔗 **Private Group:**\n{PRIVATE_GROUP_LINK}"
    
    await update.message.reply_text(text, parse_mode='Markdown')


async def post_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /post command"""
    user = update.effective_user
    
    # Check if admin
    if user.username not in ADMIN_USERNAMES_CONFIG and user.username not in [a.replace('@', '') for a in ADMIN_USERNAMES_CONFIG]:
        await update.message.reply_text("❌ You don't have permission to post.")
        return
    
    if not context.args:
        await update.message.reply_text("Usage: /post <message>")
        return
    
    message = ' '.join(context.args)
    
    if not CHANNELS_CONFIG:
        await update.message.reply_text("No channels configured.")
        return
    
    success_count = 0
    failed_count = 0
    
    for name, channel in CHANNELS_CONFIG.items():
        try:
            await context.bot.send_message(
                chat_id=channel,
                text=message,
                parse_mode='Markdown'
            )
            success_count += 1
            logger.info(f"Posted to channel {channel}")
        except Exception as e:
            failed_count += 1
            logger.error(f"Failed to post to {channel}: {e}")
    
    result_text = f"✅ Posted to {success_count}/{len(CHANNELS_CONFIG)} channels"
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
    if user.username in ADMIN_USERNAMES_CONFIG or user.username in [a.replace('@', '') for a in ADMIN_USERNAMES_CONFIG]:
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
    elif query.data == 'channels':
        await channels_command(update, context)
    elif query.data == 'admins':
        await admins_command(update, context)


# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Start the bot"""
    logger.info("=" * 60)
    logger.info("🤖 TELEGRAM MODERATION BOT - PRODUCTION")
    logger.info("=" * 60)
    logger.info(f"✅ Bot Token: Loaded")
    logger.info(f"✅ Channels: {len(CHANNELS_CONFIG)}")
    logger.info(f"✅ Admins: {len(ADMIN_USERNAMES_CONFIG)}")
    logger.info(f"✅ Private Group: {PRIVATE_GROUP_LINK}")
    logger.info(f"✅ Debug Mode: {DEBUG}")
    logger.info("=" * 60)
    
    # Log channels
    logger.info("📡 Channels:")
    for i, (name, channel) in enumerate(CHANNELS_CONFIG.items(), 1):
        logger.info(f"  {i}. {channel}")
    
    # Log admins
    logger.info("👥 Admins:")
    for i, admin in enumerate(ADMIN_USERNAMES_CONFIG, 1):
        logger.info(f"  {i}. {admin}")
    
    logger.info("=" * 60)
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("rules", rules_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("channels", channels_command))
    application.add_handler(CommandHandler("admins", admins_command))
    application.add_handler(CommandHandler("post", post_command))
    
    # Message handlers
    application.add_handler(ChatMemberHandler(handle_new_member, ChatMemberHandler.MY_CHAT_MEMBER))
    application.add_handler(MessageHandler(filters.TEXT | filters.CAPTION, handle_message))
    
    # Callback handlers
    application.add_handler(CallbackQueryHandler(button_callback))
    
    # Start bot
    logger.info("✅ Bot started successfully!")
    logger.info("=" * 60)
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise
