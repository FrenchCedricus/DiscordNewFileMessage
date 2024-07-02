import os
import time
import discord
import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path

# Configuration du Bot Discord
TOKEN = 'YOUR_TOKEN_HERE'
CHANNEL_ID = 123456789 #YOUR CHANNEL ID HERE (DEVELOPPER MODE)

# Initialisation du client Discord
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Handler pour les nouveaux fichiers
class NewFileHandler(FileSystemEventHandler):
    def __init__(self, channel):
        self.channel = channel

    def on_created(self, event):
        if not event.is_directory:
            file_path = Path(event.src_path)
            filename = file_path.name
            parent_dir = file_path.parent.name
            message = f"[{parent_dir}] Ajout de : {filename}"
            
            # Envoyer un message dans le canal Discord
            coro = self.channel.send(message)
            fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
            try:
                fut.result()
            except Exception as e:
                print(f"Erreur lors de l'envoi du message : {e}")

@client.event
async def on_ready():
    print(f'Connecté en tant que {client.user} avec {client.latency}ms')
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print(f"Le canal avec l'ID {CHANNEL_ID} est introuvable")
        return

    # Surveiller le répertoire où les fichiers sont ajoutés
    event_handler = NewFileHandler(channel)
    observer = Observer()
    observer.schedule(event_handler, path='./', recursive=True)
    observer.start()
    print(f"Surveillance du dossier : ./")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Connexion et exécution du client Discord
client.run(TOKEN)