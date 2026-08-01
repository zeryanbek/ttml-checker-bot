import os
import sys
import tempfile
import xml.etree.ElementTree as ET
import discord
from discord.ext import commands  
import grammar

TOKEN = os.environ.get("DISCORD_TOKEN")
if not TOKEN:
    print("set DISCORD_TOKEN environment variable")
    sys.exit(1)

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

MSG_LIMIT = 2000
REPORT_LIMIT = MSG_LIMIT - 100
SEP = "\N{BOX DRAWINGS LIGHT HORIZONTAL}" * 30


@bot.event
async def on_ready():
    print(f"logged in as {bot.user}")


def build_report(filename, errors, regional):
    total = len(errors) + len(regional)

    if total == 0:
        return f"Report for: {filename}\n{SEP}\nNo issues found \u2014 all checkable rules passed."

    parts = [f"Report for: {filename}", SEP]

    if regional:
        parts.append("Disclaimer: These lyrics contain word spellings that may differentiate depending on the songwriters region.")
        parts.append("")

    if errors:
        parts.append("\n".join(errors))

    if regional:
        parts.append(SEP)
        parts.append("Words to check English spelling:")
        parts.append("")
        parts.append("\n".join(regional))

    parts.append("")
    parts.append(f"Total issues: {total}")

    report = "\n".join(parts)
    if len(report) > REPORT_LIMIT:
        report = report[:REPORT_LIMIT - 50] + f"\n{SEP}\n(report truncated \u2014 too long)"

    return report


@bot.event
async def on_message(message):
    if message.author.bot or not message.attachments:
        return

    ttml_attachments = [a for a in message.attachments if a.filename.lower().endswith(".ttml")]
    if not ttml_attachments:
        return

    for attachment in ttml_attachments:
        await handle_ttml(message, attachment)


async def handle_ttml(message, attachment):
    tmp_path = None
    try:
        raw = await attachment.read()
        with tempfile.NamedTemporaryFile(suffix=".ttml", delete=False) as tmp:
            tmp.write(raw)
            tmp_path = tmp.name

        lyrics_text = grammar.extract_lyrics(tmp_path)
        errors, regional = grammar.process_lyrics_text(lyrics_text)
        report = build_report(attachment.filename, errors, regional)

        code_block = f"```\n{report}\n```"
        if len(code_block) > MSG_LIMIT:
            code_block = f"```\n{report[:REPORT_LIMIT]}\n```"

        await message.reply(code_block, mention_author=False)

    except discord.Forbidden:
        try:
            await message.reply("missing permissions to send messages here", mention_author=False)
        except discord.HTTPException:
            pass

    except ET.ParseError:
        await message.reply(f"`{attachment.filename}` is not valid XML/TTML", mention_author=False)

    except discord.HTTPException as e:
        await message.reply(f"discord error: {e}", mention_author=False)

    except Exception as e:
        await message.reply(f"couldnt process `{attachment.filename}`: {e}", mention_author=False)

    finally:
        if tmp_path:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

# TODO: maybe add a !check command
bot.run(TOKEN)