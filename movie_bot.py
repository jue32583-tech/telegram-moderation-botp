import base64
import json
import logging
import os
from pathlib import Path
from typing import Any

import httpx
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application, CallbackQueryHandler, CommandHandler, ContextTypes,
    MessageHandler, filters,
)

load_dotenv()
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
ADMIN_IDS = {int(x.strip()) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip().isdigit()}
TARGET_CHANNELS = [x.strip() for x in os.getenv("TARGET_CHANNELS", "").split(",") if x.strip()]
STATE_FILE = Path(os.getenv("STATE_FILE", "bot_state.json"))
AI_API_KEY = os.getenv("AI_API_KEY", "").strip()
AI_BASE_URL = os.getenv("AI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
AI_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN မရှိပါ။ .env ဖိုင်ထဲထည့်ပါ။")
if not TARGET_CHANNELS:
    raise RuntimeError("TARGET_CHANNELS မရှိပါ။ .env ဖိုင်ထဲထည့်ပါ။")


def load_state() -> dict[str, Any]:
    if not STATE_FILE.exists():
        return {"next_index": 0}
    try:
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        log.exception("State file မဖတ်နိုင်ပါ။ index=0 ဖြင့် ပြန်စမည်။")
        return {"next_index": 0}


def save_state(state: dict[str, Any]) -> None:
    tmp = STATE_FILE.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(STATE_FILE)


def is_admin(update: Update) -> bool:
    user = update.effective_user
    return bool(user and user.id in ADMIN_IDS)


def menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📸 ပုံ/ဗီဒီယိုအသစ်", callback_data="new")],
        [InlineKeyboardButton("📊 လုပ်ဆောင်ချက်များ", callback_data="about"), InlineKeyboardButton("❌ ပယ်ဖျက်", callback_data="cancel")],
    ])


def editor_menu() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🎬 Movie name", callback_data="field:title"), InlineKeyboardButton("📝 ဇာတ်ညွှန်း", callback_data="field:synopsis")],
        [InlineKeyboardButton("🔗 Video link 1", callback_data="field:link1"), InlineKeyboardButton("🔗 Video link 2", callback_data="field:link2")],
        [InlineKeyboardButton("#️⃣ Hashtags", callback_data="field:hashtags")],
        [InlineKeyboardButton("🔎 ပုံထဲက Movie နာမည်ဖတ်မည်", callback_data="ocr")],
        [InlineKeyboardButton("🤖 AI ဖြင့် ဇာတ်ညွှန်း/hashtags", callback_data="ai" )],
        [InlineKeyboardButton("👀 Preview", callback_data="preview"), InlineKeyboardButton("🚀 တင်မည်", callback_data="publish")],
        [InlineKeyboardButton("❌ ပယ်ဖျက်", callback_data="cancel")],
    ])


def draft(context: ContextTypes.DEFAULT_TYPE) -> dict[str, Any]:
    return context.user_data.setdefault("draft", {})


def render_preview(d: dict[str, Any]) -> str:
    title = d.get("title") or "(မဖြည့်ရသေးပါ)"
    synopsis = d.get("synopsis") or "(မဖြည့်ရသေးပါ)"
    links = "\n".join(x for x in [d.get("link1"), d.get("link2")] if x) or "(မဖြည့်ရသေးပါ)"
    tags = d.get("hashtags") or "(မဖြည့်ရသေးပါ)"
    return f"🎬 {title}\n\n📝 {synopsis}\n\n🔗 Links:\n{links}\n\n{tags}"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_admin(update):
        await update.message.reply_text("ဤ bot ကို admin များသာ အသုံးပြုနိုင်ပါသည်။")
        return
    await update.message.reply_text(
        "မင်္ဂလာပါ။ ပုံ/ဗီဒီယိုကို ဒီ bot ထံ ပို့ပြီး ခလုတ်များဖြင့် အချက်အလက်ဖြည့်ပါ။\n"
        "တင်မည့် channel သည် round-robin အစီအစဉ်ဖြင့် တစ်ခါလျှင် တစ်ခုရွေးပါမည်။",
        reply_markup=menu(),
    )


async def receive_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_admin(update):
        return
    msg = update.effective_message
    d = draft(context)
    d.clear()
    d["chat_id"] = msg.chat_id
    d["message_id"] = msg.message_id
    d["media_type"] = "photo" if msg.photo else "video"
    d["caption"] = msg.caption or ""
    if msg.photo:
        d["file_id"] = msg.photo[-1].file_id
    elif msg.video:
        d["file_id"] = msg.video.file_id
    await msg.reply_text("Media လက်ခံပြီးပါပြီ။ အောက်ကခလုတ်နဲ့ အချက်အလက်ဖြည့်ပါ။", reply_markup=editor_menu())


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    q = update.callback_query
    await q.answer()
    if not is_admin(update):
        await q.edit_message_text("Admin မဟုတ်ပါသဖြင့် အသုံးပြုခွင့်မရှိပါ။")
        return
    if q.data == "new":
        await q.edit_message_text("ပုံ သို့မဟုတ် ဗီဒီယိုကို ဒီ chat ထဲ ပို့ပါ။")
        return
    if q.data == "about":
        await q.edit_message_text("လုပ်နိုင်သောအရာများ:\n• ပုံ/ဗီဒီယို လက်ခံခြင်း\n• Movie name, synopsis, links, hashtags ဖြည့်ခြင်း\n• Preview/အတည်ပြု\n• Channel round-robin posting\n• AI synopsis/hashtags (API key ထည့်ထားမှ)", reply_markup=menu())
        return
    if q.data == "cancel":
        context.user_data.pop("draft", None)
        context.user_data.pop("waiting", None)
        await q.edit_message_text("ပယ်ဖျက်ပြီးပါပြီ။", reply_markup=menu())
        return
    if q.data.startswith("field:"):
        field = q.data.split(":", 1)[1]
        context.user_data["waiting"] = field
        labels = {"title": "Movie name", "synopsis": "ဇာတ်ညွှန်း", "link1": "Video link 1", "link2": "Video link 2", "hashtags": "Hashtags"}
        await q.edit_message_text(f"{labels[field]} ကို စာသားနဲ့ ပို့ပါ။")
        return
    if q.data == "ocr":
        d = draft(context)
        if not AI_API_KEY:
            await q.message.reply_text("OCR အတွက် .env ထဲမှာ AI_API_KEY ထည့်ပြီး bot ကို restart လုပ်ပါ။", reply_markup=editor_menu())
            return
        if d.get("media_type") != "photo":
            await q.message.reply_text("OCR အတွက် အရင်ဆုံး ပုံတစ်ပုံ ပို့ပါ။ Video တစ်ခုတည်းမှ စာဖတ်ခြင်းကို ဒီ version မထောက်ပံ့သေးပါ။", reply_markup=editor_menu())
            return
        await q.edit_message_text("ပုံထဲက စာကို AI က ဖတ်နေပါတယ်…")
        try:
            result = await ocr_title(context, d)
            d["title"] = result.get("title", "")
            d["ocr_text"] = result.get("raw_text", "")
            await q.message.reply_text(
                f"✅ Movie name ဖတ်ပြီးပါပြီ။\n\n🎬 {d.get('title') or '(မတွေ့ပါ)'}\n\n"
                "မမှန်ပါက Movie name ခလုတ်ဖြင့် ပြန်ပြင်ပါ။",
                reply_markup=editor_menu(),
            )
        except Exception:
            log.exception("OCR error")
            await q.message.reply_text("OCR မအောင်မြင်ပါ။ ပုံကြည်လင်မှု၊ AI_API_KEY နှင့် AI_MODEL ကို စစ်ပါ။", reply_markup=editor_menu())
        return
    if q.data == "ai":
        d = draft(context)
        if not AI_API_KEY:
            await q.edit_message_text("AI မဖွင့်ရသေးပါ။ .env ထဲမှာ AI_API_KEY ထည့်ပြီး bot ကို restart လုပ်ပါ။", reply_markup=editor_menu())
            return
        await q.edit_message_text("AI က synopsis/hashtags ရေးနေပါတယ်…")
        try:
            result = await ai_generate(d)
            d.update(result)
            await q.message.reply_text("AI ဖြည့်ပေးပြီးပါပြီ။ ပြန်စစ်ပြီး Preview သို့မဟုတ် တင်မည်ကို နှိပ်ပါ။", reply_markup=editor_menu())
        except Exception:
            log.exception("AI error")
            await q.message.reply_text("AI မအောင်မြင်ပါ။ API key/model/base URL ကို စစ်ပါ။", reply_markup=editor_menu())
        return
    if q.data == "preview":
        await q.message.reply_text(render_preview(draft(context)), reply_markup=editor_menu())
        return
    if q.data == "publish":
        await publish(update, context)


async def text_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not is_admin(update) or not context.user_data.get("waiting"):
        return
    field = context.user_data.pop("waiting")
    d = draft(context)
    d[field] = (update.message.text or "").strip()
    await update.message.reply_text(f"{field} သိမ်းပြီးပါပြီ။", reply_markup=editor_menu())


async def ai_generate(d: dict[str, Any]) -> dict[str, str]:
    prompt = f"Movie name: {d.get('title','')}\nExisting caption: {d.get('caption','')}\n"
    body = {"model": AI_MODEL, "temperature": 0.4, "messages": [
        {"role": "system", "content": "You write concise Burmese movie synopsis and 8 safe hashtags. Do not invent cast, rating, or plot details that are not provided. Return JSON with synopsis and hashtags."},
        {"role": "user", "content": prompt},
    ], "response_format": {"type": "json_object"}}
    async with httpx.AsyncClient(timeout=45) as client:
        r = await client.post(f"{AI_BASE_URL}/chat/completions", headers={"Authorization": f"Bearer {AI_API_KEY}"}, json=body)
        r.raise_for_status()
        content = r.json()["choices"][0]["message"]["content"]
    data = json.loads(content)
    return {"synopsis": str(data.get("synopsis", "")), "hashtags": str(data.get("hashtags", ""))}


async def ocr_title(context: ContextTypes.DEFAULT_TYPE, d: dict[str, Any]) -> dict[str, str]:
    """Telegram photo ကို data URL အဖြစ် Vision API သို့ပို့ပြီး title/raw text ပြန်ယူသည်."""
    tg_file = await context.bot.get_file(d["file_id"])
    image_bytes = await tg_file.download_as_bytearray()
    image_b64 = base64.b64encode(bytes(image_bytes)).decode("ascii")
    body = {
        "model": AI_MODEL,
        "temperature": 0,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": "Read all visible text in this movie poster/image. Identify the movie title. Return JSON only with title and raw_text. If no title is visible, return an empty title. Do not invent a title."},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}", "detail": "high"}},
            ],
        }],
        "response_format": {"type": "json_object"},
    }
    async with httpx.AsyncClient(timeout=60) as client:
        r = await client.post(f"{AI_BASE_URL}/chat/completions", headers={"Authorization": f"Bearer {AI_API_KEY}"}, json=body)
        r.raise_for_status()
        content = r.json()["choices"][0]["message"]["content"]
    result = json.loads(content)
    return {"title": str(result.get("title", "")).strip(), "raw_text": str(result.get("raw_text", "")).strip()}


async def publish(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    d = draft(context)
    if not d.get("message_id"):
        await update.callback_query.message.reply_text("အရင်ဆုံး ပုံ/ဗီဒီယို ပို့ပါ။")
        return
    if not d.get("title"):
        await update.callback_query.message.reply_text("Movie name မဖြည့်ရသေးပါ။")
        return
    state = load_state()
    index = int(state.get("next_index", 0)) % len(TARGET_CHANNELS)
    target = TARGET_CHANNELS[index]
    caption = render_preview(d)
    try:
        await context.bot.send_chat_action(chat_id=target, action=ChatAction.UPLOAD_VIDEO if d.get("media_type") == "video" else ChatAction.UPLOAD_PHOTO)
        await context.bot.copy_message(chat_id=target, from_chat_id=d["chat_id"], message_id=d["message_id"], caption=caption)
        state["next_index"] = (index + 1) % len(TARGET_CHANNELS)
        save_state(state)
        await update.callback_query.message.reply_text(f"✅ တင်ပြီးပါပြီ။\nChannel: {target}\nနောက်တစ်ခါ: {TARGET_CHANNELS[state['next_index']]}", reply_markup=menu())
        context.user_data.pop("draft", None)
    except Exception as e:
        log.exception("Publish failed")
        await update.callback_query.message.reply_text(f"❌ မတင်နိုင်ပါ။ {type(e).__name__}\nBot ကို channel ထဲ admin ထည့်ထားမထား စစ်ပါ။", reply_markup=editor_menu())


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, receive_media))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_input))
    log.info("Bot စတင်ပါပြီ။ Channels=%s", TARGET_CHANNELS)
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == "__main__":
    main()
