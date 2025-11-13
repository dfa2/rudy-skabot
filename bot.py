import discord
from discord import app_commands
from discord.ext import commands
import json
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

DECISION_FILE = "decisions.json"

def load_decisions():
    if os.path.exists(DECISION_FILE):
        with open(DECISION_FILE, "r") as f:
            return json.load(f)
    return []

def save_decisions(data):
    with open(DECISION_FILE, "w") as f:
        json.dump(data, f, indent=2)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"🎺 Logged in as {bot.user} (ID: {bot.user.id})")
    print("Ready to skank!")

# Slash command: /toot
@bot.tree.command(name="toot", description="Send a random ska horn blast 🎺")
async def toot(interaction: discord.Interaction):
    await interaction.response.send_message("🎺 TOOT TOOT! Ska lives on!")

# Slash command: /add_decision
@bot.tree.command(name="add_decision", description="Add a decision to the list")
@app_commands.describe(text="The decision you want to record")
async def add_decision(interaction: discord.Interaction, text: str):
    """Provide command /add_decision."""
    decisions = load_decisions()
    decisions.append({"author": interaction.user.name, "text": text})
    save_decisions(decisions)
    await interaction.response.send_message(f"✅ Decision added: +\"{text}\" by {interaction.user.name}")

# Slash command: /list_decisions
@bot.tree.command(name="list_decisions", description="Show the most recent decisions")
async def list_decisions(interaction: discord.Interaction):
    decisions = load_decisions()
    if not decisions:
        await interaction.response.send_message("No decisions yet.")
        return

    msg = "**Band Decisions:**\n"
    for i, d in enumerate(decisions[-10:], 1):
        msg += f"{i}. \"{d['text']}\" — {d['author']}\n"
    await interaction.response.send_message(msg)

bot.run(TOKEN)
