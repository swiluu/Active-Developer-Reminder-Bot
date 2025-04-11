# Discord Confirm Reminder Bot

A simple Discord bot that reminds users every 25 days to type `/confirm` as a command.

## Features

- Sends reminders to users every 25 days
- Uses Discord's slash commands
- Allows users to add or remove themselves from the reminder list
- Provides information about when the next reminder will be sent

## Prerequisites

1. **Install Python**
   - Download and install Python 3.8 or newer from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation
   - Verify installation by opening a terminal/command prompt and typing:
     ```
     python --version
     ```
   - If the above command doesn't work, try:
     ```
     python3 --version
     ```
   - You should see the Python version number if installation was successful
   - Note: On some systems, particularly Linux and macOS, Python 3 is accessed using the `python3` command instead of `python`

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
   - Remove `REMOVETHIS` after editing your `.env` file

5. **Run the Bot**
   ```
   python confirm_bot.py
   ```
   If the above command doesn't work, try:
   ```
   python3 confirm_bot.py
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

## Hosting Options

The bot needs to be running continuously to send reminders. Here are some hosting options:

1. **Local Computer**: Only works when your computer is on
2. **VPS (Virtual Private Server)**: Services like DigitalOcean, Linode, or AWS
3. **PythonAnywhere**: Free tier available, good for small bots
4. **Railway.app**: Easy deployment, free tier available
5. **Replit**: Free hosting with some limitations
6. **Heroku**: Free tier discontinued, but paid options available

## Auto-Start on Linux Server

To make the bot automatically start when your Linux server boots up, you can use systemd:

1. **Create a Service File**:
   ```bash
   sudo nano /etc/systemd/system/discord-reminder.service
   ```

2. **Add the Following Content** (adjust paths as needed):
   ```
   [Unit]
   Description=Discord Reminder Bot
   After=network.target

   [Service]
   User=your_username
   WorkingDirectory=/path/to/discord-confirm-reminder
   ExecStart=/usr/bin/python3 /path/to/discord-confirm-reminder/confirm_bot.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

3. **Reload the systemd daemon** (important step!):
   ```bash
   sudo systemctl daemon-reload
   ```

4. **Enable and Start the Service**:
   ```bash
   sudo systemctl enable discord-reminder.service
   sudo systemctl start discord-reminder.service
   ```

5. **Check Status**:
   ```bash
   sudo systemctl status discord-reminder.service
   ```

This will ensure your bot starts automatically when the server boots and restarts if it crashes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
