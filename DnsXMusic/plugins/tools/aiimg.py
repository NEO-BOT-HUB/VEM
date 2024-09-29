import requests
from pyrogram import Client, filters
from DnsXMusic import app

@app.on_message(filters.command(["make", "ake"], prefixes=["/", "!", ".", "M", "m"]))
async def animeimg(client, message):
    prompt = ' '.join(message.command[1:])
    if not prompt:
        await message.reply_text('ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴘʀᴏᴍᴘᴛ.')
        return
    try:
        response = requests.get(f"https://animeimg.apiitzasuraa.workers.dev/?prompt={prompt}")
        response.raise_for_status()
        image_url = response.json().get('image')
        if image_url:
            await message.reply_photo(photo=image_url, caption=f"ɢᴇɴᴇʀᴀᴛᴇᴅ ᴀɴɪᴍᴇ-sᴛʏʟᴇ ɪᴍᴀɢᴇ ғᴏʀ: {prompt}")
        else:
            await message.reply_text("No image found.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
