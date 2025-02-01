import os
from dotenv import load_dotenv

import discord
from discord.ext import commands, tasks
from youtube_scraper import YouTubeScraper
from get_google_sheets import GoogleSheetsService

# load env 
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")  # from .env read Token
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))  # from .env read Channel ID
RESUME_CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))  # from .env read Channel ID
yt_list = "youtube_list.txt"

# set Intents
intents = discord.Intents.default()  # ues default Intents
intents.message_content = True  # activate message content event

# set up Bot command prefix -> commands starting with "!" eg. !hello, the bot will recognize it as a command
bot = commands.Bot(command_prefix="!", intents=intents)

# init google sheet service
sheets_service = GoogleSheetsService()

# activate Bot
@bot.event
async def on_ready():
    print(f'{bot.user} is running！')  # Bot running
    print(f'# Numbers of Server: {len(bot.guilds)}')  # guilds = discord server
    checkin_link.start()  # Send the checkin link 
    fetch_youtube_updates.start()  # Start the task to fetch YouTube updates
    # fetch_sheet_updates.start() # Start the task to fetch sheet updates


# Task1: send checkin link every hour
@tasks.loop(hours=1)  # hours=1 # seconds=1
async def checkin_link():
    channel = bot.get_channel(CHANNEL_ID)  # get channel id
    
    if channel:
        await channel.send("CheckIn Link！🌟")
        print("msg sent: happy hour")
    else:
        print("Can not find the channel Id, please make sure the discord channel id is correct。")


# Task2: Fetch and send YouTube updates every hour
@tasks.loop(hours=1)
async def fetch_youtube_updates():

    # Read channels from yt_list
    try:
        with open(yt_list, "r") as file:
            yt_channels = [line.strip() for line in file.readlines() if line.strip()]
    except FileNotFoundError:
        print("Error: channels.txt file not found.")
        return

    # Fetch and send updates for each channel
    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("Invalid Discord channel ID. Please check the configuration.")
        return

    for yt_channel_url in yt_channels:
        scraper = YouTubeScraper(yt_channel_url)  # Initialize the scraper for the channel
        scraper.fetch_html()  # Fetch HTML content
        latest_video = scraper.get_latest_video_info()  # Get latest video info

        # if latest_video:
        #     await channel.send(f"New video from {latest_video['author']}:\n{latest_video['title']}\n{latest_video['url']}")
        #     print(f"Sent update for {yt_channel_url}")
        if latest_video:
            # Create an embed message
            embed = discord.Embed(
                title=f"{latest_video['author']}'s New Video 🎥",  # Title
                description=f"{latest_video['title']}\n\n[Watch Now!]({latest_video['url']})",  # Description
                color=discord.Color.blue()  # Color
                )
            embed.add_field(name="Uploaded", value=latest_video['time_ago'], inline=True)
            embed.set_footer(text="YouTube Updates by SquarieBot")  # Footer for branding
            
            # Send the embed message
            await channel.send(embed=embed)
            print(f"Sent update for {yt_channel_url}")
        else:
            print(f"Failed to fetch video info for {yt_channel_url}")


# Task 2: Fetch Google Sheets updates every hour
@tasks.loop(seconds=1)
async def fetch_sheet_updates():

    channel = bot.get_channel(CHANNEL_ID)
    if not channel:
        print("Invalid Discord channel ID.")
        return
    # Fetch data from Google Sheets
    try:
        data = sheets_service.read_sheets()
        if data:
            for row in data:
                message = " | ".join(row)  # Format the row as a string
                await channel.send(message)
                print("Google Sheets updated on discord.")
        else:
            print("No data found in Google Sheets.")
    except Exception as e:
        print(f"Error fetching data from Google Sheets: {e}")


## command test
# command：ping
@bot.command()
async def ping(ctx):
    """Reply 'Pong!'"""
    await ctx.send('Pong!')


# command：hello
@bot.command()
async def hello(ctx):
    """Reply user name"""
    await ctx.send(f"Hello, {ctx.author.mention}!")  # Reply user's name


# MAIN ENTRY POINT
def main() -> None:
    bot.run(token=TOKEN)


if __name__ == '__main__':
    main()