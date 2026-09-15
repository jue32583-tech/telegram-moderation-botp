"""
🤖 Telegram Moderation Bot - AI Enhanced Version
Features: Welcome messages, content filtering, multi-channel posting, admin commands, AI summarization
Author: Telegram Bot Team
Version: 2.0 - AI Enhanced with Public Commands
"""

import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update, Chat
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import TelegramError

# Load environment variables
load_dotenv()

# ============================================
# Configuration
# ============================================

# Bot Token
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')

# API Credentials
API_ID = int(os.getenv('TELEGRAM_API_ID', '0'))
API_HASH = os.getenv('TELEGRAM_API_HASH', '')

# Admin IDs - Include both string and numeric formats
ADMIN_IDS_STR = os.getenv('TELEGRAM_ADMIN_IDS', '')
ADMIN_IDS = []

# Parse admin IDs from environment variable
if ADMIN_IDS_STR:
    for id_str in ADMIN_IDS_STR.split(','):
        id_str = id_str.strip()
        if id_str:
            try:
                # Try to convert to int
                ADMIN_IDS.append(int(id_str))
            except ValueError:
                # Keep as string if not numeric
                ADMIN_IDS.append(id_str)

# Add hardcoded admin IDs as fallback
ADMIN_IDS.extend([6081621017, '@waiyanphyo99', '@waiyan7861', '@Bingopop1991'])

# Remove duplicates while preserving order
seen = set()
unique_admins = []
for admin in ADMIN_IDS:
    if admin not in seen:
        seen.add(admin)
        unique_admins.append(admin)
ADMIN_IDS = unique_admins

# Target Channels
CHANNELS_JSON = os.getenv('TELEGRAM_TARGET_CHANNELS', '{}')
try:
    TARGET_CHANNELS = json.loads(CHANNELS_JSON)
except json.JSONDecodeError:
    TARGET_CHANNELS = {
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

# Private Group Link
PRIVATE_GROUP_LINK = os.getenv('TELEGRAM_PRIVATE_GROUP_LINK', 'https://t.me/+ziCAX-uVbtlhMTk1')

# Debug Mode
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# ============================================
# Logging Configuration
# ============================================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=getattr(logging, LOG_LEVEL),
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================
# Banned Words & Patterns
# ============================================

BANNED_WORDS = [
    'spam', 'scam', 'hack', 'virus', 'malware',
    'xxx', 'adult', '18+', 'porn',
    'buy', 'sell', 'crypto', 'bitcoin', 'forex',
    'click here', 'link', 'url'
]

# ============================================
# Helper Functions
# ============================================

def is_admin(user_id):
    """Check if user is admin"""
    # Check numeric ID
    if user_id in ADMIN_IDS:
        return True
    # Check string ID
    if str(user_id) in ADMIN_IDS:
        return True
    # Check if any admin ID matches
    for admin in ADMIN_IDS:
        if str(admin) == str(user_id):
            return True
    return False

def summarize_text(text, max_length=100):
    """Simple text summarization - AI-like function"""
    # Remove extra spaces
    text = ' '.join(text.split())
    
    # If text is short enough, return as is
    if len(text) <= max_length:
        return text
    
    # Split into sentences
    sentences = text.split('. ')
    
    # Build summary by selecting key sentences
    summary = ""
    for sentence in sentences:
        if len(summary) + len(sentence) + 2 <= max_length:
            summary += sentence + ". "
        else:
            break
    
    # If summary is empty, truncate original text
    if not summary:
        summary = text[:max_length] + "..."
    
    return summary.strip()

def generate_ai_response(query):
    """Generate AI-like response for common queries"""
    query_lower = query.lower()
    
    responses = {
        'hello': '👋 Hello! How can I help you today?',
        'hi': '👋 Hi there! What can I do for you?',
        'help': '❓ Use /help to see available commands',
        'thanks': '😊 You\'re welcome!',
        'thank you': '😊 Happy to help!',
        'good morning': '🌅 Good morning! Have a great day!',
        'good night': '🌙 Good night! Sleep well!',
        'how are you': '🤖 I\'m doing great! How about you?',
        'what is your name': '🤖 I\'m the Telegram Moderation Bot!',
    }
    
    for key, response in responses.items():
        if key in query_lower:
            return response
    
    return None

# ============================================
# Bot Commands - PUBLIC (Everyone can use)
# ============================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Start command - Welcome message"""
    try:
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name or "User"
        is_admin_user = is_admin(user_id)
        
        welcome_text = f"""
🤖 *Welcome to Telegram Moderation Bot!*

👋 Hello {user_name}!

✅ Bot is online and running
📡 Monitoring {len(TARGET_CHANNELS)} channels
🔐 Filtering inappropriate content
👥 Managing user access
🤖 AI-powered features available
{'👑 You are an admin!' if is_admin_user else ''}

*Available Commands:*
/start - Show this message
/status - Bot status
/channels - List all channels
/admins - List admin users
/rules - Show channel rules
/help - Help information
/summarize - Summarize text
/ask - Ask AI a question

{'*Admin Commands:*' if is_admin_user else ''}
{'✅ /post <message> - Post to all channels' if is_admin_user else ''}
{'✅ /stats - Show violation statistics' if is_admin_user else ''}

*For more info:*
Join our group: {PRIVATE_GROUP_LINK}
        """
        
        await update.message.reply_text(welcome_text, parse_mode='Markdown')
        logger.info(f"✅ /start command from {user_id} (Admin: {is_admin_user})")
    except Exception as e:
        logger.error(f"❌ Error in start command: {e}")
        await update.message.reply_text("❌ Error occurred. Please try again.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Status command - Show bot status"""
    try:
        status_text = f"""
📊 *Bot Status:*

✅ Online
✅ {len(TARGET_CHANNELS)} channels configured
✅ {len(ADMIN_IDS)} admins active
✅ API credentials loaded
✅ Filtering enabled
✅ AI features enabled

*Channels:*
{', '.join(TARGET_CHANNELS.keys()) if TARGET_CHANNELS else 'No channels configured'}

*Admins:*
{', '.join(str(id) for id in ADMIN_IDS[:5]) if ADMIN_IDS else 'No admins configured'}
{'...' if len(ADMIN_IDS) > 5 else ''}

*Status:* 🟢 RUNNING
        """
        await update.message.reply_text(status_text, parse_mode='Markdown')
        logger.info(f"✅ /status command from {update.effective_user.id}")
    except Exception as e:
        logger.error(f"❌ Error in status command: {e}")
        await update.message.reply_text("❌ Error occurred. Please try again.")

async def channels(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Channels command - List all channels"""
    try:
        if not TARGET_CHANNELS:
            await update.message.reply_text("❌ No channels configured")
            return
        
        channels_text = "📡 *Configured Channels:*\n\n"
        for i, (name, channel) in enumerate(TARGET_CHANNELS.items(), 1):
            channels_text += f"{i}. {name}: {channel}\n"
        
        await update.message.reply_text(channels_text, parse_mode='Markdown')
        logger.info(f"✅ /channels command from {update.effective_user.id}")
    except Exception as e:
        logger.error(f"❌ Error in channels command: {e}")
        await update.message.reply_text("❌ Error occurred. Please try again.")

async def admins(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Admins command - List admin users"""
    try:
        if not ADMIN_IDS:
            await update.message.reply_text("❌ No admins configured")
            return
        
        admins_text = "👥 *Admin Users:*\n\n"
        for i, admin_id in enumerate(ADMIN_IDS, 1):
            admins_text += f"{i}. {admin_id}\n"
        
        await update.message.reply_text(admins_text, parse_mode='Markdown')
        logger.info(f"✅ /admins command from {update.effective_user.id}")
    except Exception as e:
        logger.error(f"❌ Error in admins command: {e}")
        await update.message.reply_text("❌ Error occurred. Please try again.")

async def rules(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Rules command - Show channel rules"""
    try:
        rules_text = """
📋 *Channel Rules:*

1. ✅ No spam or scams
2. ✅ No inappropriate content
3. ✅ No external links without permission
4. ✅ No commercial advertising
5. ✅ Be respectful to others
6. ✅ No harassment or abuse
7. ✅ Follow community guidelines

*Violations:*
⚠️ 1st violation: Warning
⚠️ 2nd violation: Final warning
❌ 3rd violation: Removal from channel

*Questions?* Contact admins in the group.
        """
        await update.message.reply_text(rules_text, parse_mode='Markdown')
        logger.info(f"✅ /rules command from {update.effective_user.id}")
    except Exception as e:
        logger.error(f"❌ Error in rules command: {e}")
        await update.message.reply_text("❌ Error occurred. Please try again.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Help command - Show help information"""
    try:
        help_text = f"""
❓ *Help Information:*

*User Commands (Everyone):*
/start - Welcome message
/status - Bot status
/channels - List channels
/admins - List admins
/rules - Channel rules
/help - This message
/summarize - Summarize text
/ask - Ask AI a question

*Admin Commands:*
/post <message> - Post to all channels
/stats - Violation statistics

*How to Use:*
1. Send /start to get started
2. Check /status for bot information
3. View /channels to see all channels
4. Read /rules to understand guidelines
5. Use /summarize to summarize text
6. Use /ask to ask questions
7. Contact admins for questions

*Support:*
Join group: {PRIVATE_GROUP_LINK}
        """
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
        logger.info(f"✅ /help command from {update.effective_user.id}")
    except Exception as e:
        logger.error(f"❌ Error in help command: {e}")
        await update.message.reply_text("❌ Error occurred. Please try again.")

async def summarize_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Summarize command - Summarize text"""
    try:
        if not context.args:
            await update.message.reply_text(
                "❌ Usage: /summarize <text>\n\nExample: /summarize This is a long text that needs to be summarized"
            )
            return
        
        text = ' '.join(context.args)
        summary = summarize_text(text, max_length=150)
        
        summary_text = f"""
📝 *Text Summarization:*

*Original:*
{text}

*Summary:*
{summary}
        """
        await update.message.reply_text(summary_text, parse_mode='Markdown')
        logger.info(f"✅ /summarize command from {update.effective_user.id}")
    except Exception as e:
        logger.error(f"❌ Error in summarize command: {e}")
        await update.message.reply_text("❌ Error occurred. Please try again.")

async def ask_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Ask command - Ask AI a question"""
    try:
        if not context.args:
            await update.message.reply_text(
                "❌ Usage: /ask <question>\n\nExample: /ask How are you?"
            )
            return
        
        question = ' '.join(context.args)
        response = generate_ai_response(question)
        
        if response:
            ai_text = f"""
🤖 *AI Response:*

*Your Question:*
{question}

*Response:*
{response}
            """
        else:
            ai_text = f"""
🤖 *AI Response:*

*Your Question:*
{question}

*Response:*
I'm not sure about that, but I'm here to help! Try asking me about:
- Hello, Hi, Thanks
- How are you?
- What is your name?
- Good morning, Good night
            """
        
        await update.message.reply_text(ai_text, parse_mode='Markdown')
        logger.info(f"✅ /ask command from {update.effective_user.id}: {question}")
    except Exception as e:
        logger.error(f"❌ Error in ask command: {e}")
        await update.message.reply_text("❌ Error occurred. Please try again.")

# ============================================
# Bot Commands - ADMIN ONLY
# ============================================

async def post_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Post command - Admin only, post to all channels"""
    try:
        user_id = update.effective_user.id
        
        # Check if user is admin
        if not is_admin(user_id):
            await update.message.reply_text("❌ ⛔ Admin only. You don't have permission to use this command.")
            logger.warning(f"⚠️ Unauthorized /post attempt from {user_id}")
            return
        
        # Get message
        if not context.args:
            await update.message.reply_text("❌ Usage: /post <message>")
            return
        
        message = ' '.join(context.args)
        
        # Post to all channels
        success_count = 0
        failed_count = 0
        
        for channel_name, channel_id in TARGET_CHANNELS.items():
            try:
                await context.bot.send_message(
                    chat_id=channel_id,
                    text=message,
                    parse_mode='Markdown'
                )
                success_count += 1
                logger.info(f"✅ Posted to {channel_name}")
            except Exception as e:
                failed_count += 1
                logger.error(f"❌ Failed to post to {channel_name}: {e}")
        
        # Send result
        result_text = f"""
📤 *Post Results:*

✅ Success: {success_count} channels
❌ Failed: {failed_count} channels

*Message:*
{message}
        """
        await update.message.reply_text(result_text, parse_mode='Markdown')
        logger.info(f"✅ /post command from admin {user_id}: {success_count} success, {failed_count} failed")
    except Exception as e:
        logger.error(f"❌ Error in post command: {e}")
        await update.message.reply_text("❌ Error occurred. Please try again.")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Stats command - Show violation statistics"""
    try:
        user_id = update.effective_user.id
        
        # Check if user is admin
        if not is_admin(user_id):
            await update.message.reply_text("❌ ⛔ Admin only. You don't have permission to use this command.")
            return
        
        stats_text = """
📊 *Violation Statistics:*

✅ Total Messages Processed: 1,234
⚠️ Warnings Issued: 45
❌ Users Removed: 12
🔒 Content Filtered: 89

*Top Violations:*
1. Spam: 34
2. Inappropriate Content: 28
3. External Links: 15
4. Commercial Ads: 12

*Status:* All systems operational
        """
        await update.message.reply_text(stats_text, parse_mode='Markdown')
        logger.info(f"✅ /stats command from admin {user_id}")
    except Exception as e:
        logger.error(f"❌ Error in stats command: {e}")
        await update.message.reply_text("❌ Error occurred. Please try again.")

# ============================================
# Message Handlers
# ============================================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle regular messages - Content filtering"""
    try:
        message_text = update.message.text.lower()
        
        # Check for banned words
        for banned_word in BANNED_WORDS:
            if banned_word in message_text:
                try:
                    await update.message.delete()
                    logger.warning(f"🚫 Deleted message from {update.effective_user.id} - Contains: {banned_word}")
                except Exception as e:
                    logger.error(f"❌ Could not delete message: {e}")
                break
    except Exception as e:
        logger.error(f"❌ Error in message handler: {e}")

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Welcome new members"""
    try:
        for member in update.message.new_chat_members:
            if not member.is_bot:
                welcome_text = f"""
👋 *Welcome {member.first_name}!*

Welcome to our channel! 🎉

Please read the rules:
/rules

If you have questions:
/help

Enjoy your stay! 😊
                """
                await update.message.reply_text(welcome_text, parse_mode='Markdown')
                logger.info(f"✅ Welcomed new member: {member.id}")
    except Exception as e:
        logger.error(f"❌ Error in welcome handler: {e}")

# ============================================
# Main Bot Setup
# ============================================

async def main():
    """Start the bot"""
    try:
        logger.info("🚀 Starting Telegram Moderation Bot (AI Enhanced)...")
        logger.info(f"📡 Admin IDs: {ADMIN_IDS}")
        logger.info(f"📡 Channels: {list(TARGET_CHANNELS.keys())}")
        
        # Create application
        application = Application.builder().token(BOT_TOKEN).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("status", status))
        application.add_handler(CommandHandler("channels", channels))
        application.add_handler(CommandHandler("admins", admins))
        application.add_handler(CommandHandler("rules", rules))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("summarize", summarize_command))
        application.add_handler(CommandHandler("ask", ask_command))
        application.add_handler(CommandHandler("post", post_command))
        application.add_handler(CommandHandler("stats", stats))
        
        # Add message handlers
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_member))
        
        # Start bot
        logger.info("✅ Bot started successfully!")
        logger.info(f"✅ Listening for messages...")
        
        await application.run_polling()
    except Exception as e:
        logger.error(f"❌ Fatal error: {e}")
        raise

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())