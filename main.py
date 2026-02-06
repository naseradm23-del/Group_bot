import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
from youtubesearchpython import VideosSearch

# احصل على BOT_TOKEN من Secrets
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # إذا بدأ النص بـ "نوسا"
    if text.startswith("نوسا"):
        query = text.replace("نوسا", "").strip()
        
        if not query:
            await update.message.reply_text("اكتب اسم الأغنية بعد كلمة نوسا")
            return
        
        # البحث على يوتيوب
        videosSearch = VideosSearch(query, limit=1)
        result = videosSearch.result()

        if result["result"]:
            title = result["result"][0]["title"]
            link = result["result"][0]["link"]

            await update.message.reply_text(f"وجدت لك:\n{title}\n{link}")
        else:
            await update.message.reply_text("ما لقيت نتيجة")

# إنشاء التطبيق
app = ApplicationBuilder().token(BOT_TOKEN).build()

# إضافة الهاندلر للرسائل
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# تشغيل البوت
app.run_polling()