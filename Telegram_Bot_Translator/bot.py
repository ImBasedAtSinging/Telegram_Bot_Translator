import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import BOT_TOKEN
from translate_service import TextAnalysis  

bot = telebot.TeleBot(BOT_TOKEN)


def gen_markup_for_text():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(
        InlineKeyboardButton('Get an answer', callback_data='text_ans'),
        InlineKeyboardButton('Translate the message', callback_data='text_translate')
    )
    return markup


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    username = call.from_user.username

    if username in TextAnalysis.memory and TextAnalysis.memory[username]:
        obj = TextAnalysis.memory[username][-1]

        if call.data == "text_ans":
            bot.send_message(call.message.chat.id, obj.response)
        elif call.data == "text_translate":
            bot.send_message(call.message.chat.id, obj.translation)
    else:
        bot.send_message(call.message.chat.id, "No data found. Please send a message first.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if not message.text:
        bot.send_message(message.chat.id, "Sorry, I didn't understand you. Please, type something.")
        return

    username = message.from_user.username

    bot.send_chat_action(message.chat.id, 'typing')

    obj = TextAnalysis(message.text, username)

    if username not in TextAnalysis.memory:
        TextAnalysis.memory[username] = []

    TextAnalysis.memory[username].append(obj)

    bot.send_message(message.chat.id, "I've got your message! What do you want to do with it?", reply_markup=gen_markup_for_text())

if __name__ == "__main__":
    bot.infinity_polling(none_stop=True)