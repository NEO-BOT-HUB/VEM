import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from DnsXMusic import app

# Function to create buttons for model selection
def generate_buttons(prompt):
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Aɴɪᴍᴇ", callback_data=f"anime:{prompt}")],
            [InlineKeyboardButton("𝟹D Rᴇɴᴅᴇʀ", callback_data=f"3d:{prompt}")],
            [InlineKeyboardButton("RᴇᴀʟCᴀʀᴛᴏᴏɴ𝟹D", callback_data=f"realcartoon:{prompt}")]
        ]
    )
    return buttons

# Function to generate 4 images
def get_images(api_url, count=4):
    images = []
    for _ in range(count):
        response = requests.get(api_url)
        response.raise_for_status()
        image_url = response.json().get('image')
        if image_url:
            images.append(image_url)
    return images

# Function to create "Regenerate" button
def regenerate_button(model, prompt):
    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔄️ Regenerate", callback_data=f"regenerate:{model}:{prompt}")]]
    )
    return buttons

# Command handler for image generation
@app.on_message(filters.command(["make", "ake"], prefixes=["/", "!", ".", "M", "m"]))
async def handle_image_generation(client, message):
    prompt = ' '.join(message.command[1:])
    if not prompt:
        await message.reply_text('ᴘʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴘʀᴏᴍᴘᴛ.')
        return
    buttons = generate_buttons(prompt)
    await message.reply_text("Please select an image style:", reply_markup=buttons)

# Callback handler for button presses
@app.on_callback_query()
async def callback_query_handler(client, callback_query):
    data = callback_query.data
    parts = data.split(":")
    
    if len(parts) == 2:  # For the first image generation buttons
        filter_type, prompt = parts
    elif len(parts) == 3:  # For the regenerate button
        _, filter_type, prompt = parts
    
    # Display a waiting message
    wait_message = await callback_query.message.edit_text("Iᴍᴀɢᴇ Is Gᴇɴᴇʀᴀᴛɪɴɢ Pʟᴇᴀsᴇ Wᴀɪᴛ......")
    
    # Determine the API URL based on the model selected
    if filter_type == "anime":
        api_url = f"https://animeimg.apiitzasuraa.workers.dev/?prompt={prompt}"
        model_name = "Aɴɪᴍᴇ"
    elif filter_type == "3d":
        api_url = f"https://3d-image.apiitzasuraa.workers.dev/?prompt={prompt}"
        model_name = "𝟹D Rᴇɴᴅᴇʀ"
    elif filter_type == "realcartoon":
        api_url = f"https://magicimg.apiitzasuraa.workers.dev/?prompt={prompt}"
        model_name = "RᴇᴀʟCᴀʀᴛᴏᴏɴ𝟹D"
    else:
        await callback_query.message.reply_text("Invalid option selected.")
        return
    
    try:
        # Get 4 images from the selected API
        images = get_images(api_url, count=4)
        
        # Remove the 'Generating' message
        await client.delete_messages(chat_id=callback_query.message.chat.id, message_ids=wait_message.id)

        if images:
            # Send 4 images
            for image_url in images:
                await client.send_photo(chat_id=callback_query.message.chat.id, photo=image_url)

            # Add regenerate button
            regenerate_markup = regenerate_button(filter_type, prompt)
            
            # Send regenerate button with formatted details
            model_text = f"𝐌𝐨𝐝𝐞𝐥: {model_name}\n"
            prompt_text = f"𝐏𝐫𝐨𝐦𝐩𝐭: `{prompt}`\n"
            user_text = f"𝐑𝐞𝐪𝐮𝐢𝐫𝐞𝐝 𝐁𝐲: {callback_query.from_user.mention}\n"
            
            caption = f"{model_text}{prompt_text}{user_text}"
            
            # Send the caption and button
            await callback_query.message.reply_text(caption, reply_markup=regenerate_markup)
        else:
            await callback_query.message.reply_text("No image found.")
    except Exception as e:
        await callback_query.message.reply_text(f"An error occurred: {e}")

