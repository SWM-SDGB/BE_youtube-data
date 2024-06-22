import os

import yt_dlp

async def get_video_sound(url, video_id, folder):
    filename = video_id+'.m4a'
    file_path = os.path.join(folder,filename)
    if os.path.exists(file_path):
        print(f"파일 '{filename}'이 이미 존재하여 넘어갑니다.")
    else:
        # URLS = ['https://www.youtube.com/watch?v=nukfvhDi6oI&t=7236s']
        ydl_opts = {
            'format': 'm4a/bestaudio/best',
            'outtmpl': f"./{folder}/{video_id}",
            # ℹ️ See help(yt_dlp.postprocessor) for a list of available Postprocessors and their arguments
            'postprocessors': [{  # Extract audio using ffmpeg
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
            }]
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download(url)