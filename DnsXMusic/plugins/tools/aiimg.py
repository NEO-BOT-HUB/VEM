
import requests
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto, InputMedia
from io import BytesIO
from DnsXMusic import app
import aiohttp  # Updated to async HTTP requests

# Function to generate buttons for model selection
def generate_buttons(prompt):
    buttons = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Aɴɪᴍᴇ", callback_data=f"anime:{prompt}"),
                InlineKeyboardButton("𝟹D Rᴇɴᴅᴇʀ", callback_data=f"3d:{prompt}")
            ],
            [
                InlineKeyboardButton("RᴇᴀʟCᴀʀᴛᴏᴏɴ𝟹D", callback_data=f"realcartoon:{prompt}"),
                InlineKeyboardButton("Dɪsɴᴇʏ", callback_data=f"disney:{prompt}")
            ]
        ]
    )
    return buttons

# Async function to get one image from the API
async def get_image(api_url):
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            response.raise_for_status()
            image_url = (await response.json()).get('image')
            if image_url:
                async with session.get(image_url) as img_response:
                    img = BytesIO(await img_response.read())
                    return img
    return None

# Function to create "🔄️ Rᴇɢᴇɴᴇʀᴀᴛᴇ 🔄️" button
def regenerate_button(model, prompt):
    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔄️ Rᴇɢᴇɴᴇʀᴀᴛᴇ 🔄️", callback_data=f"regenerate:{model}:{prompt}")]]
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
        api_url = f"https://realism-img.apiitzasuraa.workers.dev/?prompt={prompt}"  # Updated API
        model_name = "RᴇᴀʟCᴀʀᴛᴏᴏɴ𝟹D"
    elif filter_type == "disney":
        api_url = f"https://disney.apiitzasuraa.workers.dev/?prompt={prompt}"
        model_name = "Dɪsɴᴇʏ"
    else:
        await callback_query.message.reply_text("Invalid option selected.")
        return

    try:
        # Get only 1 image from the API
        image = await get_image(api_url)  # Updated for async and single image

        # Remove the 'Generating' message
        await client.delete_messages(chat_id=callback_query.message.chat.id, message_ids=wait_message.id)

        if image:
            # Create a caption
            model_text = f"𝐌𝐨𝐝𝐞𝐥: {model_name}\n"
            prompt_text = f"𝐏𝐫𝐨𝐦𝐩𝐭: `{prompt}`\n"
            user_text = f"𝐑𝐞𝐪𝐮𝐢𝐫𝐞𝐝 𝐁𝐲: {callback_query.from_user.mention}\n"
            caption = f"{model_text}{prompt_text}{user_text}"

            # Add regenerate button
            regenerate_markup = regenerate_button(filter_type, prompt)

            # Send the image with the caption and button
            await client.send_photo(
                chat_id=callback_query.message.chat.id,
                photo=image,  # Send the single image
                caption=caption,  # Add the caption
                reply_markup=regenerate_markup  # Add the regenerate button below the image
            )
        else:
            await callback_query.message.reply_text("No image found.")
    except Exception as e:
        await callback_query.message.reply_text(f"An error occurred: {e}")