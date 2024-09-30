import requests
from pyrogram import Client, filters
from DnsXMusic import app

# API endpoint
API_URL = "https://chatgpt.apiitzasuraa.workers.dev/?question=hey"

# Function to handle the /geminis command in private chat
@app.on_message(filters.command(["era" "ra"], prefixes=["/", "!", ".", "e", "'E"]))
async def gemini(client, message):
    # Get the user message after the /geminis command
    user_message = message.text[len("/era"):].strip()
    
    if not user_message:
        await message.reply("Please provide a prompt after the /era command.")
        return
    
    # Send the request to the API
    response = requests.get(API_URL + user_message)
    
    if response.status_code == 200:
        json_response = response.json()
        bot_reply = json_response['candidates'][0]['content']['parts'][0]['text']
    else:
        bot_reply = "Sorry, I couldn't get a response from the API."
    
    # Reply to the user with the bot's response
    await message.reply_text(bot_reply)
