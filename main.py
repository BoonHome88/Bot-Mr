import os
import nextcord as discord
from nextcord.ext import commands

# โหลด TOKEN จาก Railway Environment
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True  # เปิดเพื่ออ่านข้อความ
bot = commands.Bot(command_prefix="!", intents=intents)

# 🔥 Trigger หลายคำ พร้อมข้อความหลายบรรทัด และรูปจาก URL
TRIGGERS = {
    "แมว": (
        "นี่รูปแมว 🐱",
        "https://i.imgur.com/jG4Qy0O.jpg"
    ),
    "หมา": (
        "หมาน่ารักมั้ย 🐶",
        "https://i.imgur.com/NX2r7zA.jpg"
    ),
    "สวัสดี": (
        "สวัสดีครับ! 😄",
        "https://i.imgur.com/0o0uEgc.jpg"
    ),
    "บอทอยู่ไหม": (
        "ผมอยู่ครับ! ⚡",
        "https://i.imgur.com/v5LwSrx.png"
    ),
    "hwไไไl": (
        """# เงื่อนไขการต่อไวลิส / เปลี่ยนดิส / เปลี่ยนสตีม
- ให้ผู้เล่นแชร์โพส https://www.facebook.com/share/19VEEcQ6YP/  ไปยังกลุ่มที่เกี่ยวกับ FiveM กลุ่มใดก็ได้ 1  กลุ่ม
- ส่งลิงค์ที่เป็นโพสของผู้เล่นแชร์มาให้ตรวจสอบ พร้อมแคปรูปมายัง Ticket ด้วยนะครับ
- หลังการส่งหลักฐานการแชร์แล้วรอทางทีมงานตรวจสอบ (ต่อไวลิสฟรี)

หากไม่สะดวกแชร์จะมีค่าใช้จ่ายในการต่อไวลิส 100 บาท / ครั้ง 🙏🏻


ตัวอย่างกลุ่ม
1. https://www.facebook.com/groups/FiveMThailand/posts/1496036151129221/
2. https://www.facebook.com/groups/289008456634964/
3. https://www.facebook.com/groups/364167337464759/
4. https://www.facebook.com/groups/communityfivem
5. https://www.facebook.com/groups/686633655307229/posts/1348306932473228/""",
        "https://img2.pic.in.th/pic/Untitled-16664908eb4ccba12.jpg"
    )
}

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "hwl" in message.content:  # Trigger ตัวอย่าง
        embed = discord.Embed(
            title="เงื่อนไขการต่อไวลิส / เปลี่ยนดิส / เปลี่ยนสตีม",
            color=0x00BFFF
        )
        
        # เพิ่มข้อความทีละบล็อก
        embed.add_field(
            name="📌 ขั้นตอน",
            value=(
                "- ให้ผู้เล่นแชร์โพส https://www.facebook.com/share/19VEEcQ6YP/ \n"
                "- ส่งลิงก์ไปให้ผู้เล่นตรวจสอบ พร้อมแนบรูปภาพหรือ Ticket ด้วยครับ\n"
                "- หลังการส่งหลักฐานการแชร์แล้วรอทางทีมงานตรวจสอบ (ต่อไวลิสฟรี)"
            ),
            inline=False
        )
        
        embed.add_field(
            name="💰 ค่าตรวจสอบ",
            value="หากไม่สะดวกจะมีค่าใช้จ่ายในการต่อไวลิส 100 บาท / ครั้ง 🙏",
            inline=False
        )
        
        embed.add_field(
            name="ตัวอย่างกลุ่ม",
            value=(
                "https://www.facebook.com/groups/FiveMThailand/posts/1496036151129221/\n"
                "https://www.facebook.com/groups/289008456634964/\n"
                "https://www.facebook.com/groups/364167337464759/\n"
                "https://www.facebook.com/groups/communityfivem\n"
                "https://www.facebook.com/groups/686633655307229/posts/1348306932473228/"
            ),
            inline=False
        )
        
        # เพิ่มรูป
        embed.set_image(url="https://i.imgur.com/yourimage.png")  # แทนด้วย URL ของรูปจริง
        
        await message.channel.send(embed=embed)

    await bot.process_commands(message)

@bot.event
async def on_ready():
    # ตั้ง Activity โดยไม่ขึ้น "กำลังเล่น"
    activity = discord.Activity(
        type=discord.ActivityType.watching,  # หรือ ActivityType.listening
        name="Developer By MOO TEDET99"
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"✅ บอทออนไลน์แล้วในชื่อ: {bot.user}")


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    for key, (text, img_url) in TRIGGERS.items():
        if key in message.content:
            embed = discord.Embed(description=text, color=0x00BFFF)
            embed.set_image(url=img_url)
            await message.channel.send(embed=embed)
            break

    await bot.process_commands(message)

# คำสั่งทดสอบ
@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

bot.run(TOKEN)
