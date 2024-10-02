import requests
import random
import re
from MukeshAPI import api
from pyrogram import filters
from pyrogram.enums import ChatAction, ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from DnsXMusic import app
from prometheus_client import start_http_server, Counter

# Start Prometheus monitoring
start_http_server(8000)
request_counter = Counter('telegram_bot_requests_total', 'Total number of requests to the Telegram bot')

# List of supported emojis for reactions
EMOJI_LIST = [
    "👍", "👎", "❤️", "🔥", "🥳", "👏", "😁", "😂", "😲", "😱",
    "😢", "😭", "🎉", "😇", "😍", "😅", "💩", "🙏", "🤝", "🍓",
    "🎃", "👀", "💯", "😎", "🤖", "🐵", "👻", "🎄", "🥂", "🎅",
    "❄️", "✍️", "🎁", "🤔", "💔", "🥰", "😢", "🥺", "🙈", "🤡",
    "😋", "🎊", "🍾", "🌟", "👶", "🦄", "💤", "😷", "👩‍💻", "🍌",
    "🍓", "💀", "👩‍🏫", "🤝", "☠️", "🎯", "🍕", "🦾", "🔥", "💃"
]

# Function to send a random emoji reaction
async def react_with_random_emoji(client, message):
    try:
        emoji = random.choice(EMOJI_LIST)
        await app.send_reaction(message.chat.id, message.id, emoji)
    except Exception as e:
        print(f"Failed to send reaction: {str(e)}")

# Function to convert text to a more feminine, "girly" style
def to_feminine_style(text):
    # Replace some words with more feminine alternatives
    text = text.replace('hello', 'hiii')
    text = text.replace('how are you', 'how are you doing, sweetie?')
    text = text.replace('thank you', 'aww, thank you so much!')
    text = text.replace('sorry', 'oopsie, my bad!')
    text = text.replace('please', 'pretty please?')
    # Add more replacements as needed
    return text

# Function to add some feminine touches
def add_feminine_touch(text):
    interjections = [
        "Aww, ", "Ohh, ", "Tee hee, ", "Hmm, let me think... ",
        "Gosh, ", "Wow, ", "Tehee, "
    ]
    emojis = ["😊", "🥰", "😘", "😉", "😍", "💕", "💖"]
    
    text = random.choice(interjections) + text
    if random.random() < 0.5:  # 50% chance to add emoji
        text += " " + random.choice(emojis)
    return text

# Function to truncate text to a maximum of 50 words
def truncate_text(text, max_words=50):
    words = text.split()
    if len(words) > max_words:
        return ' '.join(words[:max_words]) + "..."
    return text

# Dictionary to store full messages
full_messages = {}

# Handler for "Read More" button
@app.on_callback_query(filters.regex(r"read_more:(\d+)"))
async def read_more_callback(client, callback_query):
    message_id = int(callback_query.data.split(":")[1])
    full_message = full_messages.get(message_id)

    if full_message:
        await callback_query.message.edit_text(full_message, parse_mode=ParseMode.MARKDOWN)
    else:
        await callback_query.message.edit_text("Message not found.", parse_mode=ParseMode.MARKDOWN)

# Handler for direct messages (DMs)
@app.on_message(filters.private)
async def gemini_dm_handler(client, message):
    request_counter.inc()
    await react_with_random_emoji(client, message)
    await app.send_chat_action(message.chat.id, ChatAction.TYPING)
    
    user_input = message.text

    try:
        response = api.gemini(user_input)
        x = response.get("results")
        image_url = response.get("image_url")

        if x:
            x = to_feminine_style(x)
            x = add_feminine_touch(x)
            truncated_response = truncate_text(x)
            full_messages[message.id] = x  # Store the full message using message ID as key

            if image_url:
                await message.reply_photo(
                    image_url,
                    caption=truncated_response,
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Read More", callback_data=f"read_more:{message.id}")]]
                    ),
                    quote=True
                )
            else:
                await message.reply_text(
                    truncated_response,
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("Read More", callback_data=f"read_more:{message.id}")]]
                    ),
                    quote=True
                )
        else:
            await message.reply_text(to_feminine_style("Oopsie, I don't have a response for that. Could you please try again, sweetie?"), quote=True)
    except requests.exceptions.RequestException as e:
        pass

# Handler for group chats when replying to the bot's message or mentioning the bot
@app.on_message(filters.group)
async def gemini_group_handler(client, message):
    request_counter.inc()
    bot_username = (await app.get_me()).username

    # Ensure that the message contains text
    if message.text:
        # Ignore message if it starts with '/'
        if message.text.startswith('/'):
            return

        # Check if the message is a reply to the bot's message
        if message.reply_to_message and message.reply_to_message.from_user.username == bot_username:
            await react_with_random_emoji(client, message)
            await app.send_chat_action(message.chat.id, ChatAction.TYPING)

            user_input = message.text.strip()
            try:
                response = api.gemini(user_input)
                x = response.get("results")
                image_url = response.get("image_url")

                if x:
                    x = to_feminine_style(x)
                    x = add_feminine_touch(x)
                    truncated_response = truncate_text(x)
                    full_messages[message.id] = x  # Store the full message

                    if image_url:
                        await message.reply_photo(
                            image_url,
                            caption=truncated_response,
                            reply_markup=InlineKeyboardMarkup(
                                [[InlineKeyboardButton("Read More", callback_data=f"read_more:{message.id}")]]
                            ),
                            quote=True
                        )
                    else:
                        await message.reply_text(
                            truncated_response,
                            reply_markup=InlineKeyboardMarkup(
                                [[InlineKeyboardButton("Read More", callback_data=f"read_more:{message.id}")]]
                            ),
                            quote=True
                        )
                else:
                    await message.reply_text(to_feminine_style("Oopsie, I don't have a response for that. Could you please try again, sweetie?"), quote=True)
            except requests.exceptions.RequestException as e:
                pass
        
        # Check if the bot's username is mentioned anywhere in the text
        elif f"@{bot_username}" in message.text:
            await react_with_random_emoji(client, message)
            await app.send_chat_action(message.chat.id, ChatAction.TYPING)

            user_input = message.text.replace(f"@{bot_username}", "").strip()

            try:
                response = api.gemini(user_input)
                x = response.get("results")
                image_url = response.get("image_url")

                if x:
                    x = to_feminine_style(x)
                    x = add_feminine_touch(x)
                    truncated_response = truncate_text(x)
                    full_messages[message.id] = x  # Store the full message

                    if image_url:
                        await message.reply_photo(
                            image_url,
                            caption=truncated_response,
                            reply_markup=InlineKeyboardMarkup(
                                [[InlineKeyboardButton("Read More", callback_data=f"read_more:{message.id}")]]
                            ),
                            quote=True
                        )
                    else:
                        await message.reply_text(
                            truncated_response,
                            reply_markup=InlineKeyboardMarkup(
                                [[InlineKeyboardButton("Read More", callback_data=f"read_more:{message.id}")]]
                            ),
                            quote=True
                        )
                else:
                    await message.reply_text(to_feminine_style("Oopsie, I don't have a response for that. Could you please try again, sweetie?"), quote=True)
            except requests.exceptions.RequestException as e:
                pass
