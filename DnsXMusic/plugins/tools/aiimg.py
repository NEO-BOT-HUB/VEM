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
    
    # Remove the buttons and show 'Image Generating' message
    wait_message = await callback_query.message.edit_text("Iᴍᴀɢᴇ Is Gᴇɴᴇʀᴀᴛɪɴɢ Pʟᴇᴀsᴇ Wᴀɪᴛ......")
    
    # Determine API URL based on button pressed
    if filter_type == "anime":
        api_url = f"https://animeimg.apiitzasuraa.workers.dev/?prompt={prompt}"
        model_name = "Aɴɪᴍᴇ"
    elif filter_type == "3d":
        api_url = f"https://disneyimg.apiitzasuraa.workers.dev/?prompt={prompt}"
        model_name = "𝟹D Rᴇɴᴅᴇʀ"
    elif filter_type == "realcartoon":
        api_url = f"https://magicimg.apiitzasuraa.workers.dev/?prompt={prompt}"
        model_name = "RᴇᴀʟCᴀʀᴛᴏᴏɴ𝟹D"
    else:
        await callback_query.message.reply_text("Invalid option selected.")
        return
    
    try:
        # Send request to the API
        response = requests.get(api_url)
        response.raise_for_status()
        image_url = response.json().get('image')
        
        # Remove 'Generating' message
        await client.delete_messages(chat_id=callback_query.message.chat.id, message_ids=wait_message.message_id)

        if image_url:
            # Format the output message
            model_text = f"𝐌𝐨𝐝𝐞𝐥: {model_name}\n"
            prompt_text = f"𝐏𝐫𝐨𝐦𝐩𝐭: `{prompt}`\n"
            user_text = f"𝐑𝐞𝐪𝐮𝐢𝐫𝐞𝐝 𝐁𝐲: {callback_query.from_user.mention}\n"
            
            caption = f"{model_text}\n{prompt_text}\n{user_text}"
            
            # Send the generated image with the formatted caption
            await client.send_photo(chat_id=callback_query.message.chat.id, photo=image_url, caption=caption, parse_mode="Markdown")
        else:
            await callback_query.message.reply_text("No image found.")
    except Exception as e:
        await callback_query.message.reply_text(f"An error occurred: {e}")

