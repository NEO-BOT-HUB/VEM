import asyncio
import aiohttp
import json
from pyrogram import filters
from DnsXMusic import app
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatAction

# Rest of the imports and configurations remain same...

@app.on_message(filters.command("ask"))
async def ai_chat(client, message):
    try:
        user_id = message.from_user.id
        
        # Check if message is provided
        if len(message.command) < 2:
            await message.reply_text(
                "❌ Please provide a message.\n\nFormat: /ask <your_message>"
            )
            return

        # Get user's preferred model or set default
        model = user_preferences.get(user_id, 'claude-sonnet-3.5')
        
        # Extract message
        user_message = " ".join(message.command[1:])
        
        # Handle model override
        if "--model" in user_message:
            try:
                msg_parts = user_message.split("--model")
                user_message = msg_parts[0].strip()
                specified_model = msg_parts[1].strip()
                
                if specified_model in MODELS_INFO:
                    model = specified_model
                else:
                    await message.reply_text(
                        "❌ Invalid model specified! Using your preferred model instead."
                    )
            except:
                await message.reply_text("❌ Invalid format, using your preferred model.")

        # Show typing action
        await message.reply_chat_action(ChatAction.TYPING)

        # Make API request
        async with aiohttp.ClientSession() as session:
            api_url = API_URL.format(message=user_message, model=model)
            async with session.get(api_url) as response:
                if response.status == 200:
                    raw_result = await response.text()
                    
                    try:
                        # Parse JSON response
                        json_response = json.loads(raw_result)
                        result = json_response.get("result", "No response found")
                        
                        # Format the response with a nice UI
                        response_text = f"""
╔══════ ≪ °❈° ≫ ══════╗
  🤖 **AI RESPONSE**
╚══════ ≪ °❈° ≫ ══════╝

👤 **Question:**
{user_message}

🔮 **Model:** `{model}`

📝 **Answer:**
{result}

═══════════════════
**𝗗𝗡𝗦 𝗫 𝗔𝗜**"""
                    except json.JSONDecodeError:
                        # If not JSON, use raw response
                        response_text = f"""
╔══════ ≪ °❈° ≫ ══════╗
  🤖 **AI RESPONSE**
╚══════ ≪ °❈° ≫ ══════╝

👤 **Question:**
{user_message}

🔮 **Model:** `{model}`

📝 **Answer:**
{raw_result}

═══════════════════
**𝗗𝗡𝗦 𝗫 𝗔𝗜**"""
                    
                    # Split response if too long
                    try:
                        if len(response_text) > 4096:
                            # First chunk with header
                            first_chunk = response_text[:4000] + "\n\n... (continued)"
                            await message.reply_text(first_chunk)
                            
                            # Remaining text without header
                            remaining_text = response_text[4000:]
                            while remaining_text:
                                chunk = remaining_text[:4000]
                                remaining_text = remaining_text[4000:]
                                if remaining_text:
                                    chunk += "\n\n... (continued)"
                                await message.reply_text(chunk)
                        else:
                            await message.reply_text(response_text)
                    except Exception as e:
                        await message.reply_text(f"❌ Error in sending response: {str(e)}")
                else:
                    await message.reply_text(
                        f"❌ Error: API response status {response.status}"
                    )

    except Exception as e:
        await message.reply_text(f"❌ Error occurred: {str(e)}")

# Rest of the code remains same...
