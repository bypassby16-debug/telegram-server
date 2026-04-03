import requests
import os
import time
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# ----------- COLORS -----------
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"

colors = [RED, YELLOW, GREEN, CYAN, BLUE]

# ----------- LOGO -----------
def show_logo():
    os.system("clear")
    print(f"""{RED}
███╗   ███╗ █████╗ ███████╗██╗ █████╗ 
████╗ ████║██╔══██╗██╔════╝██║██╔══██╗
██╔████╔██║███████║█████╗  ██║███████║
██║╚██╔╝██║██╔══██║██╔══╝  ██║██╔══██║
██║ ╚═╝ ██║██║  ██║██║     ██║██║  ██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝
{RESET}
""")

# ----------- COLOR ANIMATION -----------
def color_animation():
    i = 0
    while True:
        color = colors[i % len(colors)]
        print(f"\r{color} >>> @M_a_F_i_a0000 MaFia TikTok Bot <<< {RESET}", end="")
        time.sleep(1)
        i += 1

# ----------- START COMMAND -----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📌 TikTok Username → Profile Pic\n"
        "📌 Video Link → HD Video\n"
        "📌 Photo Link → HD Photos\n"
        "📌 Story Link → (Try Download 🔥)"
    )

# ----------- MESSAGE HANDLER -----------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.strip()

    # ================= STORY (TRY) =================
    if "tiktok.com" in text and ("story" in text or "/stories/" in text):
        try:
            api = f"https://tikwm.com/api/?url={text}"
            res = requests.get(api).json()

            if res.get("code") != 0:
                await update.message.reply_text("❌ Story မရနိုင်ပါ (private ဖြစ်နိုင်)")
                return

            data = res["data"]

            # try video
            if "play" in data:
                await update.message.reply_video(data["play"], caption="📖 Story Video")
                return

            # try image
            if "images" in data:
                for img in data["images"]:
                    await update.message.reply_photo(img)
                return

            await update.message.reply_text("❌ Story မတွေ့ပါ")

        except:
            await update.message.reply_text("❌ Story Error")

        return

    # ================= VIDEO / PHOTO =================
    if "tiktok.com" in text:
        try:
            api = f"https://tikwm.com/api/?url={text}"
            res = requests.get(api).json()

            if res.get("code") != 0:
                await update.message.reply_text("❌ Download မရနိုင်ပါ")
                return

            data = res["data"]

            if "images" in data:
                photos = data["images"]
                await update.message.reply_text(f"📸 {len(photos)} Photos")

                for img in photos:
                    await update.message.reply_photo(img)
                return

            video_url = data["play"]

            caption = f"""
👁 {data.get("play_count",0)}
❤️ {data.get("digg_count",0)}
💬 {data.get("comment_count",0)}
🔁 {data.get("share_count",0)}
"""

            await update.message.reply_video(video_url, caption=caption)

        except:
            await update.message.reply_text("❌ Error")

    # ================= PROFILE =================
    else:
        username = text.replace("@", "")
        url = f"https://www.tiktok.com/@{username}"
        headers = {"User-Agent": "Mozilla/5.0"}

        try:
            response = requests.get(url, headers=headers)
            html = response.text

            start_index = html.find('"avatarLarger":"')
            if start_index == -1:
                await update.message.reply_text("Username မတွေ့ ❌")
                return

            start_index += len('"avatarLarger":"')
            end_index = html.find('"', start_index)

            profile_pic = html[start_index:end_index].replace("\\u002F", "/")

            await update.message.reply_photo(profile_pic)

        except:
            await update.message.reply_text("❌ Profile Error")

# ----------- MAIN -----------
if __name__ == "__main__":

    show_logo()

    t = threading.Thread(target=color_animation)
    t.daemon = True
    t.start()

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()