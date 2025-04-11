# Discord Confirm Reminder Bot

A simple Discord bot that reminds users every 25 days to type `/confirm` as a command.

## Features

- Sends reminders to users every 25 days
- Uses Discord's slash commands
- Allows users to add or remove themselves from the reminder list
- Provides information about when the next reminder will be sent

## Setup Instructions

1. **Create a Discord Bot**
   - Go to [Discord Developer Portal](https://discord.com/developers/applications)
   - Click "New Application" and give it a name
   - Go to the "Bot" tab and click "Add Bot"
   - Under "Privileged Gateway Intents", enable "Message Content Intent" and "Server Members Intent"
   - Copy your bot token

2. **Invite the Bot to Your Server**
   - In the Developer Portal, go to the "OAuth2" tab
   - In the "URL Generator" section, select the "bot" and "applications.commands" scopes
   - Select the permissions: "Send Messages", "Read Messages/View Channels"
   - Copy the generated URL and open it in your browser to invite the bot to your server

3. **Install Requirements**
   ```
   pip install -r requirements.txt
   ```

4. **Configure the Bot**
   - Edit the `.env` file to add your bot token
   - Replace `your_token_here` with your actual Discord bot token
   - Remove "REMOTETHIS" and the ending .example after editing your `.env` file

5. **Run the Bot**
   ```
   python confirm_bot.py
   ```

## Usage

- `/add_reminder` - Add yourself to the reminder list
- `/remove_reminder` - Remove yourself from the reminder list
- `/confirm` - Confirm your activity (this is what the bot will remind you to do)
- `/next_reminder` - Check when the next reminder will be sent

## Troubleshooting

If slash commands aren't appearing:
- Make sure you invited the bot with the `applications.commands` scope
- Try using the `!sync` command in your server
- Restart your Discord client
- Wait a few minutes as Discord can take time to register commands

## Note

The bot needs to be running continuously to send reminders. Consider hosting it on a server or using a service like Heroku for 24/7 operation.
