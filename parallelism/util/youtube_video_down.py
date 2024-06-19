import yt_dlp

async def get_video_sound(url, video_id, folder): 

# URLS = ['https://www.youtube.com/watch?v=nukfvhDi6oI&t=7236s']
    folder = 'test'
    video_id = '1'
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