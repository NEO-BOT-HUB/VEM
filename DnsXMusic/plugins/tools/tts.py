from DnsXMusic import app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import pyttsx3
import os
import hashlib
import json
from datetime import datetime

engine = pyttsx3.init()

# Cache for storing generated audio files
audio_cache = {}

# Stats for tracking usage
usage_stats = {
    "total_requests": 0,
    "language_usage": {},
    "voice_usage": {}
}

# Load stats from file if it exists
if os.path.exists("tts_stats.json"):
    with open("tts_stats.json", "r") as f:
        usage_stats = json.load(f)

# Get available voices and languages
available_voices = engine.getProperty('voices')
available_languages = list(set(voice.languages[0] for voice in available_voices if voice.languages))

@app.on_message(filters.command(["tts", "ts"], prefixes=["/", "!", ".", "T", "t"]))
async def tts(client, message):
    if len(message.command) > 1:
        # If text is provided with the command
        text = ' '.join(message.command[1:])
        await process_tts(message, text=text)
    elif message.reply_to_message and message.reply_to_message.text:
        # If replying to a message
        await process_tts(message, text=message.reply_to_message.text)
    else:
        # If no text is provided, show voice options
        keyboard = []
        for lang in available_languages:
            keyboard.append([
                InlineKeyboardButton(f"Default ({lang})", callback_data=f"tts_default_{lang}"),
                InlineKeyboardButton(f"Male ({lang})", callback_data=f"tts_male_{lang}")
            ])
            keyboard.append([
                InlineKeyboardButton(f"Female ({lang})", callback_data=f"tts_female_{lang}"),
                InlineKeyboardButton(f"Child ({lang})", callback_data=f"tts_child_{lang}")
            ])
        markup = InlineKeyboardMarkup(keyboard)
        await message.reply_text("Choose a voice option and language, or provide text after the command:", reply_markup=markup)

@app.on_callback_query(filters.regex("^tts_"))
async def tts_callback(client, callback_query):
    voice_option, lang = callback_query.data.split("_")[1:]
    await process_tts(callback_query.message, voice_option=voice_option, lang=lang)
    await callback_query.answer()

async def process_tts(message, voice_option="default", lang="en-us", text=None):
    global usage_stats
    
    if not text:
        await message.reply_text("Please provide text or reply to a message.")
        return

    # Update usage stats
    usage_stats["total_requests"] += 1
    usage_stats["language_usage"][lang] = usage_stats["language_usage"].get(lang, 0) + 1
    usage_stats["voice_usage"][voice_option] = usage_stats["voice_usage"].get(voice_option, 0) + 1

    # Save stats to file
    with open("tts_stats.json", "w") as f:
        json.dump(usage_stats, f)

    # Generate a unique hash for this text and voice combination
    text_hash = hashlib.md5((text + voice_option + lang).encode()).hexdigest()

    if text_hash in audio_cache:
        audio_file = audio_cache[text_hash]
    else:
        # Find appropriate voice
        target_voice = None
        for voice in available_voices:
            if voice.languages and voice.languages[0] == lang:
                if voice_option == "male" and voice.gender == 'male':
                    target_voice = voice
                    break
                elif voice_option == "female" and voice.gender == 'female':
                    target_voice = voice
                    break
                elif voice_option == "default":
                    target_voice = voice
                    break
        
        if not target_voice:
            target_voice = available_voices[0]  # Fallback to first available voice

        engine.setProperty('voice', target_voice.id)

        if voice_option == "child":
            engine.setProperty('rate', 150)
        else:
            engine.setProperty('rate', 130)

        audio_file = f"output_{text_hash}.mp3"
        engine.save_to_file(text, audio_file)
        engine.runAndWait()

        # Apply audio effect (example: increase volume by 1.5x)
        os.system(f"ffmpeg -i {audio_file} -filter:a 'volume=1.5' {audio_file}_enhanced.mp3")
        os.remove(audio_file)
        os.rename(f"{audio_file}_enhanced.mp3", audio_file)

        audio_cache[text_hash] = audio_file

    try:
        await message.reply_voice(audio_file)
    except Exception as e:
        await message.reply_text(f"Error sending voice message: {str(e)}")

    # Clean up old cache files
    current_time = datetime.now()
    for file in os.listdir():
        if file.startswith("output_") and file.endswith(".mp3"):
            file_creation_time = datetime.fromtimestamp(os.path.getctime(file))
            if (current_time - file_creation_time).days > 1:  # Delete files older than 1 day
                os.remove(file)
                if file in audio_cache.values():
                    del audio_cache[list(audio_cache.keys())[list(audio_cache.values()).index(file)]]

@app.on_message(filters.command(["ttsstats", "tss"], prefixes=["/", "!", ".", "T", "t"]))
async def tts_stats(client, message):
    stats_message = f"Total TTS requests: {usage_stats['total_requests']}\n\n"
    stats_message += "Language usage:\n"
    for lang, count in usage_stats['language_usage'].items():
        stats_message += f"{lang}: {count}\n"
    stats_message += "\nVoice usage:\n"
    for voice, count in usage_stats['voice_usage'].items():
        stats_message += f"{voice}: {count}\n"
    
    await message.reply_text(stats_message)
