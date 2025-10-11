import os
import discord
from discord.ext import commands

# โหลด TOKEN จาก Railway Environment
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 🔥 Trigger หลายคำ พร้อมรูปจาก URL
TRIGGERS = {
    "แมว": ("นี่รูปแมว 🐱", "https://i.imgur.com/jG4Qy0O.jpg"),
    "หมา": ("หมาน่ารักมั้ย 🐶", "https://i.imgur.com/NX2r7zA.jpg"),
    "สวัสดี": ("สวัสดีครับ! 😄", "https://i.imgur.com/0o0uEgc.jpg"),
    "บอทอยู่ไหม": ("ผมอยู่ครับ! ⚡", "https://i.imgur.com/v5LwSrx.png")
}

@bot.event
async def on_ready():
    print(f"✅ บอทออนไลน์แล้วในชื่อ: {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # ตรวจว่ามีคำ trigger ในข้อความไหม
    for key, (text, img_url) in TRIGGERS.items():
        if key in message.content:
            embed = discord.Embed(description=text, color=0x00BFFF)
            embed.set_image(url=img_url)
            await message.channel.send(embed=embed)
            break

    await bot.process_commands(message)


# คำสั่งทดสอบ (พิมพ์ !ping แล้วบอทจะตอบกลับ)
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

bot.run(TOKEN)
