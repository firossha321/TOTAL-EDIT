from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from openai import OpenAI
import asyncio

loop = asyncio.get_event_loop()

SUPPORT_GROUP = -1001885126003
SUPPORT_LINK = 'https://t.me/chatgptbotsupport'
OPENAI_API = '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'

START_MESSAGE = """ʜᴇʟʟᴏ, {user},
ᴍʏ ɴᴀᴍᴇ ɪꜱ ᴀɪ ʙᴏᴛ
ɪ ᴀᴍ ᴀɴ ᴀɪ ʙᴏᴛ ᴍᴀᴅᴇ ʙʏ ꜰɪʀᴏꜱ
ʏᴏᴜ ᴄᴀɴ ᴀꜱᴋ ᴍᴇ qᴜᴇꜱᴛɪᴏɴ ʙʏ ᴩʟᴀᴄɪɴɢ ʏᴏᴜʀ qᴜᴇꜱᴛɪᴏɴ ᴀꜰᴛᴇʀ /openai ᴄᴏᴍᴍᴀɴᴅ
ɴᴏᴡ ᴀꜱᴋ ʏᴏᴜʀ qᴜᴇꜱᴛɪᴏɴ ?
ᴇxᴀᴍᴩʟᴇ : /openai who invented Ai ?"""

# AI setup
ai_client = OpenAI(api_key=OPENAI_API)

@app.on_message(filters.command("start"))
async def start(client, message):
    welcome_message = START_MESSAGE.format(user=message.from_user.first_name)
    btn1 = [[
            InlineKeyboardButton('Support Group', url=SUPPORT_LINK),
            InlineKeyboardButton('ADMIN',url='https://t.me/firossha')
        ]]
    await message.reply_text(welcome_message,reply_markup=InlineKeyboardMarkup(btn1))

@app.on_message(filters.command("openai"))
async def ask_question(client, message):
    if len(OPENAI_API) == 0:
        return await message.reply("OPENAI_API is empty")
    if message.chat.id != SUPPORT_GROUP:
        btn = [[
            InlineKeyboardButton('Support Group', url=SUPPORT_LINK)
        ]]
        return await message.reply("This command only working in support group.", reply_markup=InlineKeyboardMarkup(btn))
    try:
        text = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text("Command Incomplete!\nUsage: /openai your_question")
    stk = await message.reply_sticker("CAACAgUAAxkBAAIYJ2XA-H0GrHrCCetu4hHCN-3rss_EAAJfAQAC5k-5VFd6fFm2UUXSHgQ")
    try:
        response = ai_client.chat.completions.create(
            messages=[
                {"role": "user", "content": text}
            ],
            model="gpt-3.5-turbo"
        )
        await message.reply(f"User: {message.from_user.mention}\nQuery: <code>{text}</code>\n\nResults:\n\n<code>{response.choices[0].message.content}</code>")
        return await stk.delete()
    except Exception as e:
        await msg.edit(f'Error - <code>{e}</code>')
        return await stk.delete()