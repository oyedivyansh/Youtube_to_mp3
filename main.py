# youtube_mp3_downloader/app.py

import yt_dlp
import uuid
import os
import streamlit as st
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# Create downloads directory
DOWNLOAD_DIR = Path("downloads")
DOWNLOAD_DIR.mkdir(exist_ok=True)

st.set_page_config(page_title="YouTube to MP3 Downloader", layout="centered")
st.title("🎵 YouTube to MP3 Downloader")
st.markdown("""
Enter a YouTube video URL below and download the audio in MP3 format. Works on mobile and desktop.
""")

# User input
url = st.text_input("🔗 YouTube Video URL", placeholder="https://www.youtube.com/watch?v=...")
download_clicked = st.button("🎧 Download MP3")

# Normalize URL (handle shorts, youtu.be, remove extra params)
def normalize_youtube_url(url):
    if "youtube.com/shorts/" in url:
        video_id = url.split("/shorts/")[-1].split("?")[0]
        return f"https://www.youtube.com/watch?v={video_id}"
    elif "youtu.be/" in url:
        video_id = url.split("youtu.be/")[-1].split("?")[0]
        return f"https://www.youtube.com/watch?v={video_id}"
    elif "watch?v=" in url:
        video_id = url.split("watch?v=")[-1].split("&")[0]
        return f"https://www.youtube.com/watch?v={video_id}"
    return url

# Apply normalization
if url:
    url = normalize_youtube_url(url)

# Handle download
if download_clicked and url:
    try:
        st.info("Downloading... Please wait")
        filename = f"{uuid.uuid4()}.mp3"
        output_path = DOWNLOAD_DIR / filename

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': str(output_path),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        with open(output_path, "rb") as f:
            st.success("Download ready!")
            st.download_button(
                label="⬇️ Click here to download MP3",
                data=f,
                file_name="youtube_audio.mp3",
                mime="audio/mpeg"
            )

    except Exception as e:
        if "This content isn’t available" in str(e):
            st.error("❌ Error: This video is not available or is restricted.")
        else:
            st.error(f"❌ Error: {str(e)}")

elif download_clicked:
    st.warning("Please enter a valid YouTube URL")
