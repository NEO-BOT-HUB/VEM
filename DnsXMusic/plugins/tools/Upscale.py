from io import BytesIO
from pyrogram import filters
from DnsXMusic import app
import cv2
import numpy as np

# Upscale image using OpenCV
def upscale_image(image_data, scale_factor=4):
    img = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
    upscaled_img = cv2.resize(img, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_CUBIC)
    success, encoded_img = cv2.imencode('.jpg', upscaled_img)
    return encoded_img.tobytes() if success else None

@app.on_message(filters.command(["upscale", "pscale", "p"], prefixes=["/", "!", ".", "U", "u"]) & filters.reply)
async def upscale_command(client, message):
    # Ensure the command is a reply to an image
    if message.reply_to_message and message.reply_to_message.photo:
        # Get the largest available image
        photo = message.reply_to_message.photo[-1]
        
        # Download the image
        file = await client.download_media(photo.file_id)

        # Upscale the image
        upscaled_image = upscale_image(file)
        
        if upscaled_image:
            # Send the upscaled image back to the user
            await message.reply_photo(photo=BytesIO(upscaled_image), caption="Here's your upscaled image!")
        else:
            await message.reply_text("Sorry, I couldn't upscale the image.")
    else:
        await message.reply_text("Please reply to an image with the /upscale command to use this feature.")
