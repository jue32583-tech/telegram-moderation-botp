#!/usr/bin/env python3
"""Telegram moderation bot with Burmese commands and controlled channel copying."""

from __future__ import annotations

import json
import logging
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import TelegramError
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    ChatMemberHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN Railway secret variable is required")
if not re.fullmatch(r"\d+:[A-Za-z0-9_-]{20,}", BOT_TOKEN):
    raise RuntimeError("TELEGRAM_BOT_TOKEN has an invalid format")

DEFAULT_ADMIN_IDS = {6081621017, 6940887457, 6432487408}


def parse_admin_ids() -> set[int]:
    raw = os.getenv("TELEGRAM_ADMIN_IDS", "")
    configured: set[int] = set()
    for value in raw.split(","):
        value = value.strip()
        if value.isdigit():
            configured.add(int(value))
    return configured or DEFAULT_ADMIN_IDS


def parse_channels(raw: str, fallback: dict[str, str]) -> dict[str, str | int]:
    try:
        value = json.loads(raw) if raw else fallback
        if not isinstance(value, dict):
            raise ValueError
        return {str(name): channel for name, channel in value.items()}
    except (TypeError, ValueError, json.JSONDecodeError):
        logging.warning("Invalid channel JSON; using safe defaults")
        return dict(fallback)


SOURCE_CHANNELS = parse_channels(
    os.getenv("TELEGRAM_SOURCE_CHANNELS", ""),
    {"AnimeMM User Links": "@animemmuserlinkcollection"},
)
TARGET_CHANNELS = parse_channels(
    os.getenv("TELEGRAM_TARGET_CHANNELS", ""),
    {"AnimeOngoing MM": "@AnimeOngoing_MM"},
)
# Keep authorization deliberately fixed to the three IDs requested by the owner.
# TELEGRAM_ADMIN_IDS remains in .env.example for documentation/deployment clarity,
# but no username or extra environment value can silently grant admin access.
ADMIN_IDS = DEFAULT_ADMIN_IDS
DATA_FILE = Path(os.getenv("BOT_DATA_FILE", "bot_data.json"))
MAX_WARNINGS = 3
DRAFT_PREFIX = os.getenv("DRAFT_PREFIX", "").strip()
DRAFT_SUFFIX = os.getenv("DRAFT_SUFFIX", "").strip()

BANNED_PATTERNS = [
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"\b(spam|scam|hack|virus|malware)\b",
        r"\b(xxx|adult|porn|18\+)\b",
        r"\b(buy|sell|crypto|bitcoin)\b",
    )
]

WELCOME_MESSAGE = (
    "🎉 *{chat_name} မှ ကြိုဆိုပါတယ်!\n\n"
    "မင်္ဂလာပါ {user_name}။\n\n"
    "📋 *စည်းကမ်းချက်များ*\n"
    "• Spam၊ scam နှင့် ကြော်ငြာ မပို့ရ\n"
    "• မသင့်လျော်သော အကြောင်းအရာ မပို့ရ\n"
    "• အဖွဲ့ဝင်များကို လေးစားစွာ ဆက်ဆံရ\n"
    "• ပြင်ပ link များကို ခွင့်ပြုချက်မရှိဘဲ မပို့ရ\n\n"
    "⚠️ စည်းကမ်းဖောက်ဖျက်ပါက သတိပေးခြင်း သို့မဟုတ် ဖယ်ရှားခြင်း ပြုလုပ်နိုင်ပါတယ်။"
)

RULES_MESSAGE = (
    "📋 *စည်းကမ်းချက်များ*\n\n"
    "1. လူတိုင်းကို လေးစားစွာ ဆက်ဆံပါ။\n"
    "2. Spam၊ scam၊ မသင့်လျော်သော အကြောင်းအရာ မပို့ပါနှင့်။\n"
    "3. ခွင့်ပြုချက်မရှိဘဲ ပြင်ပ link/ကြော်ငြာ မပို့ပါနှင့်။\n"
    "4. Channel အကြောင်းအရာနှင့် သက်ဆိုင်သော post များသာ ပို့ပါ။\n\n"
    "⚠️ ပထမအကြိမ် သတိပေး၊ ဒုတိယအကြိမ် နောက်ဆုံးသတိပေး၊ တတိယအကြိမ် ဖယ်ရှားပါမည်။"
)

logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper(), logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("telegram_moderation_bot")


def load_data() -> dict[str, Any]:
    if not DATA_FILE.exists():
        return {"warnings": {}, "copy_success": 0, "copy_failed": 0, "moderated": 0}
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        logger.exception("Could not load data file")
        return {"warnings": {}, "copy_success": 0, "copy_failed": 0, "moderated": 0}


def save_data(data: dict[str, Any]) -> None:
    DATA_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def is_admin(user_id: int | None) -> bool:
    return user_id is not None and user_id in ADMIN_IDS


def admin_denied_text() -> str:
    return "❌ Admin များသာ သုံးနိုင်ပါတယ်။"


def channel_label(channels: dict[str, str | int]) -> str:
    if not channels:
        return "မရှိသေးပါ"
    return "\n".join(f"{index}. {name} — `{channel}`" for index, (name, channel) in enumerate(channels.items(), 1))


class ModerationBot:
    def __init__(self) -> None:
        self.data = load_data()
        self.target_channels = dict(TARGET_CHANNELS)

        saved_targets = self.data.get("target_channels", {})
        if isinstance(saved_targets, dict):
            self.target_channels.update(saved_targets)

    def persist(self) -> None:
        self.data["target_channels"] = self.target_channels
        self.data["updated_at"] = datetime.now(timezone.utc).isoformat()
        save_data(self.data)

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("📋 စည်းကမ်းချက်များ", callback_data="rules")],
                [InlineKeyboardButton("📚 အကူအညီ", callback_data="help")],
                [InlineKeyboardButton("📡 Channel စာရင်း", callback_data="channels")],
            ]
        )
        await update.effective_message.reply_text(
            "🤖 *Bot အလုပ်လုပ်နေပါပြီ*\n\n"
            "ခလုပ်များကို နှိပ်၍ အသုံးပြုနိုင်ပါတယ်။\n"
            "အများသုံး command များအတွက် /help ကို နှိပ်ပါ။",
            parse_mode="Markdown",
            reply_markup=keyboard,
        )

    async def rules(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        await update.effective_message.reply_text(RULES_MESSAGE, parse_mode="Markdown")

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        text = (
            "📚 *အကူအညီ*\n\n"
            "*အများသုံး Commands*\n"
            "/start — Bot အလုပ်လုပ်နေ/မနေ\n"
            "/rules — စည်းကမ်းချက်များ\n"
            "/help — အကူအညီ\n"
            "/channels — သတ်မှတ်ထားသော channel စာရင်း\n\n"
            "*Admin Commands*\n"
            "/status — Bot အခြေအနေ၊ warning နှင့် channel အရေအတွက်\n"
            "/addchannel နာမည် @channel — target channel ထည့်ရန်\n"
            "/removechannel နာမည် — target channel ဖျက်ရန်\n"
            "/post စာသား — target channel အားလုံးသို့ ပို့ရန်\n"
            "/stats — သုံးစွဲသူနှင့် warning စာရင်းအင်း\n\n"
            "*Manual Draft Mode*\n"
            "Admin account မှ Bot private chat သို့ photo/video ပို့ပါ။\n"
            "Bot က caption ပြင်ပြီး ပြန်ပို့ပေးပါမည်။ ထို့နောက် သင့် channel တွင် ကိုယ်တိုင် post တင်နိုင်ပါတယ်။\n\n"
            "❗ Admin command များကို သတ်မှတ်ထားသော admin ID ၃ ယောက်သာ သုံးနိုင်ပါတယ်။"
        )
        await update.effective_message.reply_text(text, parse_mode="Markdown")

    async def channels(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        text = "📡 *Target Channel စာရင်း*\n\n" + channel_label(self.target_channels)
        await update.effective_message.reply_text(text, parse_mode="Markdown")

    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not is_admin(update.effective_user.id if update.effective_user else None):
            await update.effective_message.reply_text(admin_denied_text())
            return
        warnings = self.data.get("warnings", {})
        await update.effective_message.reply_text(
            "✅ *Bot အခြေအနေ: အလုပ်လုပ်နေပါပြီ*\n\n"
            f"⚠️ သတိပေးခံထားရသူ: {len(warnings)} ယောက်\n"
            f"📡 Source channel: {len(SOURCE_CHANNELS)} ခု\n"
            f"🎯 Target channel: {len(self.target_channels)} ခု\n"
            f"📨 Auto-copy အောင်မြင်: {self.data.get('copy_success', 0)} ခု\n"
            f"❌ Auto-copy မအောင်မြင်: {self.data.get('copy_failed', 0)} ခု",
            parse_mode="Markdown",
        )

    async def addchannel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not is_admin(update.effective_user.id if update.effective_user else None):
            await update.effective_message.reply_text(admin_denied_text())
            return
        if len(context.args) != 2:
            await update.effective_message.reply_text(
                "📝 အသုံးပြုပုံ:\n/addchannel ChannelName @channel\n\n"
                "Bot ကို အဲဒီ channel မှာ admin အဖြစ် ထည့်ထားရပါမယ်။"
            )
            return
        name, channel = context.args
        if not channel.startswith("@") and not channel.lstrip("-").isdigit():
            await update.effective_message.reply_text("❌ Channel username သို့မဟုတ် numeric ID မှားနေပါတယ်။")
            return
        if channel.lstrip("-").isdigit():
            channel = int(channel)
        try:
            chat = await context.bot.get_chat(channel)
            member = await context.bot.get_chat_member(chat.id, context.bot.id)
            if member.status not in {"administrator", "creator"}:
                await update.effective_message.reply_text("❌ Bot ကို ဒီ channel မှာ admin အဖြစ် ထည့်ပေးပါ။")
                return
            self.target_channels[name] = channel
            self.persist()
            await update.effective_message.reply_text(f"✅ `{name}` ကို target channel အဖြစ် ထည့်ပြီးပါပြီ။", parse_mode="Markdown")
        except TelegramError:
            logger.exception("Channel validation failed")
            await update.effective_message.reply_text("❌ Channel မတွေ့ပါ၊ ID မှားနေပါသည်၊ သို့မဟုတ် Bot admin မဟုတ်ပါ။")

    async def removechannel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not is_admin(update.effective_user.id if update.effective_user else None):
            await update.effective_message.reply_text(admin_denied_text())
            return
        if len(context.args) != 1:
            await update.effective_message.reply_text("📝 အသုံးပြုပုံ: /removechannel ChannelName")
            return
        name = context.args[0]
        if name not in self.target_channels:
            await update.effective_message.reply_text("❌ Channel ရှာမတွေ့ပါ။")
            return
        del self.target_channels[name]
        self.persist()
        await update.effective_message.reply_text(f"✅ `{name}` ကို ဖျက်ပြီးပါပြီ။", parse_mode="Markdown")

    async def post(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not is_admin(update.effective_user.id if update.effective_user else None):
            await update.effective_message.reply_text(admin_denied_text())
            return
        if not context.args:
            await update.effective_message.reply_text("📝 အသုံးပြုပုံ: /post ပို့လိုသောစာသား")
            return
        text = " ".join(context.args)
        success = failed = 0
        for channel in self.target_channels.values():
            try:
                await context.bot.send_message(chat_id=channel, text=text)
                success += 1
            except TelegramError:
                failed += 1
                logger.exception("Manual post failed for %s", channel)
        await update.effective_message.reply_text(f"📨 *ပို့ပြီးပါပြီ*\n✅ အောင်မြင်: {success}\n❌ မအောင်မြင်: {failed}", parse_mode="Markdown")

    async def stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not is_admin(update.effective_user.id if update.effective_user else None):
            await update.effective_message.reply_text(admin_denied_text())
            return
        warnings = self.data.get("warnings", {})
        total = sum(int(value) for value in warnings.values())
        await update.effective_message.reply_text(
            "📊 *စာရင်းအင်းများ*\n\n"
            f"👥 Warning ရရှိထားသူ: {len(warnings)} ယောက်\n"
            f"⚠️ Warning စုစုပေါင်း: {total} ကြိမ်\n"
            f"📨 Auto-copy အောင်မြင်: {self.data.get('copy_success', 0)} ခု\n"
            f"❌ Auto-copy မအောင်မြင်: {self.data.get('copy_failed', 0)} ခု",
            parse_mode="Markdown",
        )

    @staticmethod
    def prepare_caption(caption: str | None) -> str | None:
        """Prepare a caption without downloading or modifying the media file."""
        parts = [part.strip() for part in (caption or "").splitlines()]
        parts = [part for part in parts if part]
        body = "\n".join(parts)
        if DRAFT_PREFIX:
            body = f"{DRAFT_PREFIX}\n{body}" if body else DRAFT_PREFIX
        if DRAFT_SUFFIX:
            body = f"{body}\n{DRAFT_SUFFIX}" if body else DRAFT_SUFFIX
        return body or None

    async def handle_admin_draft(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Return an edited media copy to an admin for manual posting."""
        message = update.effective_message
        user = update.effective_user
        chat = update.effective_chat
        if not message or not user or not chat or chat.type != "private" or not is_admin(user.id):
            return

        # Commands are handled by CommandHandler and must not be treated as drafts.
        if message.text and message.text.startswith("/"):
            return

        caption = self.prepare_caption(message.caption)
        try:
            await context.bot.copy_message(
                chat_id=user.id,
                from_chat_id=chat.id,
                message_id=message.message_id,
                caption=caption,
            )
            await context.bot.send_message(
                chat_id=user.id,
                text=(
                    "✅ *Draft ပြင်ပြီးပါပြီ။*\n\n"
                    "အပေါ်က photo/video ကို သင့်ပိုင် channel သို့ ကိုယ်တိုင် ပြန်တင်နိုင်ပါတယ်။\n"
                    "ဒီ mode က သူများ channel ထဲသို့ Bot ကိုယ်တိုင် ဝင်တင်ပေးခြင်း မဟုတ်ပါ။"
                ),
                parse_mode="Markdown",
            )
        except TelegramError:
            logger.exception("Could not prepare admin draft")
            await message.reply_text("❌ Draft ပြန်ပို့မရပါ။ Photo/video ဖိုင်အရွယ်အစား သို့မဟုတ် caption ကို စစ်ပါ။")

    async def handle_new_member(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        member_update = update.chat_member
        if not member_update or not member_update.new_chat_member:
            return
        member = member_update.new_chat_member
        if member.status not in {"member", "restricted"} or member.user.is_bot:
            return
        chat = update.effective_chat
        if chat:
            await context.bot.send_message(
                chat_id=chat.id,
                text=WELCOME_MESSAGE.format(chat_name=chat.title or "ကျွန်ုပ်တို့အဖွဲ့", user_name=member.user.first_name),
                parse_mode="Markdown",
            )

    async def moderate_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        message = update.effective_message
        user = update.effective_user
        if not message or not user or is_admin(user.id):
            return
        text = message.text or message.caption or ""
        if not any(pattern.search(text) for pattern in BANNED_PATTERNS):
            return
        key = f"{message.chat_id}:{user.id}"
        warnings = self.data.setdefault("warnings", {})
        warnings[key] = int(warnings.get(key, 0)) + 1
        count = warnings[key]
        self.data["moderated"] = int(self.data.get("moderated", 0)) + 1
        self.persist()
        try:
            await message.delete()
        except TelegramError:
            logger.warning("Could not delete violating message", exc_info=True)
        if count >= MAX_WARNINGS:
            try:
                await context.bot.ban_chat_member(message.chat_id, user.id)
                text_out = f"❌ {user.mention_html()} ကို စည်းကမ်းဖောက်ဖျက်မှု ၃ ကြိမ်ကြောင့် ဖယ်ရှားလိုက်ပါပြီ။"
            except TelegramError:
                text_out = f"⚠️ {user.mention_html()} ကို ဖယ်ရှားရန် Bot permission မလုံလောက်ပါ။"
        elif count == 2:
            text_out = f"⚠️ {user.mention_html()} — နောက်ဆုံးသတိပေးချက် (2/3)။ နောက်တစ်ကြိမ် ထပ်မဖောက်ဖျက်ပါနှင့်။"
        else:
            text_out = f"⚠️ {user.mention_html()} — သတိပေးချက် (1/3)။ သင့်စာကို ဖျက်လိုက်ပါပြီ။"
        await context.bot.send_message(chat_id=message.chat_id, text=text_out, parse_mode="HTML")

    async def copy_source_post(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        message = update.channel_post
        if not message or not message.chat:
            return
        source_username = f"@{message.chat.username}" if message.chat.username else None
        allowed = message.chat.id in SOURCE_CHANNELS.values() or source_username in SOURCE_CHANNELS.values()
        if not allowed:
            return
        for target in self.target_channels.values():
            try:
                await context.bot.copy_message(chat_id=target, from_chat_id=message.chat.id, message_id=message.message_id)
                self.data["copy_success"] = int(self.data.get("copy_success", 0)) + 1
            except TelegramError:
                self.data["copy_failed"] = int(self.data.get("copy_failed", 0)) + 1
                logger.exception("Auto-copy failed from %s to %s", message.chat.id, target)
        self.persist()

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        query = update.callback_query
        if not query:
            return
        await query.answer()
        if query.data == "rules":
            await query.edit_message_text(RULES_MESSAGE, parse_mode="Markdown")
        elif query.data == "help":
            await query.edit_message_text("📚 အကူအညီကို /help command ဖြင့် ကြည့်နိုင်ပါတယ်။")
        elif query.data == "channels":
            await query.edit_message_text("📡 *Target Channel စာရင်း*\n\n" + channel_label(self.target_channels), parse_mode="Markdown")

    def run(self) -> None:
        application = Application.builder().token(BOT_TOKEN).build()
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("rules", self.rules))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("channels", self.channels))
        application.add_handler(CommandHandler("status", self.status))
        application.add_handler(CommandHandler("addchannel", self.addchannel))
        application.add_handler(CommandHandler("removechannel", self.removechannel))
        application.add_handler(CommandHandler("post", self.post))
        application.add_handler(CommandHandler("stats", self.stats))
        application.add_handler(CallbackQueryHandler(self.button_callback))
        application.add_handler(ChatMemberHandler(self.handle_new_member, ChatMemberHandler.CHAT_MEMBER))
        application.add_handler(
            MessageHandler(
                filters.ChatType.PRIVATE
                & (filters.PHOTO | filters.VIDEO | filters.Document.ALL | filters.ANIMATION | filters.AUDIO | filters.VOICE)
                & ~filters.COMMAND,
                self.handle_admin_draft,
            ),
            group=0,
        )
        application.add_handler(MessageHandler(filters.ALL, self.copy_source_post), group=1)
        application.add_handler(MessageHandler(filters.TEXT | filters.CAPTION, self.moderate_message), group=2)
        logger.info("Bot started with %d admins, %d sources, %d targets", len(ADMIN_IDS), len(SOURCE_CHANNELS), len(self.target_channels))
        application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    ModerationBot().run()
