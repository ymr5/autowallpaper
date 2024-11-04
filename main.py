import requests, random, json, ctypes
from PIL import Image
from io import BytesIO
from pathlib import Path

WALLPAPER_PATH = Path(__file__).parent / "wallpaper" / "current_wallpaper.jpg"
print(WALLPAPER_PATH)

# Download image for wallpaper
def download_image(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img.save(save_path)
    else:
        print("Failed to download image.")

# Set wallpaper
def set_wallpaper(image_url, save_image_path):
    download_image(image_url, save_image_path)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, str(save_image_path), 3)

subreddit_url = "https://www.reddit.com/r/MEOW_IRL/.json"
response = requests.get(subreddit_url)

if response.status_code == 200:
    data = response.json()
    posts = data["data"]["children"]
    
    # Filter image posts
    image_posts = [
        post["data"]["url"] for post in posts
        if post["data"]["url"].endswith(('.jpg', '.jpeg', '.png'))
    ]

    # Choose a random post
    if image_posts:
        image_url = random.choice(image_posts)

        # Finalize wallpaper
        set_wallpaper(image_url, WALLPAPER_PATH)
    else:
        print("Image search failed.")
else:
    print("Failed to fetch subreddit data.")
