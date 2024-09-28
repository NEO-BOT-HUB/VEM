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

# Log function for debugging
async def log_message(message):
    print(f"[DEBUG] {message}")

# Start/Stop Quiz command with multiple prefixes and command variations
@app.on_message(filters.command(["quiz", "uiz"], prefixes=["/", "!", ".", "Q", "q"]))
async def quiz(client, message):
    global is_quiz_on, active_poll_message
    await log_message("Quiz command received.")

    user_id = message.from_user.id
    current_time = time.time()

    # Prevent spamming of /quiz command
    if user_id in last_command_time and current_time - last_command_time[user_id] < 5:
        await message.reply_text("Please wait 5 seconds before using this command again.")
        return

    last_command_time[user_id] = current_time

    # Start the quiz if "on" is passed
    if len(message.command) > 1 and message.command[1].lower() == "on":
        await log_message("/quiz on command received.")
        if is_quiz_on:
            await message.reply_text("Quiz is already running!")
            return

        is_quiz_on = True
        await message.reply_text("Quiz started! Type /quiz off to stop.")

        # Polling loop with 10-minute intervals
        categories = [9, 17, 18, 20, 21, 27]
        while is_quiz_on:
            await app.send_chat_action(message.chat.id, ChatAction.TYPING)

            url = f"https://opentdb.com/api.php?amount=1&category={random.choice(categories)}&type=multiple"
            await log_message("Sending request to OpenTDB.")
            response = requests.get(url).json()
            await log_message(f"Received response: {response}")

            question_data = response["results"][0]
            question = question_data["question"]
            correct_answer = question_data["correct_answer"]
            incorrect_answers = question_data["incorrect_answers"]

            all_answers = incorrect_answers + [correct_answer]
            random.shuffle(all_answers)

            correct_option_id = all_answers.index(correct_answer)

            active_poll_message = await app.send_poll(
                chat_id=message.chat.id,
                question=question,
                options=all_answers,
                is_anonymous=False,
                type=PollType.QUIZ,
                correct_option_id=correct_option_id,
            )
            await log_message("Poll sent successfully.")

            # Wait 10 minutes before deleting the poll and sending a new one
            await asyncio.sleep(600)
            await log_message("10-minute sleep completed.")

            # Delete the poll if still active and quiz is on
            if is_quiz_on:
                await app.delete_messages(message.chat.id, active_poll_message.message_id)
                await log_message("Poll deleted.")

    # Stop the quiz if "off" is passed
    elif len(message.command) > 1 and message.command[1].lower() == "off":
        await log_message("/quiz off command received.")
        if not is_quiz_on:
            await message.reply_text("Quiz is not running!")
            return

        is_quiz_on = False
        await message.reply_text("Quiz stopped.")
        await log_message("Quiz stopped successfully.")

# /new command for generating a new quiz immediately
@app.on_message(filters.command(["new", "ew", "newquiz", "ewquiz"], prefixes=["/", "!", ".", "N", "n"]))
async def new_quiz(client, message):
    global active_poll_message
    await log_message("/new command received.")
    if active_poll_message:
        await app.delete_messages(message.chat.id, active_poll_message.message_id)
        await log_message("Old poll deleted.")
        await quiz(client, message)

# Ranks command with multiple variations and buttons for "Today", "Week", "Overall"
@app.on_message(filters.command(["quizranks", "uziranks", "ranks"], prefixes=["/", "!", ".", "Q", "q"]))
async def quiz_ranks(client, message):
    await log_message("/quizranks command received.")
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
    await log_message(f"Rank button {callback_query.data} pressed.")
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
    await log_message(f"Ranks displayed for {period}.")

# Handle poll answers to update scores
@app.on_message(filters.poll)
async def handle_poll(client, message):
    await log_message("Poll message received.")
    if message.poll.is_closed:
        return

    poll_answers = message.poll.options
    correct_option_id = message.poll.correct_option_id

    # Increment the score for the user who answered correctly
    for answer in poll_answers:
        if answer.voter_count > 0 and poll_answers.index(answer) == correct_option_id:
            user_id = message.from_user.id
            now = datetime.now()

            if user_id in quiz_scores:
                _, current_score = quiz_scores[user_id]
                quiz_scores[user_id] = (now, current_score + 1)
            else:
                quiz_scores[user_id] = (now, 1)

    await log_message(f"Scores updated: {quiz_scores}")
