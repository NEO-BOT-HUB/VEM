import cv2
import numpy as np
from DnsXMusic import app
from pyrogram import filters
import io

# Simple bilinear or bicubic upscale using OpenCV
def upscale_image(image_data, scale_factor=4):
    img = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
    # Bilinear upscale
    upscaled_img = cv2.resize(img, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
    success, encoded_img = cv2.imencode('.jpg', upscaled_img)
    return encoded_img.tobytes() if success else None

@app.on_message(filters.command(["upscale", "pscale", "p"], prefixes=["/", "!", ".", "U", "u"]) & filters.reply)
async def upscale_command(client, message):
    # Check if the command is a reply to an image
    if message.reply_to_message and message.reply_to_message.photo:
        # Get the image file ID from the replied message
        photo = message.reply_to_message.photo  # This is already a list of photos
        if photo:  # Check if the photo list is not empty
            largest_photo = photo[-1]  # Get the largest available resolution
            file = await client.download_media(largest_photo.file_id)

            # Send the image to be upscaled
            upscaled_image = upscale_image(file)
            if upscaled_image:
                await message.reply_photo(photo=io.BytesIO(upscaled_image), caption="Here's your upscaled image!")
            else:
                await message.reply_text("Sorry, I couldn't upscale the image.")
        else:
            await message.reply_text("No photo found to upscale.")
    else:
        await message.reply_text("Please reply to an image with the /upscale command to use this feature.")
