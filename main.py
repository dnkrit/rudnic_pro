import telebot
from telebot import types

TOKEN = 'Место для токена'
bot = telebot.TeleBot(TOKEN)

USER_STATE = {}

def get_user_state(message):
    return USER_STATE.get(message.chat.id)

def update_user_state(message, state):
    USER_STATE[message.chat.id] = state

PRODUCTS = ['Кредит', 'Гарантия', 'Факторинг', 'Лизинг']

# Обработка команды start
@bot.message_handler(commands=['start'])
def send_start(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for product in PRODUCTS:
        markup.add(product)
    bot.reply_to(message, 'Выберите финансовый продукт: Кредит, Гарантия, Факторинг, Лизинг', reply_markup=markup)
    update_user_state(message, 'CHOOSE_PRODUCT')

@bot.message_handler(func=lambda message: get_user_state(message) == 'CHOOSE_PRODUCT')
def product_choice(message):
    chosen_product = message.text
    if chosen_product in PRODUCTS:
        update_user_state(message, 'ENTER_AMOUNT')
        bot.reply_to(message, 'Введите сумму в рублях:')
    else:
        bot.reply_to(message, 'Пожалуйста, выберите продукт из списка.')

@bot.message_handler(func=lambda message: get_user_state(message) == 'ENTER_AMOUNT')
def amount_entered(message):
    # Здесь должна быть проверка на корректность введенной суммы
    update_user_state(message, 'ENTER_TERM')
    bot.reply_to(message, 'Введите срок в месяцах:')

@bot.message_handler(func=lambda message: get_user_state(message) == 'ENTER_TERM')
def term_entered(message):
    # Здесь также может быть проверка данных
    update_user_state(message, 'ENTER_INN_IKZ')
    bot.reply_to(message, 'Введите ИНН организации:')

@bot.message_handler(func=lambda message: get_user_state(message) == 'ENTER_INN_IKZ')
def inn_ikz_entered(message):
    update_user_state(message, None)  # Сбрасываем состояние пользователя
    bot.reply_to(message, 'Мы приступили к добыче ресурсов!')

# Обработка непредвиденных сообщений
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Извините, я не понимаю эту команду.")

# Запуск бота
bot.infinity_polling()