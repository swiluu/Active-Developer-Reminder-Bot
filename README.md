# Discord Confirm Reminder Bot

A simple Discord bot that reminds users every 25 days to type `/confirm` as a command.

## Features

- Sends reminders to users every 25 days
- Uses Discord's slash commands
- Allows users to add or remove themselves from the reminder list
- Provides information about when the next reminder will be sent

## Prerequisites

1. **Install Python**

   ### Windows
   - Download the installer from [python.org](https://www.python.org/downloads/)
   - Run the installer
   - **Important**: Check "Add Python to PATH" during installation
   - Choose "Customize installation" (optional)
   - Click "Install Now"
   - Verify installation by opening Command Prompt and typing:
     ```
     python --version
     ```

   ### macOS
   - Download the installer from [python.org](https://www.python.org/downloads/)
   - Run the installer package
   - Follow the installation wizard
   - Verify installation by opening Terminal and typing:
     ```
     python3 --version
     ```
   - You can also install Python using Homebrew:
     ```
     brew install python
     ```

   ### Linux (Ubuntu/Debian)
   - Python is usually pre-installed, but you can ensure you have the latest version:
     ```
     sudo apt update
     sudo apt install python3 python3-pip
     ```
   - Verify installation:
     ```
     python3 --version
     ```

   ### Linux (CentOS/RHEL)
   - Install Python 3:
     ```
     sudo yum install python3 python3-pip
     ```
   - Verify installation:
     ```
     python3 --version
     ```

   If you see the Python version number, installation was successful. If using Python 3.x, you may need to use `python3` and `pip3` commands instead of `python` and `pip`.

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
   - Remove `REMOVETHIS` from your `.env` file

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

**Note**: Always remember to run `sudo systemctl daemon-reload` after making any changes to the service file. Without this step, systemd won't recognize your changes and may fail to start the service properly.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
