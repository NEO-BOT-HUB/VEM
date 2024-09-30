import requests
from DnsXMusic import app
from pyrogram import filters

# Function to call the GPT API
def call_gpt_api(question):
    try:
        # Send a request to the GPT API with the question
        response = requests.get(f"https://chatgpt.apiitzasuraa.workers.dev/?question={question}")
        
        # Log the raw API response for debugging
        print(f"API Response: {response.text}")
        
        # Check if the request was successful
        if response.status_code == 200:
            json_response = response.json()
            
            # Log the JSON response for debugging
            print(f"JSON Response: {json_response}")
            
            # Return the response text or a message if not found
            return json_response.get("response", "No 'response' field found in the API response.")
        else:
            return f"Error {response.status_code}: Failed to get a valid response from the API."
    
    except Exception as e:
        # Return a more detailed error message
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

