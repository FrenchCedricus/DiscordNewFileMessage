import os
import time
import discord
import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path

# Discord bot configuration
TOKEN = 'YOUR_DISCORD_BOT_TOKEN_HERE' #Discord Developpeur portal
CHANNEL_ID = 123456789 #Your channel ID here (developer mode on discord)

# Discord bot initialisation
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Handler for the new files
class NewFileHandler(FileSystemEventHandler):
    def __init__(self, channel):
        self.channel = channel

    def on_created(self, event):
        if not event.is_directory:
            file_path = Path(event.src_path)
            filename = file_path.name
            message = f"New file : {filename}"
            
            # Send a message in the discord channel
            coro = self.channel.send(message)
            fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
            try:
                fut.result()
            except Exception as e:
                print(f"Error. Impossible to send the message : {e}")

@client.event
async def on_ready():
    print(f'Connected as{client.user} with {client.latency}ms')
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print(f"Error. The channel with ID {CHANNEL_ID} cannot be found")
        return

    # Watch the folder
    event_handler = NewFileHandler(channel)
    observer = Observer()
    observer.schedule(event_handler, path='./', recursive=True)
    observer.start()
    print(f"Watching the folder : YOUR/PATH/HERE")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Discord bot connexion and execution
client.run(TOKEN)