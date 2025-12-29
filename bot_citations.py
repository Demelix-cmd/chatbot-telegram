import google.generativeai as genai
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# 🔑 Configure Gemini API
genai.configure(api_key="AIzaSyBIFBnYuT6VKEmWjUN6N-iSnG1RrjPPPzE")

# Modèle IA à utiliser (Gemini Pro)
model = genai.GenerativeModel("models/gemini-1.5-flash")

async def start(update, context):
    await update.message.reply_text("Salut 👋! Je suis ton bot IA cree par demetech")

async def chat(update, context):
    user_message = update.message.text
    chat_type = update.message.chat.type

    # Si on est dans un groupe
    if chat_type in ["group", "supergroup"]:
        bot_username = (await context.bot.get_me()).username

        # Vérifier si le bot est mentionné
        mentioned = f"@{bot_username}" in user_message

        # Vérifier si le message ressemble à une questionN
        is_question = user_message.strip().endswith("?")

        # Si ni mention ni question → ignorer
        if not mentioned and not is_question:
            return

        # Retirer la mention pour l'IA
        user_message = user_message.replace(f"@{bot_username}", "").strip()
        user_name = update.message.from_user.first_name
        prefix = f"@{user_name} "
    else:
        # En privé : répondre à tout
        prefix = ""

    try:
        response = model.generate_content(user_message)
        await update.message.reply_text(prefix + response.text)
    except Exception as e:
        await update.message.reply_text("⚠️ Oups, je n’ai pas pu répondre.")
        print("Erreur API:", e)

def main():
    app = Application.builder().token("6770589511:AAFRzLsnv4bqtdB-KmUi8N8ELxWZQNLgedM").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("🤖 Bot demetech en ligne *L2I* ....")
    app.run_polling()

if __name__ == "__main__":
    main()



