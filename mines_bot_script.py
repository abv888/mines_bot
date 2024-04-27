import asyncio
import telebot.async_telebot as telebot
from sqlalchemy import update, select
from telebot import types
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

from database.engine import drop_db, create_db, session_maker
from database.models import User


bot = telebot.AsyncTeleBot(token=os.getenv("BOT_TOKEN"))
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL")
ADMIN_1 = os.getenv("ADMIN_USERNAME_1")
ADMIN_2 = os.getenv("ADMIN_USERNAME_2")

async def is_subscriber(channel_id, user_id):
    try:
        subscription = await bot.get_chat_member(channel_id, user_id)
        if subscription.status in ['member', 'administrator', 'creator']:
            return True
        else:
            return False
    except Exception as e:
        print("Error:", e)
        return False

@bot.message_handler(commands=['start'])
async def start(message):
    async with session_maker() as session:
        user_find = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
        if user_find.scalar_one_or_none() is None:
            user = User(username=message.from_user.username, telegram_id=message.from_user.id, full_name=message.from_user.full_name, casino_id=None)
            session.add(user)
            await session.commit()
    keyboardmain = types.InlineKeyboardMarkup(row_width=1)
    subscribe_button = types.InlineKeyboardButton(text="Se inscrever", url="https://t.me/+FkoAO1FBlEJlYWUy")
    check_button = types.InlineKeyboardButton(text="Conferir", callback_data="check_subscription")
    keyboardmain.add(subscribe_button, check_button)
    await bot.send_message(message.chat.id, f"Bem-vindo, {message.from_user.full_name}! \n\nPara usar o bot - inscreva-se em nosso canal🤝", reply_markup=keyboardmain)

@bot.callback_query_handler(func=lambda call:True)
async def callback_inline(call):
    if call.data == "check_subscription":
        # Здесь ваш код для проверки подписки пользователя на канал
        # После проверки отправляем сообщение с результатом
        if await is_subscriber(channel_id=TARGET_CHANNEL,
                         user_id=call.message.chat.id
                         ):
            call.data = "subscriber"
        else:
            await bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Você não está inscrito no canal")
            await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)

    if call.data == "subscriber":
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        register_button = types.InlineKeyboardButton(text="📱 Inscrição", callback_data="registration")
        instruction_button = types.InlineKeyboardButton(text="📚 Instruções", callback_data="instruction")
        get_signal_button = types.InlineKeyboardButton(text="💣 Receba um sinal 💣", callback_data="get_signal")
        keyboard.add(register_button, instruction_button, get_signal_button)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        await bot.send_message(chat_id=call.message.chat.id, text="Bem-vindo ao 🔸MINES BitsGap V3.0🔸!\n"
                                                            "💣Mines é um jogo de azar da casa de apostas 1win, baseado no clássico Campo Minado.\n"
                                                            "Seu objetivo é abrir celas seguras e evitar cair em armadilhas.\n\n\n"
                                                            "Nosso bot é baseado em uma rede neural da OpenAI.\n"
                                                            "Ele pode prever a localização das estrelas com 85% de probabilidade.",
                         reply_markup=keyboard
                         )

    if call.data == "registration":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        register_button = types.InlineKeyboardButton(text="📱 🔶Registro", url='https://1wprru.life/?open=register#yrs1')
        back_button = types.InlineKeyboardButton(text="🔙 Voltar ao menu principal", callback_data="subscriber")
        keyboard.add(register_button, back_button)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        await bot.send_photo(chat_id=call.message.chat.id,
                             photo=open('resources/registration.jpg', 'rb'),
                         caption="🔷 1. Para começar, cadastre-se usando o link do site. <a href='https://1wprru.life/?open=register#yrs1' style='text-decoration:none'>1WIN (CLICK)</a>\n"
                              "🔷 2. Após o cadastro bem sucedido, copie seu ID no site (aba ‘Reabastecimento’ e seu ID estará no canto superior direito).\n"
                              "🔷 3.E envie para o bot em resposta a esta mensagem!",
                         reply_markup=keyboard,
                         parse_mode='HTML'
                         )


    if call.data == "instruction":
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        back_button = types.InlineKeyboardButton(text="🔙 Voltar ao menu principal", callback_data="subscriber")
        keyboard.add(back_button)
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        await bot.send_photo(chat_id=call.message.chat.id,photo=open('resources/instruction.JPG', 'rb'), caption="O bot é baseado e treinado em um cluster de rede neural 🖥 [bitsGap].\n\n"
                                                       "🎰 Mais de 10.000 partidas foram disputadas para treinar o bot.\n"
                                                       "No momento, os usuários de bot ganham com sucesso de 15 a 25% de seu 💸 capital por dia!\n\n"
                                                       "No momento, o bot ainda está passando por verificações e correções! A precisão do bot é de 92%!\n\n"
                                                       "Para obter lucro máximo, siga as seguintes instruções:\n\n"
                                                       "🟢 1. Cadastre-se na casa de apostas <a href='https://1wprru.life/?open=register#yrs1' style='text-decoration:none'>1WIN (CLICK)</a>\n"
                                                       "Se não abrir, entre com VPN habilitada (Suécia). O Play Market/App Store está cheio de serviços gratuitos, por exemplo: Vpnify, Planet VPN, Hotspot VPN e assim por diante!\n\n"
                                                       "Sem registro, o acesso aos sinais não será aberto!\n\n"
                                                       "🟢 2. Recarregue o saldo da sua conta.\n\n"
                                                       "🟢 3. Vá para a seção de jogos 1win e selecione o jogo 💣'MINES'.\n\n"
                                                       "🟢 4. Defina o número de armadilhas para três. É importante!\n\n"
                                                       "🟢 5. Solicite um sinal no bot e faça apostas com base nos sinais do bot.\n\n"
                                                       "🟢 6. Se o sinal não tiver sucesso, recomendamos dobrar (X²) a aposta para cobrir completamente a perda no próximo sinal.",
                         reply_markup=keyboard,
                         parse_mode="HTML"
                         )

    if call.data == "get_signal":
        async with session_maker() as session:
            user1 = await session.execute(select(User).where(User.telegram_id == call.message.chat.id))
            user2 = await session.execute(select(User).where(User.telegram_id == call.message.chat.id))
            if (user1.scalar_one_or_none() is None) or (user2.scalar_one_or_none().casino_id is None):
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                register_button = types.InlineKeyboardButton(text="📱 🔶Registro",
                                                             url='https://1wprru.life/?open=register#yrs1')
                keyboard.add(register_button)
                await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
                await bot.send_message(chat_id=call.message.chat.id, text="Por favor, registre-se antes de receber um sinal", reply_markup=keyboard)
            else:
                keyboard = types.InlineKeyboardMarkup(row_width=1)
                webapp = types.WebAppInfo("https://yemines.online/")
                apple_app_button = types.InlineKeyboardButton(text="🍏 Abra o aplicativo da Web iOS", web_app=webapp)
                android_app_button = types.InlineKeyboardButton(text="🤖 Abra o Android | WINDOWS", web_app=webapp)
                back_button = types.InlineKeyboardButton(text="🔙 Voltar ao menu principal", callback_data="subscriber")
                keyboard.add(apple_app_button, android_app_button, back_button)
                await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
                await bot.send_message(chat_id=call.message.chat.id, text="Aplicação WEB:", reply_markup=keyboard)

    if call.data == "close_menu":
        await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)


@bot.message_handler(func=lambda message: message.text.isdigit() and len(message.text) <= 10)
async def handle_custom_number(message):
    async with session_maker() as session:
        user1 = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
        user2 = await session.execute(select(User).where(User.telegram_id == message.from_user.id))
        if user1.scalar_one_or_none() and (user2.scalar_one_or_none().casino_id is None):
            await session.execute(update(User).where(User.telegram_id == message.from_user.id).values(casino_id=message.text))
            await session.commit()
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            instruction_button = types.InlineKeyboardButton(text="📚 Instruções", callback_data="instruction")
            get_signal_button = types.InlineKeyboardButton(text="💣 Receba um sinal 💣", callback_data="get_signal")
            close_menu_button = types.InlineKeyboardButton(text="❌ Fechar", callback_data="close_menu")
            keyboard.add(get_signal_button, instruction_button, close_menu_button)
            await bot.send_message(message.chat.id, "Você se registrou com sucesso! Agora você tem acesso aos sinais.", reply_markup=keyboard)



@bot.message_handler(func=lambda message: (message.text and not (message.text.isdigit())) and (message.from_user.username == ADMIN_1 or message.from_user.username == ADMIN_2))
async def handle_admin_post(message):
    async with session_maker() as session:
        result = await session.execute(select(User))
        users = result.scalars()
        for user in users:
            await bot.send_message(chat_id=user.telegram_id, text=message.text)

@bot.message_handler(content_types=['photo', 'document', 'video'])
async def handle_admin_post_photo(message):
    print(message)
    if (message.from_user.username == ADMIN_1) or (message.from_user.username == ADMIN_2):
        async with session_maker() as session:
            result = await session.execute(select(User))
            users = result.scalars()
            for user in users:
                await bot.copy_message(chat_id=user.telegram_id, from_chat_id=message.chat.id, message_id=message.id)


async def on_startup(bot):
    run_param = False
    if run_param:
        await drop_db()

    await create_db()


async def on_shutdown(bot):
    print('Bot shut down...')

async def main():
    await on_startup(bot)
    await bot.polling(none_stop=True)

asyncio.run(main())