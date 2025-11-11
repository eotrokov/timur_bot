import logging
import asyncio
import re
import os
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Состояния бота
DAY1, DAY2, DAY3, DAY4, DAY5 = range(5)

# Хранилище состояния пользователей
user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user_id = update.effective_user.id

    # Отправляем приветствие в стиле Стругацких
    await update.message.reply_text(
        "🛸 Подключение к каналу Лаборатории Изучения Пограничных Состояний...\n\n"
        "Кандидат, ты был избран для подготовки к экспедиции.\n"
        "5 дней испытаний, 5 шагов к допуску в Аномальную Зону.\n\n"
        "Твои блястящие знания, острый ум и внимательность будут\n"
        "проверены в условиях, приближенных к реальным\n"
        "аномалиям Зоны.\n\n"
        "⚠️ **Важное правило:** Каждый новый день активируется\n"
        "командой 'готов'. Напиши это слово, когда будешь готов\n"
        "получить задание дня.\n\n"
        "Система ждет твоего решения."
    )

    # Пауза для драматизма
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action='typing'
    )
    await asyncio.sleep(3)

    # Инициализация состояния пользователя
    user_states[user_id] = {
        'day': DAY1,
        'name': update.effective_user.first_name,
        'task_active': True
    }
    await asyncio.sleep(30)
    # Начало первого задания
    await update.message.reply_text(
        "Зафиксирован запуск системы. Подключение к каналу установлено. "
        "Голосовая связь отсутствует, работаю в текстовом режиме.\n\n"
        "Кандидат, для начала подготовки необходимо найти \"Нулевой Объект\". "
        "Координаты в формате (X, Y), где X — количество клавиш, Y — количество ног.\n\n"
        "Введите координаты:"
    )

    return DAY1

async def handle_day1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ответа для Дня 1"""
    user_id = update.effective_user.id

    if user_id not in user_states or not user_states[user_id].get('task_active', False):
        user_input = update.message.text.strip().lower()
        if user_input == 'готов':
            user_states[user_id]['task_active'] = True
            await update.message.reply_text(
                "Кандидат, для начала подготовки необходимо найти \"Нулевой Объект\". "
                "Координаты в формате (X, Y), где X — количество клавиш, Y — количество ног.\n\n"
                "Введите координаты:"
            )
        else:
            await update.message.reply_text("Для получения задания дня 1 введите 'готов'")
        return DAY1

    user_input = update.message.text.strip()

    patterns = [
        r'\(?\s*104\s*[,.\s]\s*0\s*\)?',
        r'104\s*[,.\s]\s*0',
        r'сто\s*четыре\s*[,.\s]\s*ноль',
        r'клавиатура'
    ]

    is_correct = any(re.search(pattern, user_input.lower()) for pattern in patterns)

    if is_correct:
        user_states[user_id]['day'] = DAY2
        user_states[user_id]['task_active'] = False

        await update.message.reply_text(
            "✅ Координаты подтверждены. Объект \"Клавиатура\" идентифицирован. "
            "Ты прошел тест на наблюдательность.\n\n"
            "Для получения следующего задания напиши 'готов', когда будешь готов."
        )
        return DAY2
    else:
        await update.message.reply_text(
            "❌ Координаты не распознаны. Совет: объект находится в зоне твоего прямого доступа "
            "и используется для ввода данных. Перепроверь подсчет элементов.\n\n"
            "Введите координаты в формате (X, Y) или X Y:"
        )
        return DAY1

async def handle_day2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ответа для Дня 2"""
    user_id = update.effective_user.id

    if user_id not in user_states:
        await update.message.reply_text("Начни квест с команды /start")
        return ConversationHandler.END

    if not user_states[user_id].get('task_active', False):
        user_input = update.message.text.strip().lower()
        if user_input == 'готов':
            user_states[user_id]['task_active'] = True
            await update.message.reply_text(
                "Кандидат. Видимый спектр — лишь малая часть информации. Истина часто скрыта в невидимом. "
                "Мы зашифровали сообщение в ультрафиолетовом диапазоне.\n\n"
                "Введите код:"
            )
        else:
            await update.message.reply_text("Для получения задания дня 2 введите 'готов'")
        return DAY2

    user_input = update.message.text.strip().upper()

    if user_input in ['INVERSE', 'ИНВЕРСЕ', 'ОБРАТНЫЙ']:
        user_states[user_id]['day'] = DAY3
        user_states[user_id]['task_active'] = False

        await update.message.reply_text(
            "✅ Код \"Обратный\" принят. Ты нашел скрытый канал информации.\n\n"
            "Для получения следующего задания напиши 'готов', когда будешь готов к испытанию."
        )
        return DAY3
    else:
        await update.message.reply_text(
            "❌ Код неверен. Совет: обрати внимание на плафоны основных светильников. "
            "Буквы должны образовать слово на английском языке.\n\n"
            "Введите код:"
        )
        return DAY2

async def handle_day3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ответа для Дня 3"""
    user_id = update.effective_user.id

    if user_id not in user_states:
        await update.message.reply_text("Начни квест с команды /start")
        return ConversationHandler.END

    if not user_states[user_id].get('task_active', False):
        user_input = update.message.text.strip().lower()
        if user_input == 'готов':
            user_states[user_id]['task_active'] = True
            await update.message.reply_text(
                "Кандидат. Иногда путь к решению лежит через изоляцию переменной. "
                "Задача скрыта в \"Запретной Зоне\".\n\n"
                "Когда найдешь шифр, введи числовой ответ:"
            )
        else:
            await update.message.reply_text("Для получения задания дня 3 введите 'готов'")
        return DAY3

    user_input = update.message.text.strip()

    try:
        answer = int(user_input)
        if answer == 32:
            user_states[user_id]['day'] = DAY4
            user_states[user_id]['task_active'] = False

            await update.message.reply_text(
                "✅ Ключ 32 принят. Ты справился с пространственным парадоксом!\n\n"
                "Книга «Маятник Культуры» — это карта будущих открытий, найди её на подоконнике. "
                "Для получения следующего задания напиши 'готов', когда будешь готов."
            )
            return DAY4
        else:
            await update.message.reply_text(
                "❌ Ответ неверен. Совет: используй метод последовательного исключения переменных. "
                "Проверь вычисления для f(4).\n\n"
                "Введите числовой ответ:"
            )
            return DAY3
    except ValueError:
        await update.message.reply_text(
            "❌ Не понимаю ответ. Введи только числовое значение.\n\n"
            "Введите числовой ответ из шифра Прогрессора:"
        )
        return DAY3

async def handle_day4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ответа для Дня 4"""
    user_id = update.effective_user.id

    if user_id not in user_states:
        await update.message.reply_text("Начни квест с команды /start")
        return ConversationHandler.END

    if not user_states[user_id].get('task_active', False):
        user_input = update.message.text.strip().lower()
        if user_input == 'готов':
            user_states[user_id]['task_active'] = True
            await update.message.reply_text(
                "Кандидат. Большой Айзек запросил прямой контакт. Декодируй сообщение:\n\n"
                "`Uryyb, Jbeyq!`\n\n"
                "Этот шифр похож на те, что используют для маркировки аномальных зон.\n\n"
                "Введи расшифрованную фразу:"
            )
        else:
            await update.message.reply_text("Для получения задания дня 4 введите 'готов'")
        return DAY4

    user_input = update.message.text.strip()

    correct_answers = [
        'Hello, World!', 'hello world', 'HELLO WORLD',
        'Hello World', 'Привет, мир!', 'привет мир'
    ]

    if user_input in correct_answers:
        user_states[user_id]['day'] = DAY5
        user_states[user_id]['task_active'] = False

        await update.message.reply_text(
            "✅ Пропуск принят. Большой Айзек подтвердил твой статус. Носи униформу с честью.\n\n"
            "Для получения финального задания напиши 'готов', когда будешь готов к экспедиции."
        )
        return DAY5
    else:
        await update.message.reply_text(
            "❌ Фраза не распознана. Совет: это шифр Цезаря со сдвигом 13 (ROT13).\n\n"
            "Введите расшифрованную фразу:"
        )
        return DAY4

async def handle_day5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка ответа для Дня 5 - ФИНАЛ С ЭКСКУРСИЕЙ В ФОРТ"""
    user_id = update.effective_user.id

    if user_id not in user_states:
        await update.message.reply_text("Начни квест с команды /start")
        return ConversationHandler.END

    if not user_states[user_id].get('task_active', False):
        user_input = update.message.text.strip().lower()
        if user_input == 'готов':
            user_states[user_id]['task_active'] = True
            await update.message.reply_text(
                "Кандидат. Миссия подходит к концу. Ты прошел проверку! "
                "Помни, что главное качество "
                "Прогрессора — синтез. Он видит целое, там, где другие видят "
                "разрозненные части.\n\n"
                "Введи финальный код:"
            )
        else:
            await update.message.reply_text("Для получения финального задания введите 'готов'")
        return DAY5

    user_input = update.message.text.strip().upper()

    correct_answers = ['ЗОНА', 'ZONA', 'ZONE']

    if user_input in correct_answers:
        user_name = user_states[user_id]['name']

        # НОВЫЙ ФИНАЛ С ЭКСКУРСИЕЙ В ФОРТ
        await update.message.reply_text(
            "✅ Код 'ЗОНА' принят. Все системы доступа разблокированы.\n\n"
            "Поздравляю с завершением подготовки, Сотрудник. "
            "Твоя экспедиция в аномальную зону назначена на..."
        )

        # Драматическая пауза
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        await asyncio.sleep(3)

        await update.message.reply_text(
            "🕵️ *ВНИМАНИЕ! Обнаружено внешнее вмешательство в протокол!*\n\n"
            "Похоже, кто-то из 'высших сфер' уже рассекретил локацию твоей экспедиции...\n"
            "Система фиксирует утечку информации категории 'День Рождения'..."
        )

        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        await asyncio.sleep(2)

        await update.message.reply_text(
            "😄 **СЮРПРИЗ РАСКРЫТ!**\n\n"
            "Да, мы знаем, что ты уже в курсе про ночную экскурсию в форт. "
            "Наши 'источники' сообщили, что этот секрет хуже хранится, чем архивы КГБ!\n\n"
            "Но знаешь что? Это даже лучше!"
        )

        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        await asyncio.sleep(2)

        await update.message.reply_text(
            "🎭 *Переходим к протоколу 'Ирония Судьбы':*\n\n"
            "Вместо того чтобы делать вид, что это сюрприз...\n\n"
            "Мы официально подтверждаем, что твоя экспедиция в аномальную зону 'Форт' "
            "состоится в назначенный срок!\n\n"
            "И знаешь почему это гениально?"
        )

        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        await asyncio.sleep(2)

        await update.message.reply_text(
            "🔮 **Потому что теперь ты можешь:**\n"
            "• Осознанно готовиться к экспедиции\n"
            "• Изучать карты локации заранее\n"
            "• Разрабатывать теории об аномалиях\n"
            "• Наслаждаться предвкушением как настоящий учёный!\n\n"
            "Разве не это главная радость любого исследования?"
        )

        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action='typing')
        await asyncio.sleep(2)

        await update.message.reply_text(
            f"С Днём Рождения, {user_name}! Желаю тебе самых невероятных открытий "
            "в этой и многих будущих экспедициях!\n\n"
            "Конец связи... или только начало? 🗝️"
        )

        # Очищаем состояние пользователя
        del user_states[user_id]
        return ConversationHandler.END
    else:
        await update.message.reply_text(
            "❌ Код неверен. Совет: проверь все 4 записки под воздействием тепла. "
            "Символы должны образовать слово из 4 букв.\n\n"
            "Введите финальный код:"
        )
        return DAY5

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /help"""
    user_id = update.effective_user.id

    if user_id in user_states:
        current_day = user_states[user_id]['day']
        day_descriptions = {
            DAY1: "Найти Нулевой Объект по координатам",
            DAY2: "Расшифровать УФ-сообщение",
            DAY3: "Решить математический шифр",
            DAY4: "Декодировать сообщение ROT13",
            DAY5: "Найти финальный код на записках"
        }

        task_status = "активно" if user_states[user_id].get('task_active', False) else "неактивно"

        state = "Продолжайте выполнение задания" if user_states[user_id].get('task_active', False) else 'Для активации задания введите \"готов\"'

        await update.message.reply_text(f"📊 Статус подготовки:\nТекущий день: {current_day + 1}\nЗадание: {day_descriptions.get(current_day, 'Неизвестно')}\nСтатус задания: {task_status}\n\n{state}\nДля связи с куратором обратись к своему Проводнику.")
    else:
        await update.message.reply_text(
            "🛸 Лаборатория Изучения Пограничных Состояний\n\n"
            "Для начала подготовки к экспедиции используй команду /start\n\n"
            "5 дней испытаний отделяют тебя от допуска в Аномальную Зону.\n"
            "⚠️ Каждый день активируется командой 'готов'."
        )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик отмены"""
    user_id = update.effective_user.id
    if user_id in user_states:
        del user_states[user_id]

    await update.message.reply_text(
        "❌ Подготовка прервана. Статус: КАНДИДАТ ОТЧИСЛЕН.\n\n"
        "Для возобновления используй /start"
    )
    return ConversationHandler.END

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик голосовых сообщений"""
    await update.message.reply_text(
        "🎙️ Голосовая связь недоступна. Работаю в текстовом режиме.\n\n"
        "Используй текстовый ввод для прохождения подготовки."
    )

async def handle_unexpected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик непредусмотренных сообщений"""
    user_id = update.effective_user.id

    if user_id in user_states:
        current_day = user_states[user_id]['day']
        task_active = user_states[user_id].get('task_active', False)

        if not task_active:
            await update.message.reply_text("Для получения задания дня введите 'готов'")
            return current_day
        else:
            prompts = {
                DAY1: "Введите координаты в формате (X, Y):",
                DAY2: "Введите найденный код:",
                DAY3: "Введите числовой ответ:",
                DAY4: "Введите расшифрованную фразу:",
                DAY5: "Введите финальный код:"
            }

            await update.message.reply_text(
                f"❌ Не понимаю запрос. {prompts.get(current_day, 'Продолжайте выполнение задания.')}"
            )
            return current_day
    else:
        await update.message.reply_text(
            "🛸 Для начала подготовки в Лабораторию Изучения Пограничных Состояний используй команду /start"
        )
        return ConversationHandler.END

async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для проверки статуса"""
    user_id = update.effective_user.id

    if user_id in user_states:
        current_day = user_states[user_id]['day']
        task_active = user_states[user_id].get('task_active', False)

        day_names = {
            DAY1: "День 1: Пробуждение",
            DAY2: "День 2: Физика",
            DAY3: "День 3: Математика",
            DAY4: "День 4: Информатика",
            DAY5: "День 5: Синтез"
        }

        status = "активно" if task_active else "неактивно"
        state = "Продолжайте выполнение задания" if task_active else 'Для активации задания введите \"готов\"'
        await update.message.reply_text(f"📊 Статус подготовки:\nТекущий этап: {day_names.get(current_day, 'Неизвестно')}\nЗадание: {status}\n\n{state}")
    else:
        await update.message.reply_text("Подготовка не начата. Используй /start для начала квеста.")

async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда для сброса прогресса"""
    user_id = update.effective_user.id
    if user_id in user_states:
        del user_states[user_id]

    await update.message.reply_text("🔄 Прогресс сброшен. Для начала новой подготовки используй /start")
    return ConversationHandler.END

def main():
    """Основная функция запуска бота"""
    TOKEN = os.getenv("TELEGRAM_TOKEN")

    application = Application.builder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            DAY1: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_day1)],
            DAY2: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_day2)],
            DAY3: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_day3)],
            DAY4: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_day4)],
            DAY5: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_day5)],
        },
        fallbacks=[
            CommandHandler('cancel', cancel),
            CommandHandler('help', help_command),
            CommandHandler('status', status_command),
            CommandHandler('reset', reset_command),
            MessageHandler(filters.VOICE, handle_voice),
            MessageHandler(filters.ALL, handle_unexpected)
        ],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('help', help_command))
    application.add_handler(CommandHandler('status', status_command))
    application.add_handler(CommandHandler('reset', reset_command))
    application.add_handler(CommandHandler('cancel', cancel))
    application.add_handler(MessageHandler(filters.VOICE, handle_voice))

    print("🤖 Бот 'ИНИ-Инициация' запущен...")
    print("⏳ Ожидание подключения кандидатов...")
    print("🔗 Токен бота активирован")

    application.run_polling()

if __name__ == '__main__':
    main()
