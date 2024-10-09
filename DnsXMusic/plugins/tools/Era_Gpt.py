import asyncio
import aiohttp
from pyrogram import filters
from DnsXMusic import app
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ChatAction

# API URL template
API_URL = "https://chatwithai.codesearch.workers.dev/chat={message}&model={model}"

# Available models with descriptions
MODELS_INFO = {
    'claude-sonnet-3.5': "🎯 Best for detailed answers & analysis",
    'gemini-pro': "🚀 Fast & efficient for general tasks",
    'gpt-4o': "🧠 Advanced reasoning & complex tasks",
    'blackbox': "⚡ Quick responses for simple queries",
    'gemini-1.5-flash': "💫 Latest Gemini model, very fast",
    'llama-3.1-8b': "📱 Lightweight & efficient",
    'llama-3.1-70b': "💪 Powerful for various tasks",
    'llama-3.1-405b': "🔥 Most powerful Llama model",
    'ImageGenerationLV45LJp': "🎨 Specialized in creative tasks"
}

# User preferences dictionary
user_preferences = {}

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
        
        # If user explicitly specifies model, override preference
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
                    result = await response.text()
                    
                    response_text = f"""
**🤖 AI Response:**
**Using Model:** {model}

{result}"""
                    
                    # Split response if too long
                    try:
                        if len(response_text) > 4096:
                            chunks = [response_text[i:i+4096] for i in range(0, len(response_text), 4096)]
                            for chunk in chunks:
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

@app.on_message(filters.command("aimodels"))
async def select_model(client, message):
    try:
        user_id = message.from_user.id
        
        # Create keyboard with models
        keyboard = []
        row = []
        for i, (model, desc) in enumerate(MODELS_INFO.items()):
            # Create 2 buttons per row
            if i % 2 == 0 and row:
                keyboard.append(row)
                row = []
            row.append(InlineKeyboardButton(
                f"{model.split('-')[0].capitalize()}",
                callback_data=f"select_model_{model}"
            ))
        if row:
            keyboard.append(row)

        text = "**🤖 Select Your Preferred AI Model:**\n\n"
        for model, desc in MODELS_INFO.items():
            text += f"**{model}**\n{desc}\n\n"
        
        await message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_callback_query(filters.regex("^select_model_"))
async def model_selected(client, callback_query):
    try:
        user_id = callback_query.from_user.id
        selected_model = callback_query.data.replace("select_model_", "")
        
        user_preferences[user_id] = selected_model
        
        await callback_query.message.edit_text(
            f"✅ Your preferred model has been set to **{selected_model}**\n\n"
            "You can now use /ask command directly without specifying the model.\n"
            "To change model anytime, use /aimodels again."
        )
    except Exception as e:
        await callback_query.message.edit_text(f"❌ Error: {str(e)}")

@app.on_message(filters.command("aihelp"))
async def help_command(_, message):
    try:
        help_text = """
**🤖 AI Chat Assistant Help**

**Available Commands:**
⊚ /ask <message> - Chat with AI using your preferred model
⊚ /aimodels - Select your preferred AI model
⊚ /aihelp - Show this help message

**Note:** 
- New users will automatically use Claude-3.5 model
- You can change your preferred model anytime using /aimodels
- You can still override your preference by using:
  `/ask <message> --model <model_name>`
"""
        await message.reply_text(help_text)
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
