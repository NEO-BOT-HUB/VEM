import requests
from DnsXMusic import app  # Importing app from DnsXMusic
from pyrogram import filters

# Function to call the GPT API
def call_gpt_api(question):
    try:
        # Send a request to the GPT API with the question
        response = requests.get(f"https://chatgpt.apiitzasuraa.workers.dev/?question={question}")
        
        # Check if the request was successful
        if response.status_code == 200:
            return response.json().get("response", "Sorry, I couldn't get a response.")
        else:
            return f"Error {response.status_code}: Failed to get a response from the API."
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Handler for the bot commands
@app.on_message(filters.command(["era", "ra"], prefixes=["/", "!", ".", "e", "E"]))
def gpt_response_handler(client, message):
    # Get the user's query after the command
    user_query = message.text.split(" ", 1)  # Split the message to extract the query

    # Check if a query is provided
    if len(user_query) > 1:
        question = user_query[1]  # Get the query text
        gpt_response = call_gpt_api(question)  # Call the GPT API
        
        # Send the GPT response back to the user
        message.reply_text(gpt_response)
    else:
        message.reply_text("Please provide a question after the command.")

# You don't need to call app.run() since the app from DnsXMusic is already running in your project
