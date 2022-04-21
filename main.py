import logging
import os
from aiogram import Bot, Dispatcher, executor, types

import markups as nav
from db import BotDB

BotDB = BotDB('users.db')


logging.basicConfig(level=logging.INFO)

BOT_TOKEN = '5376266478:AAEPayJ2gwxFbkT8hxqk5ufaKEdLNVC42Mg'
bot = Bot(token=BOT_TOKEN)
APP_URL = 'https://ctyptown.herokuapp.com/' + BOT_TOKEN
dp = Dispatcher(bot)

admin = [491603763, 999374204, 2066551161]
b = ['1', '11', '13', '20', '30', '32', '34', '35', '36', '37', '42', '44', '46', '49', '51', '56', '58', '59', '60', '70', '73', '76', '78', '84', '86', '90', '95', '96', '98', '100']

def avaliable():
    file_names = os.listdir('avaliable')
    return sorted([int(i.replace('.png', '')) for i in file_names])

def count_nft(user_id):
    mynft = BotDB.get_nft(user_id)
    if mynft:
        return mynft.split(',')
    else:
        return 0

"""Страт бота"""
@dp.message_handler(commands=['start', 'help', 'menu'])
async def start(message: types.Message):
    if not BotDB.user_exists(message.from_user.id):
        BotDB.add_user(message.from_user.id)
    BotDB.new_menu(message.from_user.id, 0)

    if admin.count(message.from_user.id) != 0:
        await bot.send_message(message.from_user.id,
                               text=f'Admin {message.from_user.id}', reply_markup=nav.Statistic)
    else:
        await bot.send_message(message.from_user.id, text='Бот поможет купить наши NFT, поторопись всего 100 жителей по 5💎\nДля начала работы, выберите раздел:', reply_markup=nav.mainMenu)


"""Покупка NFT"""
@dp.callback_query_handler(text='buyNFT')
async def buyNFT(message: types.Message):

    BotDB.new_menu(message.from_user.id, 1)

    BotDB.update()


    if BotDB.get_tonkeepr(message.from_user.id):
        buy = BotDB.get_buy(message.from_user.id)
        if buy:
            text=f'👨‍🎤 Вы выбрали жителя под номером {buy}. \n💎 Для покупки переведите 5 TON на Tonkeeper кошелёк \n\n`EQDa7GX9FcBnG1kq3VLyfO6TQrR5WDw9PlkbK43JVYEuuLti` \n\n❗️Комментарий к платежу `{message.from_user.id}`'
            if BotDB.get_proverka(message.from_user.id):
                BotDB.new_menu(message.from_user.id, 6)
                await bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text=text, parse_mode="Markdown", reply_markup=nav.backMenu)
            else:
                await bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text=text, parse_mode="Markdown", reply_markup=nav.buyMenu)
        else:
            if avaliable():
                await bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text=f'💳 Для покупки, отправь боту любой свободный номер.\n👀Напоминаю, в этих номерах скрываются жители категории USUAL/RESIDENT\n\n👻Свободные номера:\n{str(avaliable())[1:-1]}', reply_markup=nav.backMenu)
            else:
                await bot.send_message(chat_id=message.message.chat.id, text=f'Все NFT куплены', reply_markup=nav.backMenu)

    else:
        BotDB.new_menu(message.from_user.id, 11)
        await bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text='Введите ваш Tonkeepr кошелек. Это нужно для того чтобы потом, и передать вам ваши NFT', reply_markup=nav.backMenu)

    await message.answer()


@dp.callback_query_handler(text='myNFT')
async def myNFT(message: types.Message):
    BotDB.new_menu(message.from_user.id, 2)
    mynft = count_nft(message.from_user.id)
    if mynft != 0:
        media = []
        for i in mynft:
            if i:
                media.append(types.InputMediaPhoto(open(f'inaccessible/{i}.png', 'rb')))

        await bot.send_message(chat_id=message.message.chat.id, text="🕑️ Загрузка...")

        for i in range(0, len(media), 10):
            await bot.send_media_group(message.from_user.id, media=media[i:i + 10])

        c = []
        for i in mynft:
            for j in b:
                if i == j:
                    c.append(i)
                    break

        await bot.send_message(chat_id=message.message.chat.id, text=f'🧑🏽‍🎤 Твои жители \nUSUAL - {len(mynft)-len(c)}\nRESIDENT - {len(c)}', reply_markup=nav.backMenu)

    else:
        await bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                    text='Ты еще не приобрел своего жителя 🧑', reply_markup=nav.backMenu)
    await message.answer()


@dp.callback_query_handler(text='oProject')
async def oProject(message: types.Message):
    BotDB.new_menu(message.from_user.id, 3)
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id, text='О проекте:\n🏛Представляем вам «Криптаун», метаполис свободы и гармонии, со своими NFT-жителями олицетворяющими криптовалюту.\n💎Наша NFT-коллекция не просто набор иллюстраций, а экосистема будущего (которая будет включать в себя: DAO, стейкинг, NFT-аватары для телеграм сообществ, P2E игру).\n💙Оставайтесь с нами, ведь за нами будущее!', reply_markup=nav.backMenu)
    await message.answer()
@dp.callback_query_handler(text='oNas')
async def oNas(message: types.Message):
    BotDB.new_menu(message.from_user.id, 4)
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id,
                                text='🦸🏼Команда «Cryptown» состоит из четырёх человек:\nХудожник – Егор (@fridins).\nВеб-разработчик – Илья (@Mer3avchik).\nИдейный вдохновитель – Кирилл (@kireeshk).\nПрограммист - Вова (@mango_cs).\n\n🔥Каждый из нас будет рад ответить на все ваши вопросы и предложения!', reply_markup=nav.backMenu)
    await message.answer()


@dp.callback_query_handler(text='profile')
async def profile(message: types.Message):
    BotDB.new_menu(message.from_user.id, 5)
    tonkeepr = BotDB.get_tonkeepr(message.from_user.id)
    if not tonkeepr:
        tonkeepr = 'Не указан'
    if not count_nft(message.from_user.id):
        count = 0
    else:
        count = len(count_nft(message.from_user.id))
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id,
                                text=f'<strong>ID:</strong> <code>{message.from_user.id}</code>\n<strong>Количество жителей: {count}</strong>\n<strong>Tonkeepr:</strong> <code>{tonkeepr}</code>',
                                parse_mode='HTML',
                                reply_markup=nav.backMenu)
    await message.answer()


@dp.callback_query_handler(text='back')
async def back_menu(message: types.Message):
    if BotDB.get_menu(message.from_user.id) in [2, 1, 6]:
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
        await bot.send_message(chat_id=message.from_user.id, text='Бот поможет купить наши NFT, поторопись всего 100 жителей по 5💎\nДля начала работы, выберите раздел:', reply_markup=nav.mainMenu)
    else:
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id, text='Бот поможет купить наши NFT, поторопись всего 100 жителей по 5💎\nДля начала работы, выберите раздел:', reply_markup=nav.mainMenu)
    BotDB.new_menu(message.from_user.id, 0)
    await message.answer()





""" ОБРАЮОТКА ПОКУПКИ """
@dp.callback_query_handler(text='prover')
async def prover(message: types.Message):
    BotDB.add_proverka(message.from_user.id)

    await bot.edit_message_reply_markup(chat_id=message.from_user.id, message_id=message.message.message_id, reply_markup=nav.backMenu)

    await bot.send_message(chat_id=message.from_user.id, text='🕑️ Запрос на проверку отправлен')
    await bot.send_message(chat_id='491603763', text=f'{message.from_user.id} запросил проверку оплаты (житель № {BotDB.get_buy(message.from_user.id)})', reply_markup=nav.ChackPay)
    await bot.send_message(chat_id='999374204', text=f'{message.from_user.id} запросил проверку оплаты (житель № {BotDB.get_buy(message.from_user.id)})', reply_markup=nav.ChackPay)
    await message.answer()

@dp.callback_query_handler(text='otmena')
async def otmena(message: types.Message):
    num = BotDB.get_buy(message.from_user.id)
    if num:
        os.replace(f'inaccessible/{num}.png', f'avaliable/{num}.png')
        BotDB.del_buy(message.from_user.id)
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
        await bot.send_message(chat_id=message.from_user.id, text='Бот поможет купить наши NFT, поторопись всего 100 жителей по 5💎\nДля начала работы, выберите раздел:', reply_markup=nav.mainMenu)
    else:
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message.message_id)
        await bot.send_message(chat_id=message.from_user.id, text='Бот поможет купить наши NFT, поторопись всего 100 жителей по 5💎\nДля начала работы, выберите раздел:', reply_markup=nav.mainMenu)
    await message.answer()


"""ADMIN"""
@dp.callback_query_handler(text='yes')
async def yes(message: types.Message):
    user_id = message.message.text.split(' ')[0]
    nft = BotDB.get_buy(user_id)
    BotDB.add_nft(user_id, nft)

    await bot.send_message(chat_id=user_id, text=f'✅ Оплата подтверждена')
    BotDB.del_buy(user_id)
    BotDB.del_proverka(user_id)
    await bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id,
                                text=f'{message.message.text}\n✅ Оплатил')
    await message.answer()

@dp.callback_query_handler(text='no')
async def no(message: types.Message):
    user_id = message.message.text.split(' ')[0]
    BotDB.del_proverka(user_id)
    await bot.edit_message_text(chat_id=message.message.chat.id, message_id=message.message.message_id, text=f'{message.message.text}\n❌ Не оплатил')

    await bot.send_message(chat_id=user_id, text=f'❌ Оплата не подтверждена')

    await message.answer()




@dp.message_handler(content_types=['text'])
async def get_text_messages(message: types.Message):
    msg = BotDB.get_menu(message.from_user.id)
    error_msg = ''
    if msg == 1 and not BotDB.get_buy(message.from_user.id):
        try:
            if 1 <= int(message.text) <= 100:
                if int(message.text) in avaliable():
                    BotDB.add_buy(message.from_user.id, int(message.text))
                    await bot.send_message(chat_id=message.chat.id, text=f'👨‍🎤 Вы выбрали жителя под номером {message.text}. \n💎 Для покупки переведите 5 TON на Tonkeeper кошелёк \n\n`EQDa7GX9FcBnG1kq3VLyfO6TQrR5WDw9PlkbK43JVYEuuLti` \n\n❗️Комментарий к платежу `{message.from_user.id}`', parse_mode="Markdown", reply_markup=nav.buyMenu)
                else:
                    error_msg = f'❗️Жителя под номером {message.text} уже купили'
            else:
                error_msg = f'❗️Жителя под номером {message.text} не существует'
        except:
            error_msg = f'❗️"{message.text}" не является числом'
            if error_msg:
                await bot.send_message(chat_id=message.chat.id, text=f'{error_msg}\n\n💳 Для покупки, отправь боту любой свободный номер.\n👀Напоминаю, в этих номерах скрываются жители категории USUAL/RESIDENT\n\n👻Свободные номера:\n{str(avaliable())[1:-1]}', parse_mode="Markdown", reply_markup=nav.backMenu)
    elif msg == 11:
        BotDB.add_tonkeepr(message.from_user.id, message.text)
        await bot.send_message(chat_id=message.chat.id, text='✅ Кошелек сохранен')
        BotDB.new_menu(message.from_user.id, 1)
        if avaliable():
            await bot.send_message(chat_id=message.chat.id,
                                   text=f'💳 Для покупки, отправь боту любой свободный номер.\n👀Напоминаю, в этих номерах скрываются жители категории USUAL/RESIDENT\n\n👻Свободные номера:\n{str(avaliable())[1:-1]}',
                                   reply_markup=nav.backMenu)
        else:
            await bot.send_message(chat_id=message.message.chat.id,
                                   text=f'Все NFT куплены',
                                   reply_markup=nav.backMenu)
    else:
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id)











@dp.callback_query_handler(text='avaliable')
async def no(message: types.Message):
    admin_avaliable = BotDB.admin_avaliable()
    admin_delayed_nft = BotDB.admin_delayed_nft()
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id,
                                text=f'✅ Купленные NFT ({len(admin_avaliable)}):\n{str(admin_avaliable)[1:-1]}\n\n🕑 Отложенные NFT ({len(admin_delayed_nft)}):\n{str(admin_delayed_nft)[1:-1]}\n\n🖼 Не купленные NFT ({len(avaliable())}):\n{str(avaliable())[1:-1]}', reply_markup=nav.backAdmin)
    await message.answer()
@dp.callback_query_handler(text='people')
async def no(message: types.Message):
    all_people = BotDB.all_people()
    active_people = BotDB.active_people()
    not_active_people = BotDB.not_active_people()
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id,
                                text=f'🏘 Все пользователи: {all_people}\n\n🏡 Пользователи с NFT: {active_people} ({round(active_people*100/all_people)}%)\n\n🏚 Без Tonkeepr (неактивные): {not_active_people} ({round(not_active_people*100/BotDB.all_people())}%)',
                                reply_markup=nav.backAdmin)
    await message.answer()
@dp.callback_query_handler(text='allstatistic')
async def no(message: types.Message):
    all = BotDB.all_statistic()
    text = ''.join([f"<strong>ID:</strong> <code>{i[0]}</code>\n<strong>Tonkeepr:</strong> <code>{i[1]}</code>\n<strong>NFT: {i[2]}</strong>\n\n" for i in all])
    if text:
        text = f'🧑‍💻 Покупатели\n\n{text}'
    else:
        text = '😔 Пока что покупателей нету'
    try:
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id,
                                    text=text, parse_mode="HTML",
                                    reply_markup=nav.backAdmin)
    except:
        await bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id,
                                    text=f'Ошибка! Слишком большой текст\nНа меню времени не хватило)',
                                    reply_markup=nav.backAdmin)

    await message.answer()
@dp.callback_query_handler(text='backAdmin')
async def no(message: types.Message):
    await bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message.message_id,
                                text=f'Admin {message.from_user.first_name}', reply_markup=nav.Statistic)
    await message.answer()






if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

