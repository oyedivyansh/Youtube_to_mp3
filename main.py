# youtube_mp3_downloader/main.py

from flask import Flask, request, send_file, jsonify
import yt_dlp
import os
import uuid

app = Flask(__name__)
DOWNLOADS_DIR = "downloads"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

@app.route("/download", methods=["POST"])
def download_audio():
    try:
        data = request.json
        url = data.get("url")
        if not url:
            return jsonify({"error": "No URL provided"}), 400

        filename = f"{uuid.uuid4()}.mp3"
        output_path = os.path.join(DOWNLOADS_DIR, filename)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
