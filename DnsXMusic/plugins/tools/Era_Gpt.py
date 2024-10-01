import requests
from pyrogram import Client, filters
from DnsXMusic import app

@Client.on_message(filters.command("bard"))
async def gemini(client, message):
    user_message = message.text[len("/bard "):].strip()
    
    if not user_message:
        await message.reply_text("Please provide a question after the /bard command.")
        return
    
    try:
        response = requests.get(f"https://gemini.apiitzasuraa.workers.dev/?prompt={user_message}")
        
        if response.status_code == 200:
            json_response = response.json()
            bot_reply = json_response['candidates'][0]['content']['parts'][0]['text']
        else:
            bot_reply = "Sorry, I couldn't get a response from the API."
    
    except Exception as e:
        bot_reply = f"An error occurred: {e}"
    
    await message.reply_text(bot_reply)