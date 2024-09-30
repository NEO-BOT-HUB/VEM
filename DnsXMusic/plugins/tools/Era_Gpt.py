import requests
from DnsXMusic import app
from pyrogram import filters

# Function to call the GPT API
def call_gpt_api(question):
    try:
        # Send a request to the GPT API with the question
        response = requests.get(f"https://chatgpt.apiitzasuraa.workers.dev/?question={question}")
        
        # Check if the request was successful
        if response.status_code == 200:
            json_response = response.json()

            # Log only the essential info
            if "response" in json_response:
                print(f"GPT Response: {json_response['response']}")
                return json_response['response']
            else:
                print(f"Unexpected JSON structure: {json_response}")
                return "No valid response field found in the API result."
        else:
            print(f"Error {response.status_code}: Failed to get a valid response from the API.")
            return f"Error {response.status_code}: API returned an error."
    
    except Exception as e:
        # Log a clean error message
        print(f"Exception occurred: {str(e)}")
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

