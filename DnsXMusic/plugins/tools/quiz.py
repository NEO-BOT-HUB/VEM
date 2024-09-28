import random
import requests
import time
import asyncio
from datetime import datetime, timedelta
from pyrogram import filters
from pyrogram.enums import PollType, ChatAction
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from DnsXMusic import app

# Global variables to manage quiz state and scores
is_quiz_on = False
active_poll_message = None
quiz_scores = {}
last_command_time = {}

@app.on_message(filters.command(["quiz", "uiz"], prefixes=["/", "!", ".", "Q", "q"]))
async def quiz(client, message):
    global is_quiz_on, active_poll_message
    user_id = message.from_user.id
    current_time = time.time()

    if user_id in last_command_time and current_time - last_command_time[user_id] < 5:
        await message.reply_text(
            "Pʟᴇᴀsᴇ ᴡᴀɪᴛ 𝟻 sᴇᴄᴏɴᴅs ʙᴇғᴏʀᴇ ᴜsɪɴɢ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴀɢᴀɪɴ."
        )
        return

    last_command_time[user_id] = current_time

    if message.command[1] == "on":
        is_quiz_on = True
        await message.reply_text("Quiz started! Type /quiz off to stop.")
        categories = [9, 17, 18, 20, 21, 27]
        while is_quiz_on:
            await app.send_chat_action(message.chat.id, ChatAction.TYPING)
            url = f"https://opentdb.com/api.php?amount=1&category={random.choice(categories)}&type=multiple"
            response = requests.get(url).json()

            question_data = response["results"][0]
            question = question_data["question"]
            correct_answer = question_data["correct_answer"]
            incorrect_answers = question_data["incorrect_answers"]

            all_answers = incorrect_answers + [correct_answer]
            random.shuffle(all_answers)

            cid = all_answers.index(correct_answer)
            active_poll_message = await app.send_poll(
                chat_id=message.chat.id,
                question=question,
                options=all_answers,
                is_anonymous=False,
                type=PollType.QUIZ,
                correct_option_id=cid,
            )

            # Wait for 10 minutes (600 seconds)
            await asyncio.sleep(600)

            # Delete the old poll and start a new one if quiz is still on
            if is_quiz_on:
                await app.delete_messages(message.chat.id, active_poll_message.message_id)
    
    elif message.command[1] == "off":
        is_quiz_on = False
        await message.reply_text("Quiz stopped!")

@app.on_message(filters.command(["new", "ew", "newquiz", "ewquiz"], prefixes=["/", "!", ".", "N", "n"]))
async def new_quiz(client, message):
    global active_poll_message
    if active_poll_message:
        await app.delete_messages(message.chat.id, active_poll_message.message_id)
        await quiz(client, message)

@app.on_message(filters.command(["quizranks", "uziranks", "ranks"], prefixes=["/", "!", ".", "Q", "q"]))
async def quiz_ranks(client, message):
    buttons = [
        [
            InlineKeyboardButton("Tᴏᴅᴀʏ", callback_data="today"),
            InlineKeyboardButton("Wᴇᴇᴋ", callback_data="week"),
            InlineKeyboardButton("Oᴠᴇʀᴀʟʟ", callback_data="overall")
        ]
    ]
    await message.reply_text("Select the time period to view ranks:", reply_markup=InlineKeyboardMarkup(buttons))

@app.on_callback_query(filters.regex(r"(today|week|overall)"))
async def show_ranks(client, callback_query):
    period = callback_query.data
    now = datetime.now()

    if period == "today":
        start_time = now - timedelta(days=1)
        text = "Today's Quiz Ranks:"
    elif period == "week":
        start_time = now - timedelta(days=7)
        text = "This Week's Quiz Ranks:"
    else:
        start_time = None
        text = "Overall Quiz Ranks:"

    # Filter scores based on the time period
    filtered_scores = {user: score for user, (timestamp, score) in quiz_scores.items() if not start_time or timestamp >= start_time}
    
    # Sort and display ranks
    sorted_scores = sorted(filtered_scores.items(), key=lambda x: x[1], reverse=True)
    
    if sorted_scores:
        rank_list = "\n".join([f"{i+1}. {user}: {score} points" for i, (user, score) in enumerate(sorted_scores)])
    else:
        rank_list = "No quizzes solved in this period."

    await callback_query.message.edit_text(f"{text}\n\n{rank_list}")

# Update quiz_scores when a quiz is solved
@app.on_poll_answer()
async def handle_poll_answer(client, poll_answer):
    user_id = poll_answer.user.id
    now = datetime.now()

    if user_id in quiz_scores:
        _, current_score = quiz_scores[user_id]
        quiz_scores[user_id] = (now, current_score + 1)
    else:
        quiz_scores[user_id] = (now, 1)

