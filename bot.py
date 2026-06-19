import telebot
from groq import Groq

TELEGRAM_TOKEN = "8731539303:AAHxkl8WAoVLvS4YOI5vfAc9dtW6ocsiREI"
GROQ_API_KEY = "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"

client = Groq(api_key=GROQ_API_KEY)
bot = telebot.TeleBot(TELEGRAM_TOKEN)

SYSTEM_PROMPT = """Ты отвечаешь от имени живого человека в Telegram.
Пиши по-русски, неформально, как реальный человек.
Можешь материться. Используй смайлики. Будь краток и по делу."""

@bot.inline_handler(lambda query: True)
def inline_query(query):
    user_question = query.query.strip()
    if not user_question:
        return
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_question}
            ]
        )
        answer = response.choices[0].message.content
    except Exception as e:
        answer = f"Ошибка: {e}"

    result = telebot.types.InlineQueryResultArticle(
        id="1",
        title="Ответ AI",
        description=answer[:100],
        input_message_content=telebot.types.InputTextMessageContent(answer)
    )
    bot.answer_inline_query(query.id, [result], cache_time=0)

print("Бот запущен!")
bot.infinity_polling()
