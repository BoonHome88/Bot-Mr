import os
import nextcord as discord
from nextcord.ext import commands, tasks
import asyncio
from aiohttp import web, ClientSession

# โหลด TOKEN จาก Railway Environment
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
     "htpay": (
        """# วิธีโดเนท Midnight Racing
>>> แอพ MRP SHOP จะอยู่ในมือถือในเกมส์ของผู้เล่นทุกท่าน""",
        "https://img2.pic.in.th/pic/HOW_TO_DONATE.png"
    ),
    "dncar": (
        """# รายการโดเนทรถ

ร้านค้ารถทั่วไป  : https://discord.com/channels/980035347264208906/1325752244079169606

ร้านค้ารถแรร์ : https://discord.com/channels/980035347264208906/1297059148340662332

ร้านค้ามอไซค์ : https://discord.com/channels/980035347264208906/1338224394551431250

แพ็ครถเริ่มต้น : https://discord.com/channels/980035347264208906/1283822453478396026

รถในร้านค้า IC ทุกคันสามารถแคปรูปมาเพื่อสอบถามราคา OC ได้เลยนะครับ""",
        "https://img5.pic.in.th/file/secure-sv1/openserver86e25af469a50025.png"
    ),
    "deldt": (
        """# สำหรับผู้เล่นที่มีอาการที่คาดว่าแปลกไปจากเดิม ให้ทำการลบแคชและข้อมูลดังนี้

**ตรวจเช็คไดร์เวอร์การ์ดจอให้เป็นเวอร์ชั่นล่าสุด**

ขั้นตอนแรก เข้าไปที่ FiveM Application Data (หอยทากสีเขียว)
ให้ลบทั้ง 3 โฟลเดอร์นี้
- citizen
- crashes
- data

ขั้นตอนที่สอง กดปุ่ม Win + R พิมพ์ appdata กด ok เข้าโฟลเดอร์ Roaming 
ให้ลบโฟลเดอร์ CitizenFX 

เสร็จทั้งหมดแล้วให้เข้า FiveM ใหม่ เข้าเซิฟผ่าน IP https://discordapp.com/channels/980035347264208906/985455390013685800
""",
        "-"
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
KEEP_ALIVE_URL = "https://worker-mr-bottt.up.railway.app"  # แก้ให้ตรงกับ Domain ของคุณ

@tasks.loop(minutes=5)
async def keep_alive():
    try:
        async with ClientSession() as session:
            async with session.get(KEEP_ALIVE_URL) as resp:
                print("🟢 Keep-alive status:", resp.status)
    except Exception as e:
        print(f"⚠️ เกิดข้อผิดพลาด keep-alive: {e}")

# 🔁 ระบบ Auto Reconnect / Restart เมื่อเกิด error
async def run_bot():
    while True:
        try:
            print("🚀 กำลังเริ่มต้น Discord Bot...")
            await bot.start(TOKEN)
        except Exception as e:
            print(f"❌ บอทเกิดข้อผิดพลาด: {e}")
            print("🔁 กำลังรีสตาร์ทบอทใหม่ใน 10 วินาที...")
            await asyncio.sleep(10)  # หน่วงเวลา 10 วินาทีก่อนลองใหม่

# 🚀 รันทั้ง web server และบอทพร้อมระบบ reconnect
async def main():
    await start_web_server()
    await run_bot()

asyncio.run(main())
