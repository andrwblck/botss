from aiogram.filters.callback_data import CallbackData


class FoodData(CallbackData, prefix="food"):
    name: str
    cooldown: int
