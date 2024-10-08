from pyrogram import Client, filters
from pyrogram.types import Message

from DnsXMusic import app  # Your bot's app

# Function to forward the message to @SaveMedia_bot and get a response
@app.on_message(filters.text & filters.private)
def forward_to_savemedia(client, message):
    user_link = message.text

    if "instagram.com" in user_link or "facebook.com" in user_link:
        # Forward the message to @SaveMedia_bot
        forward_message = client.send_message("@SaveMedia_bot", user_link)

        # Wait for response from @SaveMedia_bot (you can add a delay or timeout)
        forward_message = client.listen()  # listen for the reply from SaveMedia bot
        
        # Send the result back to the user
        client.send_message(message.chat.id, f"Here's your content: {forward_message.text}")

    else:
        client.send_message(message.chat.id, "Please send a valid social media link (Instagram, Facebook, etc.).")
