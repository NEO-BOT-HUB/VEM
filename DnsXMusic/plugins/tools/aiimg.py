import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from DnsXMusic import app

# Function to create buttons
def generate_buttons(prompt):
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Aɴɪᴍᴇ", callback_data=f"anime:{prompt}")],
            [InlineKeyboardButton("𝟹D Rᴇɴᴅᴇʀ", callback_data=f"3d:{prompt}")],
            [InlineKeyboardButton("RᴇᴀʟCᴀʀᴛᴏᴏɴ𝟹D", callback_data=f"realcartoon:{prompt}")]
        ]
    )
    return buttons

@app.on_message(filters.command(["make", "ake"], prefixes=["/", "!", ".", "M", "m"]))
async def handle_image_generation(client, message):
    prompt = ' '.join(message.command[1:])
    if not prompt:
        await message.reply_text('ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴘʀᴏᴍᴘᴛ.')
        return
    buttons = generate_buttons(prompt)
    await message.reply_text("Please select an image style:", reply_markup=buttons)

# Handle callback queries when a button is pressed
@app.on_callback_query()
async def callback_query_handler(client, callback_query):
    data = callback_query.data
    filter_type, prompt = data.split(":")
    
    # Determine API URL based on button pressed
    if filter_type == "anime":
        api_url = f"https://animeimg.apiitzasuraa.workers.dev/?prompt={prompt}"
    elif filter_type == "3d":
        api_url = f"https://disneyimg.apiitzasuraa.workers.dev/?prompt={prompt}"
    elif filter_type == "realcartoon":
        api_url = f"https://magicimg.apiitzasuraa.workers.dev/?prompt={prompt}"
    else:
        await callback_query.message.reply_text("Invalid option selected.")
        return
    
    try:
        # Send request to the API
        response = requests.get(api_url)
        response.raise_for_status()
        image_url = response.json().get('image')
        
        if image_url:
            await client.send_photo(chat_id=callback_query.message.chat.id, photo=image_url, caption=f"Generated {filter_type}-style image for: {prompt}")
        else:
            await callback_query.message.reply_text("No image found.")
    except Exception as e:
        await callback_query.message.reply_text(f"An error occurred: {e}")

