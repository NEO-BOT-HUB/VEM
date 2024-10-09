import asyncio
import aiohttp
import json
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

# Initialize user preferences dictionary
user_preferences = {}

@app.on_message(filters.command("ask"))
async def ai_chat(client, message):
   try:
       user_id = message.from_user.id
       
       if len(message.command) < 2:
           await message.reply_text(
               "❌ Please provide a message.\n\nFormat: /ask <your_message>"
           )
           return

       model = user_preferences.get(user_id, 'claude-sonnet-3.5')
       user_message = " ".join(message.command[1:])
       
       if "--model" in user_message:
           try:
               msg_parts = user_message.split("--model")
               user_message = msg_parts[0].strip()
               specified_model = msg_parts[1].strip()
               
               if specified_model in MODELS_INFO:
                   model = specified_model
               else:
                   await message.reply_text("❌ Invalid model specified! Using your preferred model instead.")
           except:
               await message.reply_text("❌ Invalid format, using your preferred model.")

       await message.reply_chat_action(ChatAction.TYPING)

       async with aiohttp.ClientSession() as session:
           api_url = API_URL.format(message=user_message, model=model)
           async with session.get(api_url) as response:
               if response.status == 200:
                   raw_result = await response.text()
                   
                   try:
                       json_response = json.loads(raw_result)
                       result = json_response.get("result", "No response found")
                       
                       response_text = (
                           f"🔮 **Model:** `{model}`\n\n"
                           f"📝 **Answer:**\n{result}"
                       )
                   except json.JSONDecodeError:
                       response_text = (
                           f"🔮 **Model:** `{model}`\n\n"
                           f"📝 **Answer:**\n{raw_result}"
                       )
                   
                   try:
                       if len(response_text) > 4096:
                           chunks = [response_text[i:i+4096] for i in range(0, len(response_text), 4096)]
                           for i, chunk in enumerate(chunks):
                               await message.reply_text(chunk)
                       else:
                           await message.reply_text(response_text)
                   except Exception as e:
                       await message.reply_text(f"❌ Error in sending response: {str(e)}")
               else:
                   await message.reply_text(f"❌ Error: API response status {response.status}")

   except Exception as e:
       await message.reply_text(f"❌ Error occurred: {str(e)}")

@app.on_message(filters.command("aimodels"))
async def select_model(client, message):
    try:
        keyboard = []
        for model, desc in MODELS_INFO.items():
            keyboard.append([
                InlineKeyboardButton(
                    f"{model} | {desc}",
                    callback_data=f"select_model_{model}"
                )
            ])

        text = (
            "**🤖 Available AI Models**\n\n"
            "• Select your preferred AI model from below\n"
            "• Currently using: Claude-3.5 (Default)\n"
            "• Click on any model to set as default\n\n"
            "**Available Models:**"
        )
        
        await message.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")

@app.on_message(filters.command("aihelp"))
async def help_command(_, message):
    try:
        help_text = (
            "**🤖 DNS X AI Help Menu**\n\n"
            "**Available Commands:**\n"
            "• /ask - Chat with AI\n"
            "• /aimodels - Select AI model\n"
            "• /aihelp - Show this help\n\n"
            "**How to Use:**\n"
            "1. Use /aimodels to select your preferred AI model\n"
            "2. Use /ask followed by your question\n"
            "3. Default model is Claude-3.5\n\n"
            "**Example:**\n"
            "`/ask What is artificial intelligence?`\n\n"
            "**Note:** You can change model anytime using /aimodels"
        )
        
        await message.reply_text(help_text)
    except Exception as e:
        await message.reply_text(f"❌ Error: {str(e)}")
