import yt_dlp

def download_audio(link):
    options = {
        'format': 'bestaudio/best',
        'outtmpl': './downloads/%(title)s.%(ext)s',
        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
            {
                'key': 'FFmpegMetadata',
            },
            {
                'key': 'EmbedThumbnail',
            },
        ],
        'writethumbnail': True,
        'quiet': False,
        'verbose': True,
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([link])
        print("Download completo!")
    except Exception as e:
        print(f"Erro ao baixar o vídeo: {e}")
