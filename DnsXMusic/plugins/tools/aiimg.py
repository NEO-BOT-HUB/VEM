import requests
from DnsXMusic import app  
from pyrogram import filters  
from pyrogram.types import InputMediaPhoto  

# Command to generate an AI image (available in private, groups, and channels)
@app.on_message(filters.command(["make"], prefixes=["/", "!", ".", "M", "m"]) & filters.incoming)
async def generate_ai_image(client, message):
    try:
        # Extract the prompt from the message
        prompt = message.text[len('/make '):].strip()

        if not prompt:
            await message.reply_text("Please provide a prompt after /make.")
            return

        # Send request to the AI image generation API
        api_url = f'https://animeimg.apiitzasuraa.workers.dev/?prompt={prompt}'
        response = requests.get(api_url)

        # Check if the response is OK
        if response.status_code == 200:
            # Save the image temporarily
            image_file = 'generated_image.png'
            with open(image_file, 'wb') as file:
                file.write(response.content)

            # Send the image to the user as a photo
            await client.send_photo(
                chat_id=message.chat.id,
                photo=image_file,
                caption=f"Here is your image for prompt: {prompt}"
            )
        else:
            await message.reply_text("Sorry, I couldn't generate the image. Try again later.")

    except Exception as e:
        # Log the error and notify the user
        await message.reply_text("An error occurred while processing your request.")
        print(f"Error: {e}")
