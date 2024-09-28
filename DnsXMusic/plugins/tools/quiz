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

# Start/Stop Quiz command with multiple prefixes
@app.on_message(filters.command(["quiz"], prefixes=["/", "!", ".", "Q", "q"]))
async def quiz(client, message):
    global is_quiz_on, active_poll_message

    user_id = message.from_user.id

    # Start the quiz if "on" is passed
    if len(message.command) > 1 and message.command[1].lower() == "on":
        if is_quiz_on:
            await message.reply_text("Quiz is already running!")
            return

        is_quiz_on = True
        await message.reply_text("Quiz started! Type /quiz off to stop.")

        # Polling loop with 10-minute intervals
        categories = [9, 17, 18, 20, 21, 27]
        while is_quiz_on:
            await app.send_chat_action(message.chat.id, ChatAction.TYPING)

            # Fetching quiz question
            url = f"https://opentdb.com/api.php?amount=1&category={random.choice(categories)}&type=multiple"
            response = requests.get(url).json()

            question_data = response["results"][0]
            question = question_data["question"]
            correct_answer = question_data["correct_answer"]
            incorrect_answers = question_data["incorrect_answers"]

            all_answers = incorrect_answers + [correct_answer]
            random.shuffle(all_answers)

            correct_option_id = all_answers.index(correct_answer)

            # Send quiz poll
            active_poll_message = await app.send_poll(
                chat_id=message.chat.id,
                question=question,
                options=all_answers,
                is_anonymous=False,
                type=PollType.QUIZ,
                correct_option_id=correct_option_id,
            )

            # Wait for 10 minutes before the next poll
            await asyncio.sleep(600)

            # Delete the poll if still active and quiz is on
            if is_quiz_on:
                await app.delete_messages(message.chat.id, active_poll_message.message_id)

    # Stop the quiz if "off" is passed
    elif len(message.command) > 1 and message.command[1].lower() == "off":
        if not is_quiz_on:
            await message.reply_text("Quiz is not running!")
            return

        is_quiz_on = False
        await message.reply_text("Quiz stopped.")

# /new command for generating a new quiz immediately
@app.on_message(filters.command(["new"], prefixes=["/", "!", ".", "N", "n"]))
async def new_quiz(client, message):
    global active_poll_message
    if active_poll_message:
        await app.delete_messages(message.chat.id, active_poll_message.message_id)
        await quiz(client, message)

# Ranks command with multiple variations and buttons for "Today", "Week", "Overall"
@app.on_message(filters.command(["quizranks"], prefixes=["/", "!", ".", "Q", "q"]))
async def quiz_ranks(client, message):
    buttons = [
        [
            InlineKeyboardButton("Tᴏᴅᴀʏ", callback_data="today"),
            InlineKeyboardButton("Wᴇᴇᴋ", callback_data="week"),
            InlineKeyboardButton("Oᴠᴇʀᴀʟʟ", callback_data="overall")
        ]
    ]
    await message.reply_text("Select the time period to view ranks:", reply_markup=InlineKeyboardMarkup(buttons))

# Callback for handling the rank buttons
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

    # Filter and sort the quiz scores
    filtered_scores = {user: score for user, (timestamp, score) in quiz_scores.items() if not start_time or timestamp >= start_time}
    sorted_scores = sorted(filtered_scores.items(), key=lambda x: x[1], reverse=True)

    if sorted_scores:
        rank_list = "\n".join([f"{i+1}. {user}: {score} points" for i, (user, score) in enumerate(sorted_scores)])
    else:
        rank_list = "No quizzes solved in this period."

    await callback_query.message.edit_text(f"{text}\n\n{rank_list}")

# Handle poll answers to update scores
@app.on_message(filters.text)
async def handle_poll_answer(client, message):
    if message.poll_answer:
        user_id = message.poll_answer.user.id
        user_answer_id = message.poll_answer.option_ids[0]

        correct_answer_id = active_poll_message.poll.correct_option_id

        if user_answer_id == correct_answer_id:
            now = datetime.now()
            if user_id in quiz_scores:
                _, current_score = quiz_scores[user_id]
                quiz_scores[user_id] = (now, current_score + 1)
            else:
                quiz_scores[user_id] = (now, 1)

            await message.reply_text(f"You answered correctly! Your current score is: {quiz_scores[user_id][1]}")

if __name__ == "__main__":
    app.run()
