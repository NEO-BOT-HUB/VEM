import requests
from bs4 import BeautifulSoup
from pyrogram import filters
from DnsXMusic import app  # Your existing bot's app

# Function to scrape content from fastvideosave.net
def download_content_from_fastvideosave(url):
    # Request the webpage
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    data = {
        'url': url
    }
    response = requests.post('https://fastvideosave.net/download', headers=headers, data=data)
    
    if response.status_code == 200:
        # Parse the HTML page
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the download link (adjust this part based on the actual HTML structure)
        download_link = soup.find('a', {'class': 'download-btn'})  # Update selector as per HTML structure
        
        if download_link:
            return download_link['href']
        else:
            return "Download link not found!"
    else:
        return "Failed to reach website!"

# Bot function to handle the user's input link
@app.on_message(filters.text & filters.private)
def handle_message(client, message):
    url = message.text
    if "instagram.com" in url or "facebook.com" in url:  # Supported platforms
        media_url = download_content_from_fastvideosave(url)
        message.reply_text(f"Here's your content: {media_url}")
    else:
        message.reply_text("Please send a valid social media link (Instagram, Facebook, etc.).")
