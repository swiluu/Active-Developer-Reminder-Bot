import os
import json
import asyncio
import datetime
import discord
from discord import app_commands
from discord.ext import commands, tasks
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable is not set")

# Data storage
DATA_FILE = 'reminder_data.json'

# Load or create data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    else:
        default_data = {
            "users": [],
            "last_reminder": None,
            "interval_days": 25
        }
        save_data(default_data)
        return default_data

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Load data
data = load_data()

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Reminder task - checks once per day if reminders need to be sent
@tasks.loop(hours=24)
async def reminder_check():
    print(f"Running reminder check at {datetime.datetime.now().isoformat()}")
    
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # If this is the first run or last_reminder is not set
    if data["last_reminder"] is None:
        data["last_reminder"] = today
        save_data(data)
        return
    
    # Handle different date formats - the error occurs when transitioning from test mode
    try:
        # Try parsing as date only format first
        last_date = datetime.datetime.strptime(data["last_reminder"], '%Y-%m-%d')
    except ValueError:
        try:
            # If that fails, try parsing as ISO format
            last_date = datetime.datetime.fromisoformat(data["last_reminder"])
            # Update the format in the data file to be consistent going forward
            data["last_reminder"] = last_date.strftime('%Y-%m-%d')
            save_data(data)
        except Exception as e:
            print(f"Error parsing date: {e}")
            # Reset the reminder date if we can't parse it
            data["last_reminder"] = today
            save_data(data)
            return
    
    current_date = datetime.datetime.strptime(today, '%Y-%m-%d')
    days_passed = (current_date - last_date).days
    
    # Check if it's time to send a reminder (every 25 days)
    if days_passed >= data["interval_days"]:
        await send_reminders()
        data["last_reminder"] = today
        save_data(data)

async def send_reminders():
    for user_id in data["users"]:
        try:
            user = await bot.fetch_user(int(user_id))
            
            # Find a suitable channel to link to
            channel_link = "your server"
            for guild in bot.guilds:
                member = guild.get_member(int(user_id))
                if member:
                    # Find the first text channel the user has access to
                    for channel in guild.text_channels:
                        permissions = channel.permissions_for(member)
                        if permissions.send_messages:
                            channel_link = f"https://discord.com/channels/{guild.id}/{channel.id}"
                            break
                    break
            
            await user.send(f"Reminder: Please type `/confirm` in {channel_link} to confirm your activity!")
            print(f"Sent reminder to {user.name} ({user_id})")
        except Exception as e:
            print(f"Failed to send reminder to user {user_id}: {e}")

# Bot events
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('------')
    
    # Start the reminder task
    if not reminder_check.is_running():
        reminder_check.start()
    
    # Sync slash commands to each guild specifically
    try:
        print("Attempting to sync commands to guilds...")
        for guild in bot.guilds:
            try:
                guild_commands = await bot.tree.sync(guild=discord.Object(id=guild.id))
                print(f"Synced {len(guild_commands)} command(s) to guild {guild.name} ({guild.id})")
            except Exception as e:
                print(f"Failed to sync commands to guild {guild.id}: {e}")
        
        # Also try global sync
        print("Attempting global sync...")
        global_commands = await bot.tree.sync()
        print(f"Synced {len(global_commands)} command(s) globally")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# Manual sync command for troubleshooting
@bot.command(name="sync")
@commands.is_owner()
async def sync_command(ctx):
    try:
        await ctx.send("Syncing commands...")
        
        # Sync to the current guild first
        guild_commands = await bot.tree.sync(guild=discord.Object(id=ctx.guild.id))
        await ctx.send(f"Synced {len(guild_commands)} command(s) to this guild")
        
        # Then try global sync
        global_commands = await bot.tree.sync()
        await ctx.send(f"Synced {len(global_commands)} command(s) globally")
    except Exception as e:
        await ctx.send(f"Failed to sync commands: {e}")

# Slash Commands
@bot.tree.command(name="add_reminder", description="Add yourself to the 25-day reminder list")
async def add_reminder(interaction: discord.Interaction):
    try:
        user_id = str(interaction.user.id)
        
        if user_id not in data["users"]:
            data["users"].append(user_id)
            save_data(data)
            await interaction.response.send_message("You've been added to the reminder list! You'll be reminded every 25 days to confirm your activity.", ephemeral=True)
        else:
            await interaction.response.send_message("You're already on the reminder list!", ephemeral=True)
    except Exception as e:
        print(f"Error in add_reminder: {e}")
        if not interaction.response.is_done():
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)
        else:
            await interaction.followup.send(f"An error occurred: {e}", ephemeral=True)

@bot.tree.command(name="remove_reminder", description="Remove yourself from the reminder list")
async def remove_reminder(interaction: discord.Interaction):
    try:
        user_id = str(interaction.user.id)
        
        if user_id in data["users"]:
            data["users"].remove(user_id)
            save_data(data)
            await interaction.response.send_message("You've been removed from the reminder list!", ephemeral=True)
        else:
            await interaction.response.send_message("You're not on the reminder list!", ephemeral=True)
    except Exception as e:
        print(f"Error in remove_reminder: {e}")
        if not interaction.response.is_done():
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)
        else:
            await interaction.followup.send(f"An error occurred: {e}", ephemeral=True)

@bot.tree.command(name="confirm", description="Confirm your activity")
async def confirm(interaction: discord.Interaction):
    try:
        await interaction.response.send_message("Thank you for confirming your activity!", ephemeral=True)
        print(f"User {interaction.user.name} ({interaction.user.id}) confirmed their activity")
    except Exception as e:
        print(f"Error in confirm: {e}")
        if not interaction.response.is_done():
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)
        else:
            await interaction.followup.send(f"An error occurred: {e}", ephemeral=True)

@bot.tree.command(name="next_reminder", description="Check when the next reminder will be sent")
async def next_reminder(interaction: discord.Interaction):
    try:
        if data["last_reminder"] is None:
            await interaction.response.send_message("No reminders have been sent yet.", ephemeral=True)
            return
        
        last_date = datetime.datetime.strptime(data["last_reminder"], '%Y-%m-%d')
        next_date = last_date + datetime.timedelta(days=data["interval_days"])
        today = datetime.datetime.now()
        days_left = (next_date - today).days + 1
        
        if days_left > 0:
            await interaction.response.send_message(
                f"Next reminder will be sent in {days_left} days (on {next_date.strftime('%Y-%m-%d')}).", 
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"Reminder is due to be sent today!", 
                ephemeral=True
            )
    except Exception as e:
        print(f"Error in next_reminder: {e}")
        if not interaction.response.is_done():
            await interaction.response.send_message(f"An error occurred: {e}", ephemeral=True)
        else:
            await interaction.followup.send(f"An error occurred: {e}", ephemeral=True)

# Add global error handler for interactions
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error):
    print(f"Command error: {error}")
    if not interaction.response.is_done():
        await interaction.response.send_message(f"An error occurred: {error}", ephemeral=True)
    else:
        await interaction.followup.send(f"An error occurred: {error}", ephemeral=True)

# Run the bot
if __name__ == "__main__":
    bot.run(TOKEN)
