import os
import nextcord as discord
from nextcord.ext import commands, tasks
import asyncio
from aiohttp import web, ClientSession

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# 🔥 Trigger หลายคำ พร้อมข้อความหลายบรรทัด และรูปจาก URL
TRIGGERS = {
    "hwl": (
        """# เงื่อนไขการต่อไวลิส / เปลี่ยนดิส / เปลี่ยนสตีม
- ให้ผู้เล่นแชร์โพส: https://www.facebook.com/share/19VEEcQ6YP/
  ไปยังกลุ่มที่เกี่ยวกับ FiveM กลุ่มใดก็ได้ 1 กลุ่ม
- ส่งลิงค์โพสของผู้เล่นมาให้ตรวจสอบ พร้อมแคปรูปมายัง Ticket
- หลังส่งหลักฐานรอทางทีมงานตรวจสอบ (ต่อไวลิสฟรี)

💰 หากไม่สะดวกแชร์ มีค่าใช้จ่าย 100 บาท / ครั้ง

**ตัวอย่างกลุ่ม**
1. https://www.facebook.com/groups/FiveMThailand/posts/1496036151129221/
2. https://www.facebook.com/groups/289008456634964/
3. https://www.facebook.com/groups/364167337464759/
4. https://www.facebook.com/groups/communityfivem
5. https://www.facebook.com/groups/686633655307229/posts/1348306932473228/""",
        "https://img2.pic.in.th/pic/Untitled-16664908eb4ccba12.jpg"
    ),
    "payment": (
        """# โอนแล้วส่งสลิป พร้อมแจ้งเลข ID ให้กับทางแอดมินได้เลย ครับ / ค่ะ
**ทุกการโดเนทจะมี Coin สะสมให้นะครับ ยกเว้น ประมูล / เช่าอู่ / กรอบทวิต**

>>> สามารถดู Coin ได้ที่ F1 แอพ MRP SHOP จะมีของให้แลกด้วยครับ / ค่ะ
* เงื่อนไขเป็นไปตามเซิร์ฟเวอร์กำหนด""",
        "https://img2.pic.in.th/pic/11079_1a6183a4c19db5771.png"
    ),
}

@bot.event
async def on_ready():
    activity = discord.Activity(
        type=discord.ActivityType.watching,
        name="MOO TEDET99 🐷"
    )
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print(f"✅ บอทออนไลน์แล้วในชื่อ: {bot.user}")
    keep_alive.start()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    for key, (text, img_url) in TRIGGERS.items():
        if key in message.content.lower():
            await message.channel.send(text)
            if img_url != "-":
                embed = discord.Embed(color=0x00BFFF)
                embed.set_image(url=img_url)
                embed.set_footer(text="📌 โปรดอ่านให้ครบทุกข้อก่อนส่งหลักฐาน")
                await message.channel.send(embed=embed)
            break

    await bot.process_commands(message)

@bot.command()
async def ping(ctx):
    await ctx.send("🏓 Pong!")

# 🌐 Web server สำหรับ Railway
async def handle(request):
    return web.Response(text="✅ Bot is running fine on Railway!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", int(os.getenv("PORT", 8080)))
    await site.start()
    print("🌐 Web server started on port", os.getenv("PORT", 8080))

# 🔁 Keep-alive (ป้องกันบอทหลับ)
@tasks.loop(minutes=5)
async def keep_alive():
    try:
        async with ClientSession() as session:
            async with session.get("https://bot-mr-production.up.railway.app") as resp:
                print("🟢 Keep-alive status:", resp.status)
    except Exception as e:
        print(f"⚠️ เกิดข้อผิดพลาด keep-alive: {e}")

# 🚀 รันทั้ง web server และบอท
async def main():
    await start_web_server()
    await bot.start(TOKEN)

asyncio.run(main())
