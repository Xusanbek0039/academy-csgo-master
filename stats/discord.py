import discord_notify

def send_message_discord(hook_url,message):
    notifier = discord_notify.Notifier(hook_url)
    notifier.send(message,print_message=False)
