from aiogram.utils.keyboard import InlineKeyboardBuilder

from callback.data import FoodData


def start():
    kb = InlineKeyboardBuilder()

    kb.button(text="Фрукти", callback_data="veg")
    kb.button(text="Фастфуд", callback_data="junk")
    kb.button(text="Стан", callback_data="profile")

    kb.adjust(2, 1)

    return kb.as_markup()


def veg():
    kb = InlineKeyboardBuilder()

    kb.button(text="🥝 Ківі", callback_data=FoodData(name="Ківі", cooldown=24))
    kb.button(text="🥭 Манго", callback_data=FoodData(name="Манго", cooldown=17))
    kb.button(text="🍑 Персик", callback_data=FoodData(name="Персик", cooldown=10))
    kb.button(text="🍉 Кавун", callback_data=FoodData(name="Кавун", cooldown=3))

    kb.button(text="👈 Назад", callback_data="back")

    kb.adjust(1)

    return kb.as_markup()


def junk():
    kb = InlineKeyboardBuilder()

    kb.button(text="🍔 Гамбургер", callback_data=FoodData(name="Гамбургер", cooldown=24))
    kb.button(text="🍕 Піца", callback_data=FoodData(name="Піца", cooldown=17))
    kb.button(text="🌭 Хотдог", callback_data=FoodData(name="Хотдог", cooldown=10))
    kb.button(text="🌮 Тако", callback_data=FoodData(name="Тако", cooldown=3))

    kb.button(text="👈 Назад", callback_data="back")

    kb.adjust(1)

    return kb.as_markup()


def back():
    kb = InlineKeyboardBuilder()

    kb.button(text="👈 Назад", callback_data="back")

    return kb.as_markup()