# Telegram Movie Bot — Termux/24-7 Setup

ဒီ repository ရှိ `bot.py` သည် မူရင်း moderation/welcome/forward bot ဖြစ်သည်။ Poster OCR၊ button workflow၊ AI synopsis/hashtags နှင့် channel round-robin posting ပါသော workflow ကို `movie_bot.py` အဖြစ် သီးခြားထည့်ထားသည်။

## Termux install

```bash
pkg update -y
pkg install git python -y
cd ~
rm -rf telegram-moderation-botp
git clone https://github.com/jue32583-tech/telegram-moderation-botp.git
cd telegram-moderation-botp
python -m pip install -r requirements.txt
cp .env.example .env
nano .env
```

Termux တွင် `python -m pip install --upgrade pip` မလုပ်ပါနှင့်။ `Installing pip is forbidden` သည် ပုံမှန်ဖြစ်သည်။

## `.env`

```env
BOT_TOKEN=BotFather မှ အသစ်ထုတ်ထားသော token
ADMIN_IDS=6081621017,6940887457,6432487408
TARGET_CHANNELS=@channelhingo,@onepiecemmk,@chanpingo,@Cartoonmovie2002,@channeliingo,@allmovie00099,@channelaingo,@channeldogo
LOG_LEVEL=INFO
STATE_FILE=bot_state.json
AI_API_KEY=
AI_BASE_URL=https://api.openai.com/v1
AI_MODEL=gpt-4o-mini
```

Token ကို GitHub ထဲ မတင်ပါနှင့်။ `.gitignore` ထဲ `.env` ပါပြီးသားဖြစ်ရမည်။

## Telegram permission

Channel ၈ ခုတိုင်းမှာ bot ကို Administrator ထည့်ပြီး `Post Messages` permission ဖွင့်ပါ။ Bot ကို `/start` ပို့မည့် account ID သည် `ADMIN_IDS` ထဲပါရမည်။

## Test

```bash
python -m py_compile bot.py movie_bot.py
# မူရင်း moderation bot
python bot.py
# သို့မဟုတ် OCR/movie button workflow
python movie_bot.py
```

`movie_bot.py` သို့ ပုံပို့ပြီး `🔎 ပုံထဲက Movie နာမည်ဖတ်မည်` ကိုနှိပ်လျှင် Vision API ဖြင့် poster ထဲက စာကို ဖတ်ပါမည်။ `Preview` စစ်ပြီးမှ `🚀 တင်မည်` ကိုနှိပ်ပါ။

## ဖုန်းပိတ်ထားချိန် run ခြင်း

Termux သည် ဖုန်းနှင့်အတူ ပိတ်နိုင်သောကြောင့် Android battery restriction ကို ဖြုတ်ပါ။

```bash
termux-wake-lock
nohup python movie_bot.py > movie_bot.log 2>&1 &
tail -f movie_bot.log
```

Android Settings → Apps → Termux → Battery → **Unrestricted** သတ်မှတ်ပါ။ ဖုန်းကို လုံးဝ power off လုပ်ထားလျှင် Termux မည်သို့မျှ run မနိုင်ပါ။ ဖုန်းပိတ်ထားချိန်ပါ 24/7 လိုပါက ဒီ GitHub repo ကို Render/Railway/VPS ၏ Background Worker အဖြစ် deploy လုပ်ရမည်။ Deploy server ထဲတွင် Environment Variables အဖြစ်သာ secret များထည့်ပါ။

## Security

အရင်က chat သို့ GitHub သို့ ပေါ်ခဲ့သော Bot Token, GitHub Token, API key များကို revoke လုပ်ပြီး အသစ်ထုတ်ပါ။
