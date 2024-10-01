from pyrogram import Client, filters
from DnsXMusic.misc import SUDOERS
from DnsXMusic import app

@app.on_message(filters.command(["eco", "co"], prefixes=["/", "!", ".", "e", "E"]) & SUDOERS)
async def eco_reply(client, message):
    try:
        if not message.reply_to_message:
            await message.reply("Kripya iss command ka use karne ke liye kisi user ke message ka reply karein.")
            return
        
        # Command text ko extract karna
        command_text = message.text.split(None, 1)
        
        if len(command_text) < 2:
            await message.reply("Kripya /eco command ke baad ek message provide karein.")
            return
        
        # Reply karne ke liye message
        reply_message = command_text[1]
        
        # Original message ko delete karna
        await message.delete()
        
        # Reply bhejana
        await message.reply_to_message.reply(reply_message)
        
    except Exception as e:
        print(f"Error in eco_reply: {str(e)}")
        await message.reply("Kuch error aa gaya. Please try again.")
