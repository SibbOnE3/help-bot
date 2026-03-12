import discord
from discord.ext import commands
from discord import app_commands

# --- CONFIGURATION ---
BOT_TOKEN = "MTQ4MTc1MTczOTM4MzI4Nzg1OA.GwtBKU.CtmdC15dsyFnC9nXqnqA5Z2-gohI-zNTboP4AY"
YOUR_USER_ID = 1447964160691278000 # Your exact Discord ID

# Set up intents
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# --- SECURITY CHECK ---
# This function ensures ONLY you can use the commands
def is_owner():
    def predicate(interaction: discord.Interaction):
        return interaction.user.id == YOUR_USER_ID
    return app_commands.check(predicate)

@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online and secured.")
    try:
        synced = await bot.tree.sync()
        print(f"🔄 Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# --- COMMAND 1: NORMAL MESSAGE ---
@bot.tree.command(name="say", description="Send a normal text message as the bot.")
@app_commands.describe(
    channel="The channel to send the message in",
    message="The text you want the bot to say"
)
@is_owner()
async def say(interaction: discord.Interaction, channel: discord.TextChannel, message: str):
    await channel.send(message)
    # Ephemeral means only you can see this confirmation message
    await interaction.response.send_message(f"✅ Message sent to {channel.mention}", ephemeral=True)

# --- COMMAND 2: EMBED MESSAGE ---
@bot.tree.command(name="embed", description="Send a styled embed message as the bot.")
@app_commands.describe(
    channel="The channel to send the embed in",
    title="The title of the embed",
    description="The main text of the embed",
    hex_color="The hex color code (e.g., #8b5cf6) - Optional"
)
@is_owner()
async def embed(interaction: discord.Interaction, channel: discord.TextChannel, title: str, description: str, hex_color: str = "#8b5cf6"):
    # Convert hex color string to discord color format
    try:
        color_int = int(hex_color.lstrip('#'), 16)
    except ValueError:
        color_int = 0x8b5cf6 # Fallback to Lunex Purple if invalid hex is provided
    
    # Build the embed
    em = discord.Embed(title=title, description=description, color=color_int)
    
    await channel.send(embed=em)
    await interaction.response.send_message(f"✅ Embed sent to {channel.mention}", ephemeral=True)

# --- ERROR HANDLING ---
# This silently rejects anyone else who tries to use the commands
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CheckFailure):
        await interaction.response.send_message("❌ Access Denied. You do not have authorization to command this bot.", ephemeral=True)
    else:
        print(f"An error occurred: {error}")

# Start the bot
bot.run(BOT_TOKEN)