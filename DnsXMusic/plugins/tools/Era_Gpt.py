import asyncio
import aiohttp
from pyrogram import filters
from DnsXMusic import app

# API URL template
API_URL = "https://chatwithai.codesearch.workers.dev/chat={message}&model={model}"

# Available models list
AVAILABLE_MODELS = [
    'blackbox',
    'gemini-1.5-flash',
    'llama-3.1-8b',
    'llama-3.1-70b', 
    'llama-3.1-405b',
    'ImageGenerationLV45LJp',
    'gpt-4o',
    'gemini-pro',
    'claude-sonnet-3.5'
]

# Help message
HELP_MESSAGE = f"""
**🤖 AI Chat Commands:**

⊚ Format: /ask <message> --model <model_name>
⊚ Example: /ask Hello! --model gemini-pro

**📝 Available Models:**
{chr(10).join(f"⊚ {model}" for model in AVAILABLE_MODELS)}

**Default model:** blackbox
"""

@app.on_message(filters.command("aihelp"))
async def help_command(_, message):
    await message.reply_text(HELP_MESSAGE)

@app.on_message(filters.command("ask"))
async def ai_chat(client, message):
    try:
        # Get the message text
        if len(message.command) < 2:
            await message.reply_text(
                "❌ Please provide a message.\n\nFormat: /ask <message> --model <model_name>"
            )
            return

        # Extract message and model
        full_message = " ".join(message.command[1:])
        model = "blackbox"  # Default model
        
        if "--model" in full_message:
            try:
                msg_parts = full_message.split("--model")
                user_message = msg_parts[0].strip()
                model = msg_parts[1].strip()
                
                if model not in AVAILABLE_MODELS:
                    await message.reply_text(
                        f"❌ Invalid model!\n\n**Available models:**\n" + 
                        "\n".join(f"⊚ {m}" for m in AVAILABLE_MODELS)
                    )
                    return
            except:
                await message.reply_text("❌ Invalid format for model specification")
                return
        else:
            user_message = full_message

        # Send "typing" action
        async with client.action(message.chat.id, "typing"):
            # Make API request
            async with aiohttp.ClientSession() as session:
                api_url = API_URL.format(message=user_message, model=model)
                async with session.get(api_url) as response:
                    if response.status == 200:
                        result = await response.text()
                        
                        # Format the response
                        response_text = f"""
**🤖 AI Response:**
**Model:** {model}

{result}
"""
                        # Split response into chunks if too long
                        if len(response_text) > 4096:
                            chunks = [response_text[i:i+4096] for i in range(0, len(response_text), 4096)]
                            for chunk in chunks:
                                await message.reply_text(chunk)
                        else:
                            await message.reply_text(response_text)
                    else:
                        await message.reply_text(
                            f"❌ Error: API response status {response.status}"
                        )

    except Exception as e:
        await message.reply_text(f"❌ Error occurred: {str(e)}")

# Optional: Add command to list available models
@app.on_message(filters.command("aimodels"))
async def list_models(_, message):
    models_text = "**📝 Available AI Models:**\n\n" + "\n".join(f"⊚ {model}" for model in AVAILABLE_MODELS)
    await message.reply_text(models_text)

# Error handler
@app.on_message(filters.command("ask") & filters.regex(r'/ask$'))
async def empty_ask(_, message):
    await message.reply_text(
        "❌ Please provide a message with the /ask command.\n\n"
        "Format: /ask <your_message> --model <model_name>\n"
        "Example: /ask Hello! --model gemini-pro"
    )
