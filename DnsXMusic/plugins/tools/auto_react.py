
import random
import asyncio
from DnsXMusic import app
from pyrogram import filters  


# Reactions list 
reactions = [
    '👍', '👎', '❤️', '🔥', '🥰', '👏', '😁', '🤔', '🤯', '😱', '🤬', '😢', '🎉', '🤩', '🤮', '💩', '🙏', '👌',
    '🕊', '🤡', '🥱', '🥴', '😍', '🐳', '❤️‍🔥', '🌚', '🌭', '💯', '🤣', '⚡️', '🍌', '🏆', '💔', '🤨', '😐',
    '🍓', '🍾', '💋', '🖕', '😈', '😴', '🤓', '👻', '👨‍💻', '👀', '🎃', '🙈', '😇', '😨', '🤝', '✍️', '🤗',
    '🫡', '🎅', '🎄', '☃️', '💅', '🤪', '🗿', '🆒', '💘', '🙉', '🦄', '😘', '💊', '🙊', '😎', '👾', '🤷‍♂️',
    '🤷‍♀️', '😭', '🤫', '💃', '🕺', '👋', '🐷', '🌹', '💖', '🌈', '🖤', '😡', '😳', '🥳', '🤖', '🦸', '🦹',
    '🧙‍♂️', '🧙‍♀️', '🧝‍♂️', '🧝‍♀️', '🧛‍♂️', '🧛‍♀️', '🧟‍♂️', '🧟‍♀️', '🧞‍♂️', '🧞‍♀️', '🧜‍♂️', '🧜‍♀️',
    '🧚‍♂️', '🧚‍♀️', '🐶', '🐱', '🐭', '🐹', '🐰', '🦊', '🐻', '🐼', '🐻‍❄️', '🐨', '🐯', '🦁', '🐮', '🐷',
    '🐸', '🐵', '🙈', '🙉', '🙊', '🐒', '🐔', '🐧', '🐦', '🐤', '🐣', '🐥', '🦆', '🦅', '🦉', '🦜', '🐓', '🦃',
    '🐬', '🐟', '🐠', '🐡', '🦈', '🐙', '🐚', '🐌', '🐞', '🐜', '🦋', '🐝', '🐧', '🦗', '🕷', '🕸', '🦕', '🦖',
    '🦎', '🐢', '🐍', '🦂', '🦟', '🦠', '🐲', '🐉', '🦜', '🐳', '🐋', '🐬'
]


# Global variable to track reaction status (default off)
is_reaction_on = False  # Make sure this is defined globally

@app.on_message(filters.command(["reaction", "react", "eaction", "eact"], prefixes=["/", "!", ".", "R", "r"]))
async def toggle_reaction(client, message):
    global is_reaction_on
    command_parts = message.text.split()
    if len(command_parts) == 2:
        if command_parts[1].lower() == "on":
            is_reaction_on = True
            await message.reply_text("Reaction spam is now ON! 😈")
        elif command_parts[1].lower() == "off":
            is_reaction_on = False
            await message.reply_text("Reaction spam is now OFF! 😌")
        else:
            await message.reply_text("Invalid command. Use /reaction on or /reaction off")
    else:
        await message.reply_text("Invalid command. Use /reaction on or /reaction off")

@app.on_message()
async def auto_react(client, message):
    global is_reaction_on
    if is_reaction_on:
        reaction = random.choice(reactions)
        try:
            await message.react(reaction)
            await asyncio.sleep(0.1)  # Small delay to avoid overwhelming Telegram
        except Exception as e:
            print(f"An error occurred: {e}")
