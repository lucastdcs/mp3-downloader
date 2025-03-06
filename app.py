from pytubefix import YouTube
import os
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
import requests

# Entrada dinâmica de URLs pelo usuário
urls = []
print("Adicione as URLs, uma a uma. Após selecionar todas, deixe um espaço vazio e aperte 'Enter'")
while True:
    url = input(">> ")
    if not url:
        break
    urls.append(url)

# Verifica se alguma URL foi adicionada
if not urls:
    print("Nenhuma URL fornecida. Encerrando o programa.")
    exit()

# Caminho de destino para salvar os arquivos
print("Digite o destino (deixe em branco para usar o diretório atual):")
destination = str(input(">> ")) or '.'

# Loop para processar cada URL

# Caminho onde os arquivos serão salvos
destination = "./downloads"


for url in urls:
    try:
        # Cria o objeto YouTube
        yt = YouTube(url)
        
        # Extrai apenas o áudio
        audio_stream = yt.streams.filter(only_audio=True).first()

        # Faz o download do áudio
        out_file = audio_stream.download(output_path=destination)

        # Salva o arquivo como MP3
        base, ext = os.path.splitext(out_file)
        mp3_file = base + ".mp3"
        os.rename(out_file, mp3_file)

        # Baixa a thumbnail do vídeo
        thumbnail_url = yt.thumbnail_url
        thumbnail_data = requests.get(thumbnail_url).content
        thumbnail_path = os.path.join(destination, "thumbnail.jpg")
        with open(thumbnail_path, "wb") as thumb_file:
            thumb_file.write(thumbnail_data)

        # Adiciona a capa ao arquivo MP3
        audio = MP3(mp3_file, ID3=ID3)

        if audio.tags is None:
            audio.add_tags()

        audio.tags.add(
            APIC(
                encoding=3,  # UTF-8
                mime="image/jpeg",  # Tipo de imagem
                type=3,  # Capa da frente
                desc="Capa",
                data=thumbnail_data,
            )
        )

        audio.save()

        # Remove a thumbnail temporária
        os.remove(thumbnail_path)

        print(f"'{yt.title}' foi baixado e a capa adicionada com sucesso!")

    except Exception as e:
        print(f"Erro ao processar {url}: {e}")
