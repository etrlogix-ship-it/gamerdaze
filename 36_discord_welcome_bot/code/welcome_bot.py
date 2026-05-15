#!/usr/bin/env python3
"""Discord Welcome Bot - Project 36
Auto-welcome new members to your Discord server.
Install: pip install discord.py
Setup: Create a bot at discord.com/developers, get token, invite to server.
"""
import os
import random

try:
    import discord
    from discord.ext import commands
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False

TOKEN = os.environ.get("DISCORD_TOKEN", "")
WELCOME_CHANNEL = "general"  # channel name to post welcome messages

WELCOME_MESSAGES = [
    "Welcome to the server, {mention}! 🎮 Grab a role and join the game!",
    "A new challenger has entered! Welcome {mention}! ⚔️",
    "{mention} has joined the server! Get ready for an adventure! 🚀",
    "Welcome {mention}! Don't forget to read the rules in #rules 📜",
    "🎉 {mention} just landed in the server! Welcome aboard!",
]

def demo_mode():
    print("\n  🎭 DEMO MODE — Discord bot simulation")
    print("  (Set DISCORD_TOKEN env var to run for real)\n")
    names = ["Steve", "Alex", "Notch", "Herobrine"]
    import time
    for name in names:
        msg = random.choice(WELCOME_MESSAGES).format(mention=f"@{name}")
        print(f"  📨 New member: {name}")
        print(f"  Bot posted: {msg}\n")
        time.sleep(1)
    print("  Demo complete!")

if not DISCORD_AVAILABLE:
    print("discord.py not installed. Run: pip install discord.py")
    demo_mode()
elif not TOKEN:
    print("No DISCORD_TOKEN found. Running demo mode.")
    demo_mode()
else:
    intents = discord.Intents.default()
    intents.members = True
    intents.message_content = True
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"  ✅ Logged in as {bot.user}")
        print(f"  Watching for new members...")

    @bot.event
    async def on_member_join(member):
        channel = discord.utils.get(member.guild.text_channels, name=WELCOME_CHANNEL)
        if channel:
            msg = random.choice(WELCOME_MESSAGES).format(mention=member.mention)
            await channel.send(msg)
            print(f"  Welcomed {member.name}")

    @bot.command()
    async def ping(ctx):
        await ctx.send(f"🏓 Pong! {round(bot.latency * 1000)}ms")

    print("Starting Discord Welcome Bot...")
    bot.run(TOKEN)
