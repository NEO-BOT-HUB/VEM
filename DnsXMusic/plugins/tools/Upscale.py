import requests
from io import BytesIO
from pyrogram import filters
from DnsXMusic import app

def upscale_image_api(image_data):
    files = {
        'image': image_data
    }
    
    # Send the image to the UP_API for upscaling
    response = requests.post(UP_API, files=files)
    
    if response.status_code == 200:
        return response.content  # Upscaled image in bytes
    else:
        return None

@app.on_message(filters.command(["upscale", "pscale", "p"], prefixes=["/", "!", ".", "U", "u"]) & filters.reply)
async def upscale_command(client, message):
    # Ensure the message is a reply to an image
    if message.reply_to_message and message.reply_to_message.photo:
        try:
            # Get the largest photo object directly
            photo = message.reply_to_message.photo
            
            # Download the photo
            file = await client.download_media(photo.file_id)

            # Send the image to the UP_API for upscaling
            upscaled_image = upscale_image_api(BytesIO(file))

            if upscaled_image:
                # Send the upscaled image back to the user
                await message.reply_photo(photo=BytesIO(upscaled_image), caption="Here's your upscaled image!")
            else:
                await message.reply_text("Sorry, the image could not be upscaled.")
        except Exception as e:
            await message.reply_text(f"Error: {e}")
    else:
        await message.reply_text("Please reply to an image with the /upscale command to use this feature.")
