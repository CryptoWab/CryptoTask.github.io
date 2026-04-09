import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# --- CONFIGURATION ---
# Naya token yahan dalein (Purana wala revoke karne ke baad)
TOKEN = '8454471111:AAFDj7cFfA2cUeBDRzkEZ0H0naEAKy7qj-Q'

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Dummy Database (Asli project ke liye SQL ya MongoDB use karein)
user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in user_data:
        user_data[user_id] = {'balance': 0, 'referrals': 0}
    
    keyboard = [
        [InlineKeyboardButton("💰 Balance", callback_data='balance'),
         InlineKeyboardButton("🎁 Daily Bonus", callback_data='bonus')],
        [InlineKeyboardButton("👥 Refer & Earn", callback_data='refer')],
        [InlineKeyboardButton("🔓 Unlock Link (Earn)", url='https://your-github-pages-link.com')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"👋 Welcome {update.effective_user.first_name}!\n\n"
        "Ye ek advanced earning bot hai. Aap niche diye gaye buttons se paise kama sakte hain.",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == 'balance':
        bal = user_data[user_id]['balance']
        await query.edit_message_text(f"Your Current Balance: {bal} Points")
    
    elif query.data == 'bonus':
        user_data[user_id]['balance'] += 10
        await query.edit_message_text("✅ 10 Points added to your balance!")

    elif query.data == 'refer':
        link = f"https://t.me/{(await context.bot.get_me()).username}?start={user_id}"
        await query.edit_message_text(f"Per Referral: 50 Points\n\nYour Invite Link:\n{link}")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("Bot is running...")
    application.run_polling()
      
