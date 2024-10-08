import random
import re
from pyrogram import Client, filters
from pyrogram.types import Message

from DnsXMusic import userbot as us, app
from DnsXMusic.core.userbot import assistants

# Social Media Download Bot Options
download_bots = ["@SaveMedia_bot", "@instasavegrambot"]

@app.on_message(filters.text & filters.private)
async def download_social_media(client: Client, message: Message):
    url = message.text

    # Check if message contains a valid Instagram or Facebook URL
    if "instagram.com" in url or "facebook.com" in url:
        # Select a random bot from the list
        bot_choice = random.choice(download_bots)

        # Choose an assistant bot (from DnsXMusic assistants)
        if 1 in assistants:
            assistant_bot = us.one  # Using the first assistant as an example

        # Send the media link to the chosen social media bot using assistant bot
        forwarded_message = await assistant_bot.send_message(bot_choice, url)

        # Notify the user that their request is being processed
        processing_msg = await message.reply("🔄 Processing your request, please wait...")

        # Wait for the bot's response and extract the content
        async for response in assistant_bot.search_messages(bot_choice):
            if response.text:
                # Extract media URLs from the response text
                media_urls = re.findall(r'(https?://\S+)', response.text)

                if media_urls:
                    # Send each media URL to the user
                    for media_url in media_urls:
                        await message.reply(f"Here's a media link: {media_url}")
                else:
                    await message.reply("⚠️ No media links found.")
                
                break

        # Clean up messages (optional)
        await forwarded_message.delete()
        await processing_msg.delete()

    else:
        await message.reply("⚠️ Please provide a valid Instagram or Facebook link.")
