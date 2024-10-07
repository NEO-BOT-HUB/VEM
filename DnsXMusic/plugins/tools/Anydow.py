import requests
from DnsXMusic import app  # Importing the existing app

# All-in-one social media downloader API
DOWNLOADER_API = "https://bj-tricks.serv00.net/BJ_Coder-Apis/Fb-Downloader.php"

# Function jo social media link se media download karega
def download_content(url):
    # API ko call karna aur link send karna
    response = requests.get(f"{DOWNLOADER_API}?url={url}")
    if response.status_code == 200:
        data = response.json()
        if data["status"] == "success":
            return data.get("download_link", "Content not found!")
        else:
            return "Invalid link or failed to fetch content!"
    else:
        return "API request failed!"

# Bot function jo user ke link ko handle karega
@app.on_message(filters.text & filters.private)
def handle_message(client, message):
    url = message.text
    if "instagram.com" in url or "facebook.com" in url or "tiktok.com" in url:  # Supported platforms
        media_url = download_content(url)
        message.reply_text(f"Here's your content: {media_url}")
    else:
        message.reply_text("Please send a valid social media link (Instagram, Facebook, TikTok).")

# Bot ko run karna zaroori nahi, since app from DnsXMusic will handle this
