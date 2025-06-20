# youtube_mp3_downloader/app.py

import yt_dlp
import uuid
import os
import streamlit as st
from pathlib import Path

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
        st.error(f"❌ Error: {str(e)}")

elif download_clicked:
    st.warning("Please enter a valid YouTube URL")
