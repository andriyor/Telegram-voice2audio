import os

import telebot
import ffmpeg
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
bot = telebot.TeleBot(os.environ.get('TELEGRAM_TOKEN'))


@bot.message_handler(content_types='audio')
def handle_audio(message):
    file_info = bot.get_file(message.audio.file_id)
    file = bot.download_file(file_info.file_path)

    with open(file_info.file_path, 'wb') as f:
        f.write(file)

    audio = open(file_info.file_path, 'rb')
    bot.send_voice(message.chat.id, audio)


@bot.message_handler(content_types='voice')
def handle_voice(message):
    file_info = bot.get_file(message.voice.file_id)
    file = bot.download_file(file_info.file_path)

    with open(file_info.file_path, 'wb') as f:
        f.write(file)

    mp3_file_path = file_info.file_path.replace('oga', 'mp3')
    ffmpeg.input(file_info.file_path).output(mp3_file_path).run()

    audio = open(mp3_file_path, 'rb')
    bot.send_audio(message.chat.id, audio)


if __name__ == '__main__':
    bot.polling(none_stop=True)
