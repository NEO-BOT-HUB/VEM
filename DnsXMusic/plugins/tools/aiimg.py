import requests
from DnsXMusic import app  
from pyrogram import filters  
from pyrogram.types import InputMediaPhoto  

# Command to generate an AI image (available in private, groups, and channels)
@app.on_message(filters.command(["make", "ake"], prefixes=["/", "!", ".", "M", "m"]) & filters.incoming)
async def generate_ai_image(client, message):
    try:
        # Extract the prompt from the message
        prompt = message.text.split(maxsplit=1)[1].strip() if len(message.text.split()) > 1 else None

        if not prompt:
            await message.reply_text("Please provide a prompt after the command.")
            return

        # Log the prompt
        print(f"Received prompt: {prompt}")

        # Send request to the AI image generation API
        api_url = f'https://animeimg.apiitzasuraa.workers.dev/?prompt={prompt}'
        response = requests.get(api_url)

        # Log API response status
        print(f"API response status code: {response.status_code}")

        # Check if the response is OK
        if response.status_code == 200:
            # Save the image temporarily
            image_file = 'generated_image.png'
            with open(image_file, 'wb') as file:
                file.write(response.content)

            # Log successful image generation
            print(f"Image saved as {image_file}")

            # Send the image to the user as a photo
            await client.send_photo(
                chat_id=message.chat.id,
                photo=image_file,
                caption=f"Here is your image for prompt: {prompt}"
            )
        else:
            # Log the error response content
            print(f"API error response: {response.text}")
            await message.reply_text("Sorry, I couldn't generate the image. Try again later.")

    except Exception as e:
        # Log the exception details
        await message.reply_text("An error occurred while processing your request.")
        print(f"Error: {e}")
