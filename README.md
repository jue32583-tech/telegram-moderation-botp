# Telegram Moderation and Channel Copy Bot

A Python Telegram bot that provides Burmese user-facing commands, moderation, admin-only channel management, manual posting, and automatic copying of posts from approved source channels to approved target channels.

## Implemented behavior

- Burmese `/start`, `/rules`, `/help`, `/status`, `/channels`, `/addchannel`, `/removechannel`, `/post`, and `/stats` commands.
- Inline buttons on `/start` for rules, help, and channel list.
- Exactly three administrator IDs are trusted by the active `bot.py` implementation:
  - `6081621017` — `@waiyanphyo99`
  - `6940887457` — `@waiyan7861`
  - `6432487408` — `@Bingopop1991`
- Every admin-only command checks the numeric Telegram user ID. Usernames alone are never accepted as authorization.
- Three-strike moderation: delete violating text/captions, warn on strikes 1 and 2, and ban on strike 3 when the bot has permission.
- Source-channel allowlist: only configured source channels are copied.
- Target-channel allowlist: only configured target channels receive copies.
- `copy_message` preserves Telegram media, captions, links, and buttons. It does not add a logo or crop video.
- Persistent channel configuration and statistics are stored in `bot_data.json`.
- Manual media draft mode: an authorized admin can send a photo/video to the bot in a private chat; the bot cleans the caption and sends the prepared media back for manual reposting.

## Setup

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and set TELEGRAM_BOT_TOKEN.
python bot.py
```

The repository's code is written in English; bot responses are written in Burmese. The bot reads its token only from the `TELEGRAM_BOT_TOKEN` environment variable; it never stores a token in source code.

## Required Telegram permissions

1. Add the bot as an administrator to `@animemmuserlinkcollection` so it can receive channel posts. Telegram channel posts are delivered through the bot's `channel_post` update; the bot must be a member/admin of the source channel.
2. Add the bot as an administrator to `@AnimeOngoing_MM` and every target channel, with permission to post messages.
3. For group moderation and welcome messages, add the bot as an administrator with **Delete messages**, **Ban users**, and member-update visibility as appropriate.
4. Disable privacy mode with BotFather only if the bot must moderate ordinary group messages. Channel copying itself does not require disabling privacy mode.

## Commands

| Command | Access | Function |
|---|---|---|
| `/start` | Everyone | Burmese welcome message and buttons |
| `/rules` | Everyone | Rules |
| `/help` | Everyone | Command guide |
| `/channels` | Everyone | Target-channel list |
| `/status` | Admin IDs only | Warning, source, target, and copy status |
| `/addchannel Name @channel` | Admin IDs only | Validate and add a target channel |
| `/removechannel Name` | Admin IDs only | Remove a target channel |
| `/post message` | Admin IDs only | Send text to every target channel |
| `/stats` | Admin IDs only | Warning and copy statistics |

## Important limitation about source-channel copying

The bot can copy new posts only after it is added to the source channel and the source is listed in `TELEGRAM_SOURCE_CHANNELS`. It cannot read arbitrary third-party channels merely because a public link was supplied. Do not add channels you do not own or have permission to administer.

The bot copies the original Telegram message. If the post contains a logo, watermark, or video link, the bot does not automatically crop or edit it. Video/logo transformation would require a separate media-processing pipeline and may violate the source channel's rights.

## Manual media draft mode

When the source and target channels are not yours and cannot grant the bot administrator access, use this workflow:

1. Start the bot and open its private chat.
2. Send a movie photo, video, document, animation, audio, or voice message from one of the three authorized admin accounts.
3. The bot copies the media back to the same private chat and applies optional `DRAFT_PREFIX` and `DRAFT_SUFFIX` text.
4. Manually forward or repost the prepared media to your own channel.

The bot does not log in as a user, bypass channel permissions, scrape private/third-party channels, remove watermarks, or automatically publish to channels where it is not authorized. This manual mode is the supported alternative for third-party channels.

## Deployment

Use any always-on Python host. Set the start command to:

```bash
python bot.py
```

Set `TELEGRAM_BOT_TOKEN` as a secret environment variable in Railway. Do not use the old `BOT_TOKEN` variable, and do not paste bot tokens, API hashes, or other secrets into Python files or documentation. If a token was previously exposed, revoke it with BotFather and create a replacement before deployment.

## Configuration examples

```env
TELEGRAM_SOURCE_CHANNELS={"AnimeMM User Links":"@animemmuserlinkcollection"}
TELEGRAM_TARGET_CHANNELS={"AnimeOngoing MM":"@AnimeOngoing_MM"}
# Optional caption additions for manual media drafts.
# DRAFT_PREFIX=🎬 Anime Update
# DRAFT_SUFFIX=#AnimeMM
```

For private channels, use a numeric channel ID such as `-1001234567890` and ensure the bot is an administrator there.
