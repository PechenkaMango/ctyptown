from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

""" ГЛАВНОЕ МЕНЮ """
mainMenu = InlineKeyboardMarkup(row_width=2)
buyNFT = InlineKeyboardButton(text='🛍️ Купить', callback_data='buyNFT')
myNFT = InlineKeyboardButton(text='🎒 Мои NFT', callback_data='myNFT')
oProject = InlineKeyboardButton(text='🏙️ О проекте', callback_data='oProject')
oNas = InlineKeyboardButton(text='👥 О нас', callback_data='oNas')
profile = InlineKeyboardButton(text='👨‍💻 Кабинет', callback_data='profile')


mainMenu.insert(buyNFT)
mainMenu.insert(myNFT)
mainMenu.insert(oProject)
mainMenu.insert(oNas)
mainMenu.insert(profile)


""" НАЗАД """
backMenu = InlineKeyboardMarkup(row_width=1)
back = InlineKeyboardButton(text='◀️ Назад', callback_data='back')

backMenu.insert(back)

""" ПОКУПКА/ОТМЕНА """
buyMenu = InlineKeyboardMarkup(row_width=2)
prover = InlineKeyboardButton(text='⏱ Проверить оплату', callback_data='prover')
otmena = InlineKeyboardButton(text='❌ Отменить', callback_data='otmena')
back = InlineKeyboardButton(text='◀️ Назад', callback_data='back')

buyMenu.insert(prover)
buyMenu.insert(otmena)
buyMenu.insert(back)

"""ADMIN"""
ChackPay = InlineKeyboardMarkup(row_width=2)
yes = InlineKeyboardButton(text='✅ Оплатил', callback_data='yes')
no = InlineKeyboardButton(text='❌ Не оплатил', callback_data='no')

ChackPay.insert(yes)
ChackPay.insert(no)


"""STATISTIC"""
Statistic = InlineKeyboardMarkup(row_width=2)
avaliable = InlineKeyboardButton(text='💸 Купленные NFT', callback_data='avaliable')
people = InlineKeyboardButton(text='👥 Пользователи', callback_data='people')
allstatistic = InlineKeyboardButton(text='📊 Покупатели', callback_data='allstatistic')

Statistic.insert(avaliable)
Statistic.insert(people)
Statistic.insert(allstatistic)

backAdmin = InlineKeyboardMarkup(row_width=1)
backs = InlineKeyboardButton(text='◀️ Назад', callback_data='backAdmin')

backAdmin.insert(backs)
