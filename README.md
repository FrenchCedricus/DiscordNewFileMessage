# DiscordNewFileMessage
This python script send message to a specific channel when a new file is added to a folder.

# Starting
Before everything, you must have a discord bot with the "Message" intent activate. You can create a bot easily on the discord developer portal, and add all the intent on it.
You must have your discord bot private token, and your channel ID (accessible by left clicking on your channel, with developer mode on)


Let's begin : 
Once you have cloned the repo, you must lunch :
```pip install -r requirements.txt```

After, you would open the "main.py" file, here is all the code of the bot.
Le's begin by adding your private token on : 
```TOKEN = 'YOUR_DISCORD_BOT_TOKEN_HERE'```

And you channel id : 
```CHANNEL_ID = 123456789```

And that's it for the principal. you should run the python script, and enjoyed !


# Adding the "on_deleted" method
This method send message when you delete a folder, it's the same as the creation method, just the name change, due to watchdog :
```    
    def on_deleted(self, event):
        if not event.is_directory:
            file_path = Path(event.src_path)
            filename = file_path.name
            message = f"Deleted file : {filename}"
            
            # Send a message in the discord channel
            coro = self.channel.send(message)
            fut = asyncio.run_coroutine_threadsafe(coro, client.loop)
            try:
                fut.result()
            except Exception as e:
                print(f"Error. Impossible to send the message : {e}")
```

You would add it just after the "on_created" method, be carrful with the indentation !