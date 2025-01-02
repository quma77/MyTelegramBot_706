from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
import sqlite3
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler
import re


con = sqlite3.connect("baze_706.db")
cur = con.cursor()




ADMIN = 1093664497   
ADMIN_2 = 806552022
ADMIN_3 = 749427159
ADMIN_4 = 1053514876


cur.execute('''CREATE TABLE IF NOT EXISTS baze_706 (
    id INTEGER PRIMARY KEY,
    name TEXT,
    ek INTEGER,
    ekmk INTEGER,
    dis INTEGER,
    mp INTEGER
)''')
con.commit()

contacts = [
    (1093664497, 'Лисицын Святослав ADM', 0, 0, 0, 0),  
    (749427159, 'Грибанов Родион ADM', 0, 0, 0, 0),
    (1212927001, 'Гибадуллин Амир', 0, 0, 0, 0),
    (772425041, 'Яикбаев Даниил', 0, 0, 0, 0),
    (806552022, 'Мартынова Дарья ADM', 0, 0, 0, 0),
    (877798690, 'Гарипова Айзира', 0, 0, 0, 0),
    (1664532632, 'Файрушина Гульназ', 0, 0, 0, 0),
    (5080403377, 'Горбатова Индира', 0, 0, 0, 0),
    (1019777881, 'Тагирова Линиза', 0, 0, 0, 0),
    (5918430941, 'Тагиров Булат', 0, 0, 0, 0),
    (5694532778, 'Халитов Булат', 0, 0, 0, 0),
    (1419713368, 'Сабитова Ляйсан', 0, 0, 0, 0),
    (839739793, 'Галиева Ландыш', 0, 0, 0, 0),
    (1053514876, 'Галеев Вадим ADM', 0, 0, 0, 0),
    (1, 'Зимулюкина Надежда', 0, 0, 0, 0),
    (1, 'Жиганов Алексей', 0, 0, 0, 0),
    (1, 'Гилязов Наиль', 0, 0, 0, 0),
    (922068077, 'Салимгараева Милена', 0, 0, 0, 0),
    (5143322660, 'Козимжанова Румия', 0, 0, 0, 0),
    (1, 'Гарипов Тимур', 0, 0, 0, 0),
    (1, 'Сафина Рания', 0, 0, 0, 0),
    (1, 'Абделганиев Ильнар', 0, 0, 0, 0),
    (1, 'Пятибратов Артём', 0, 0, 0, 0),
    (1, 'Балаухина Ольга', 0, 0, 0, 0),
    (1, 'Глухова Юлия', 0, 0, 0, 0),
    (1, 'Яковлева Кристина', 0, 0, 0, 0),
    (1, 'Крюкова Кристина', 0, 0, 0, 0),
    
    
    
    
    

    
    
    
    

    
    



    
    
    
    

    
]

for contact in contacts:
    cur.execute('SELECT COUNT(*) FROM baze_706 WHERE id = ?', (contact[0],))
    exists = cur.fetchone()[0]
    if exists == 0:
        cur.execute('''
INSERT INTO baze_706 (id, name, ek, ekmk, dis, mp) VALUES (?, ?, ?, ?, ?, ?)
''', contact) # Используем cur.execute() для одной записи
        con.commit()
        
# Получить имя пользователя
def get_username(user_id):
    cur.execute("SELECT name FROM baze_706 WHERE id = ?", (user_id,))
    result = cur.fetchone()
    return result[0] if result else "Неизвестный пользователь"

# Проверить, существует ли пользователь в базе данных
def user_exists(user_id):
    cur.execute("SELECT id FROM baze_706 WHERE id = ?", (user_id,))
    return cur.fetchone() is not None

# Обновить данные в базе данных
def update_database(user_id, category, value):
    try:
        cur.execute(f"UPDATE baze_706 SET {category} = {category} + ? WHERE id = ?", (value, user_id))
        con.commit()
    except sqlite3.Error as e:
        print(f"Ошибка обновления базы данных: {e}")


# Начальная функция
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    if user_exists(user_id):
        #Админ
        if int(update.message.from_user.id) == ADMIN or ADMIN_2 or ADMIN_3:
            await update.message.reply_text(f'Приветствую, {get_username(user_id)}! Админ панель для тебя', reply_markup = ReplyKeyboardMarkup([['Режим продаж 💸'], ['Моя статистика 📋'], ['Открыть БД 📁'], ['Продажи 📊'], ['Отчет 📋'], ['❌ Отичстиь продажи ❌']]))   
        #Продавец
        else:
            await update.message.reply_text(f'Приветствую, {get_username(user_id)}!', reply_markup=ReplyKeyboardRemove())
            await update.message.reply_text('Жду твои продажи. За правилами использования, обратись к @qumaqq\nУспехов))',reply_markup = ReplyKeyboardMarkup([['Режим продаж 💸'], ['Моя статистика 📋']]))
            context.user_data['state'] = 'awaiting_number'
    else:
        await update.message.reply_text('К сожалению, ты не добавлен в нашу базу данных. Обратись к админу @qumaqq')

# Обработка состояния ожидания номера
async def process_number_state(update, context, text):
    try:
        number = int(text)
        reply_markup = ReplyKeyboardMarkup([[f'{number} ek', f'{number} ekmk'], [f'{number} dis', f'{number} mp'],  ['Отмена продажи']], resize_keyboard=True)
        await update.message.reply_text('Выбираем категорию:', reply_markup=reply_markup)
        context.user_data['number'] = number
        context.user_data['state'] = 'awaiting_category'
    except ValueError:
        await update.message.reply_text('Пожалуйста, введите целое число.')

# Обработка состояния ожидания категории
async def process_category_state(update, context, text):
    if text == 'Отмена продажи':
        if update.message.from_user.id == ADMIN or ADMIN_2 or ADMIN_3:
            await update.message.reply_text("Продажа отменена.", reply_markup = ReplyKeyboardMarkup([['Режим продаж 💸'], ['Моя статистика 📋'], ['Открыть БД 📁'], ['Продажи 📊'], ['Отчет 📋'], ['❌ Отичстиь продажи ❌']]))
            context.user_data.clear()  
            return 
        else:
            await update.message.reply_text("Продажа отменена.", reply_markup = ReplyKeyboardMarkup([['Режим продаж 💸'], ['Моя статистика 📋']]))
            context.user_data.clear()  
            return 
    else:
        try:
            number, category = parse_category(text)
            update_database(update.message.from_user.id, category, number)
            await update.message.reply_text(f"Добавлено {number} к {category}.", reply_markup=ReplyKeyboardRemove())
            await show_stats(update, context, category)
            context.user_data['state'] = 'awaiting_number'
        except ValueError:
            await update.message.reply_text("Некорректный ввод. Попробуйте еще раз.")

# Разбор категории и числа
def parse_category(text):
    parts = text.split()
    if len(parts) != 2:
        raise ValueError
    number = int(parts[0])
    category = parts[1].lower()
    if category not in ['ek', 'ekmk', 'dis', 'mp']:
        raise ValueError
    return number, category

# Показ статистики пользователя
async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE, category):
    cur.execute(f"SELECT {category} FROM baze_706 WHERE id = ?", (update.message.from_user.id,))
    stats = cur.fetchone()[0]
    context.user_data['state'] = 'awaiting_number'
    await update.message.reply_text(f"Твоя статистика по {category}: {stats}", reply_markup=ReplyKeyboardMarkup([["Выйти с режима продаж ◀️"]]))

    
# Обработка сообщений от продавцов
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    text2 = update.message.text.lower()
    if not user_exists(update.message.from_user.id):
        await update.message.reply_text("К сожалению, ты не добавлен в нашу базу данных. Обратись к админу @qumaqq")
        return
    if 'state' not in context.user_data: # Проверка состояния ВНЕ блока elif
        context.user_data['state'] = None # Изначально состояние не установлено
    if text == "Моя статистика 📋":
            context.user_data['state'] = None
            cur.execute("SELECT ek FROM baze_706 WHERE id = ?", (int(update.message.from_user.id),))
            ek_stut = cur.fetchone()[0]
            cur.execute("SELECT ekmk FROM baze_706 WHERE id = ?", (int(update.message.from_user.id),))
            ekmk_stut = cur.fetchone()[0]
            cur.execute("SELECT dis FROM baze_706 WHERE id = ?", (int(update.message.from_user.id),))
            dis_stut = cur.fetchone()[0]
            cur.execute("SELECT mp FROM baze_706 WHERE id = ?", (int(update.message.from_user.id),))
            mp_stut = cur.fetchone()[0]
            await update.message.reply_text(f'Твоя статистика выглядет так:\nЕК: {ek_stut}\nЕКМК: {ekmk_stut}\nDIS: {dis_stut}\nМП: {mp_stut}')
            
    elif text == "Режим продаж 💸":
        context.user_data['state'] = 'awaiting_number'
        await update.message.reply_text('Успешных продаж! хуесос)', reply_markup=ReplyKeyboardMarkup([["Выйти с режима продаж ◀️"]]))
    elif text == "Выйти с режима продаж ◀️":
        context.user_data['state'] = 'awaiting_category'
        if update.message.from_user.id == ADMIN or ADMIN_2 or ADMIN_3:
            await update.message.reply_text("Вы вышли из режима продаж.", reply_markup = ReplyKeyboardMarkup([['Режим продаж 💸'], ['Моя статистика 📋'], ['Открыть БД 📁'], ['Продажи 📊'], ['Отчет 📋'], ['❌ Отичстиь продажи ❌']]))
            context.user_data['state'] = None   
        else:
            await update.message.reply_text("Вы вышли из режима продаж.", reply_markup = ReplyKeyboardMarkup([['Режим продаж 💸'], ['Моя статистика 📋']]))
            context.user_data['state'] = None
    elif context.user_data.get('state') == 'awaiting_number':
        try:
            number = int(text)
            await process_number_state(update, context, number) # Передаем число в process_number_state
        except ValueError:
            await update.message.reply_text('Пожалуйста, введите целое число.')
    elif context.user_data.get('state') == 'awaiting_category':
        await process_category_state(update, context, text)
    elif text == "Открыть БД 📁":
        if int(update.message.from_user.id) == ADMIN or ADMIN_2 or ADMIN_3:
            cur.execute("SELECT * FROM baze_706")
            rows = cur.fetchall()
            for row in rows:
                await update.message.reply_text(f"{row[1]}: ЕК|ЕКМК|ДИС|МП: {row[2:]}")
        else:
            await update.message.reply_text('Не выйдет)')
    elif text == "Продажи 📊":
        context.user_data['state'] = None
        if int(update.message.from_user.id) == ADMIN or ADMIN_2 or ADMIN_3:
            cur.execute("SELECT * FROM baze_706 WHERE ek > 0 OR ekmk > 0 OR dis > 0 OR mp > 0 ")
            rows = cur.fetchall()
            for row in rows:
                await update.message.reply_text(f"{row[1]}: ЕК|ЕКМК|ДИС|МП: {row[2:]}")
            
            cur.execute("SELECT SUM(ek) FROM baze_706")
            total_ek = cur.fetchone()[0]
            cur.execute("SELECT SUM(ekmk) FROM baze_706")
            total_ekmk = cur.fetchone()[0]
            cur.execute("SELECT SUM(dis) FROM baze_706")
            total_dis = cur.fetchone()[0]
            cur.execute("SELECT SUM(mp) FROM baze_706")
            total_mp = cur.fetchone()[0]
            
            cur.execute("SELECT SUM(ek) FROM baze_706") 
            sum_ek = cur.fetchone()[0]
            cur.execute("SELECT SUM(ekmk) FROM baze_706") 
            sum_ekmk = cur.fetchone()[0]
            cur.execute("SELECT SUM(dis) FROM baze_706") 
            sum_dis = cur.fetchone()[0]
            sum_sell = sum_ek + sum_ekmk + sum_dis
            
            
            
            await update.message.reply_text(f"ЕК: {total_ek}\nЕКМК: {total_ekmk}\nDIS: {total_dis}\nМП: {total_mp}\nВсего ЕК/ЕКМК/Dis: {sum_sell}")
        else:
            await update.message.reply_text('Не выйдет)')
    elif text == "❌ Отичстиь продажи ❌":
        if int(update.message.from_user.id) == ADMIN or ADMIN_2 or ADMIN_3:
            cur.execute("SELECT * FROM baze_706  WHERE ek > 0 OR ekmk > 0 OR dis > 0 OR mp > 0 ")
            rows = cur.fetchall()
            for row in rows:
                await update.message.reply_text(f"{row[1]}: ЕК|ЕКМК|ДИС|МП: {row[2:]}")
            await update.message.reply_text('Удаляю)')
            cur.execute('UPDATE baze_706 SET ek = 0, ekmk = 0, dis = 0, mp = 0;')
            con.commit()
        else:
            await update.message.reply_text('Не выйдет)')
    elif text == "Отчет 📋":
        await update.message.reply_text('Напиши оборот, upt, сбп, и сумму оплаты по картам через пробел. Пример (12000 2.23 3000 8000)')

        
      
    if re.match(r"^отчет", text2): 
        match = re.search(r"отчет\s+(\d+(\.\d+)?)\s+(\d+(\.\d+)?)\s+(\d+(\.\d+)?)\s+(\d+(\.\d+)?)", text, re.IGNORECASE)
        
        cur.execute("SELECT SUM(ek) FROM baze_706") 
        sum_ek = cur.fetchone()[0]
        cur.execute("SELECT SUM(ekmk) FROM baze_706") 
        sum_ekmk = cur.fetchone()[0]
        cur.execute("SELECT SUM(dis) FROM baze_706") 
        sum_dis = cur.fetchone()[0]
        sum_sell = sum_ek + sum_ekmk + sum_dis
        cur.execute("SELECT SUM(mp) FROM baze_706") 
        sum_mp = cur.fetchone()[0]
        
        if match:
            try:
                num1 = float(match.group(1))
                num2 = float(match.group(3))
                num3 = float(match.group(5))
                num4 = float(match.group(7))
                await update.message.reply_text(f'706\n{num2}\nЕК: {int(sum_sell/num1*100)}% {int(sum_sell)}/{int(num1)}\nCБП: {int(num3/num4*100)}%\nМП: {sum_mp}')


            except ValueError:
                await update.message.reply_text("Ошибка: Не все элементы являются числами.")


    
# Основная функция
def main() -> None:
    application = ApplicationBuilder().token('7373924398:AAH43oT7Cu-WY_Dt8emZhzg18NTYcs3qk_g').build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()
    
          

if __name__ == '__main__':
    main()






































